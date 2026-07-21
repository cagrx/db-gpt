"""
Ask Databricks questions in plain English.

The model never sees your data. It sees the *shape* of your data — table and column
names — and writes SQL. We run that SQL against Databricks and hand back the rows.

Run it:  python assistant.py
"""

import json
import os
import re
import sys
from pathlib import Path

from databricks import sql
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
TABLE = os.getenv("DATABRICKS_TABLE", "samples.nyctaxi.trips")
CHUNKS_TABLE = os.getenv("DATABRICKS_CHUNKS_TABLE")  # optional — Stage 2
MAX_ROWS = 200
CACHE = Path(__file__).parent / ".cache" / "embeddings.json"

REQUIRED = (
    "DATABRICKS_SERVER_HOSTNAME",
    "DATABRICKS_HTTP_PATH",
    "DATABRICKS_TOKEN",
    "OPENAI_API_KEY",
)

# Check everything before doing anything, so a missing value produces a sentence
# rather than a stack trace from somewhere deep in a library.
_missing = [name for name in REQUIRED if not os.getenv(name)]
if _missing:
    sys.exit(
        "Missing from your .env file: "
        + ", ".join(_missing)
        + "\n\nIf you haven't created it yet:  cp .env.example .env"
        + "\nThen fill in the values -- see .env.example for where each one comes from."
    )

client = OpenAI()


# --------------------------------------------------------------------------
# Guardrails
# --------------------------------------------------------------------------

BANNED = re.compile(
    r"\b(insert|update|delete|drop|alter|create|merge|truncate|grant|revoke|copy)\b",
    re.IGNORECASE,
)


def is_read_only(query: str) -> bool:
    """Allow a single SELECT (or WITH ... SELECT) and nothing else.

    This is deliberately blunt. It will occasionally reject a legitimate query --
    a string literal containing the word 'update', say. That is the right trade:
    a false rejection costs you one retry, a false acceptance costs you a table.
    """
    q = query.strip().rstrip(";")
    if ";" in q:  # no stacked statements
        return False
    if not re.match(r"^(select|with)\b", q, re.IGNORECASE):
        return False
    return not BANNED.search(q)


# --------------------------------------------------------------------------
# Databricks
# --------------------------------------------------------------------------


def connect():
    return sql.connect(
        server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"],
    )


def describe(cursor, table: str) -> str:
    """Column names and types, formatted for the system prompt."""
    cursor.execute(f"DESCRIBE TABLE {table}")
    lines = []
    for row in cursor.fetchall():
        name, dtype = row[0], row[1]
        if not name or name.startswith("#"):  # DESCRIBE emits section headers
            break
        lines.append(f"  {name} ({dtype})")
    return f"{table}\n" + "\n".join(lines)


def run_sql(cursor, query: str) -> dict:
    if not is_read_only(query):
        return {"error": "Rejected: only a single SELECT statement is allowed."}
    try:
        cursor.execute(query)
        rows = cursor.fetchmany(MAX_ROWS)
        columns = [d[0] for d in cursor.description]
    except Exception as exc:  # hand the error back so the model can correct itself
        return {"error": str(exc)}
    return {"columns": columns, "rows": [list(r) for r in rows], "row_count": len(rows)}


# --------------------------------------------------------------------------
# Document search  (Stage 2 -- only active if DATABRICKS_CHUNKS_TABLE is set)
# --------------------------------------------------------------------------


def embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]


def load_chunks(cursor) -> list[dict]:
    """Fetch chunks from Databricks and embed them, caching so we only pay once."""
    if CACHE.exists():
        return json.loads(CACHE.read_text())

    cursor.execute(f"SELECT doc_name, chunk_id, chunk_text FROM {CHUNKS_TABLE}")
    rows = cursor.fetchall()
    print(f"Embedding {len(rows)} chunks (one time only)...")

    vectors = embed([row[2] for row in rows])
    chunks = [
        {"doc": row[0], "chunk_id": row[1], "text": row[2], "vector": vector}
        for row, vector in zip(rows, vectors)
    ]

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(chunks))
    return chunks


def cosine(a: list[float], b: list[float]) -> float:
    """Similarity between two vectors: 1.0 is identical, 0.0 is unrelated.

    This is the whole of 'vector search'. A real vector database does this faster
    over millions of rows -- it does not do anything cleverer.
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def search_documents(chunks: list[dict], question: str, top_k: int = 4) -> dict:
    query_vector = embed([question])[0]
    ranked = sorted(chunks, key=lambda c: cosine(query_vector, c["vector"]), reverse=True)
    return {
        "results": [
            {"source": c["doc"], "text": c["text"]} for c in ranked[:top_k]
        ]
    }


# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------

SQL_TOOL = {
    "type": "function",
    "name": "run_sql",
    "description": (
        "Run a read-only SQL query against Databricks and return the rows. "
        "Use this for anything involving numbers, counts, averages or aggregation."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "A single SELECT statement."}
        },
        "required": ["query"],
    },
}

DOCS_TOOL = {
    "type": "function",
    "name": "search_documents",
    "description": (
        "Search company policy documents for passages relevant to a question. "
        "Use this for questions about policy, process or rules rather than numbers."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The user's question."}
        },
        "required": ["question"],
    },
}


def system_prompt(schema: str, has_docs: bool) -> str:
    prompt = f"""You answer questions about a company's data.

You have access to this table:

{schema}

Use run_sql for anything numerical. Write standard Spark SQL. Prefer aggregate queries
over returning many raw rows, and always use LIMIT when returning individual rows.
"""
    if has_docs:
        prompt += """
Use search_documents for questions about policy, process or rules. When you answer from
documents, cite the source file you used.
"""
    prompt += """
If the data cannot answer the question, say so plainly. Never invent a number, and never
guess at a column that is not listed above. If a query fails, read the error and try once
more with a corrected query.
"""
    return prompt


# --------------------------------------------------------------------------
# The loop
# --------------------------------------------------------------------------


def answer(question: str, cursor, tools, instructions: str, chunks) -> str:
    conversation = [{"role": "user", "content": question}]

    for _ in range(6):  # bounded, so a confused model cannot loop forever
        response = client.responses.create(
            model=MODEL,
            instructions=instructions,
            tools=tools,
            input=conversation,
        )
        conversation += response.output

        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            return response.output_text

        for call in calls:
            args = json.loads(call.arguments)
            if call.name == "run_sql":
                print(f"\n  SQL: {args['query']}\n")
                result = run_sql(cursor, args["query"])
            else:
                result = search_documents(chunks, args["question"])
            conversation.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result, default=str),
                }
            )

    return "Gave up after too many attempts."


def main() -> None:
    with connect() as connection, connection.cursor() as cursor:
        schema = describe(cursor, TABLE)
        tools = [SQL_TOOL]
        chunks = None

        if CHUNKS_TABLE:
            chunks = load_chunks(cursor)
            tools.append(DOCS_TOOL)

        instructions = system_prompt(schema, has_docs=chunks is not None)

        print(f"Connected. Asking about {TABLE}.")
        print("Type a question, or Ctrl-C to quit.\n")

        while True:
            try:
                question = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not question:
                continue
            print(answer(question, cursor, tools, instructions, chunks) + "\n")


if __name__ == "__main__":
    main()
