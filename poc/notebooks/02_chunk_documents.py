# Databricks notebook source
# MAGIC %md
# MAGIC # Turn documents into a table
# MAGIC
# MAGIC You have a volume full of markdown files. A language model cannot read all of them
# MAGIC at once, and you would not want it to — you want the handful of paragraphs relevant
# MAGIC to the question.
# MAGIC
# MAGIC So: read the files, split them into chunks, write a table.
# MAGIC
# MAGIC That is **extract, transform, load**. Same three steps as the CSV work in Part 2.4.
# MAGIC The content is prose instead of rows; nothing else about the pattern changes.

# COMMAND ----------

# Point these at your own catalog, schema and volume.
CATALOG = "workspace"
SCHEMA = "default"
VOLUME = "handbook"

SOURCE = f"/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}"
TARGET = f"{CATALOG}.{SCHEMA}.handbook_chunks"

WORDS_PER_CHUNK = 200
OVERLAP_WORDS = 40

# COMMAND ----------

# MAGIC %md
# MAGIC ## Extract — read the files
# MAGIC
# MAGIC `wholetext=True` gives one row per file rather than one row per line, which is what
# MAGIC we want since we are about to split them ourselves.
# MAGIC
# MAGIC `_metadata` is a hidden column Spark attaches to anything read from files, holding
# MAGIC details about where each row came from. We pull `file_name` out of it so every
# MAGIC chunk remembers its source document — which is what makes citations possible later.
# MAGIC
# MAGIC `selectExpr` is `select` that accepts SQL expressions as strings, which is the
# MAGIC easiest way to reach into a nested column like that one.

# COMMAND ----------

raw = (
    spark.read.option("wholetext", True)
    .text(SOURCE)
    .selectExpr("_metadata.file_name AS doc_name", "value AS content")
)

display(raw.select("doc_name"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transform — split into chunks
# MAGIC
# MAGIC Two decisions worth understanding, because they are the ones that determine whether
# MAGIC retrieval works well:
# MAGIC
# MAGIC **Chunk size.** Too large and you send the model paragraphs of irrelevant text
# MAGIC alongside the useful sentence. Too small and you cut sentences off from the context
# MAGIC that makes them meaningful. A couple of hundred words is a reasonable starting point
# MAGIC for prose like this.
# MAGIC
# MAGIC **Overlap.** Chunks share a few dozen words with their neighbours, so a fact that
# MAGIC falls on a boundary still appears whole in one of them. Without overlap, the single
# MAGIC most important sentence in a document can end up split across two chunks and match
# MAGIC neither.
# MAGIC
# MAGIC ### Three Spark things in the next cell
# MAGIC
# MAGIC The splitting itself is ordinary Python. Getting Spark to *apply* it needs three
# MAGIC pieces you probably haven't met:
# MAGIC
# MAGIC - **`udf`** — a **user-defined function.** Spark's built-in functions run across a
# MAGIC   cluster; your own Python function doesn't, until you wrap it in a `udf` so Spark
# MAGIC   can ship it out to every machine and run it on each row.
# MAGIC - **`explode`** — our function returns a *list* of chunks per document, giving one
# MAGIC   row with a list in it. `explode` turns that list into one row per element. Twelve
# MAGIC   rows of lists become fourteen rows of chunks.
# MAGIC - **`monotonically_increasing_id()`** — generates a unique number per row. Awkward
# MAGIC   name, simple job: we need an id for each chunk, and rows are spread across
# MAGIC   machines, so a plain counter wouldn't work.

# COMMAND ----------

from pyspark.sql.functions import explode, udf
from pyspark.sql.types import ArrayType, StringType


def split_into_chunks(text, size=WORDS_PER_CHUNK, overlap=OVERLAP_WORDS):
    words = text.split()
    if not words:
        return []

    step = size - overlap
    chunks = []
    start = 0
    while start < len(words):
        chunks.append(" ".join(words[start : start + size]))
        if start + size >= len(words):
            break  # this chunk reached the end; another would just repeat its tail
        start += step
    return chunks


split_udf = udf(split_into_chunks, ArrayType(StringType()))

chunked = (
    raw.withColumn("chunk_text", explode(split_udf("content")))
    .drop("content")
    .selectExpr(
        "doc_name",
        "monotonically_increasing_id() AS chunk_id",
        "chunk_text",
    )
)

print(f"{raw.count()} documents -> {chunked.count()} chunks")
display(chunked.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load — write the table
# MAGIC
# MAGIC `saveAsTable` writes a real, permanent Delta table into Unity Catalog — the same
# MAGIC kind of table you made from a CSV in Part 2.4, and queryable by anyone you grant
# MAGIC access to.
# MAGIC
# MAGIC `mode("overwrite")` replaces the table if it already exists, so you can safely
# MAGIC re-run this notebook after changing the chunk size or editing a document. Without
# MAGIC it, a second run would fail rather than update.

# COMMAND ----------

chunked.write.mode("overwrite").saveAsTable(TARGET)

print(f"Wrote {TARGET}")
display(spark.sql(f"SELECT doc_name, count(*) AS chunks FROM {TARGET} GROUP BY 1 ORDER BY 1"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Now go back to your laptop
# MAGIC
# MAGIC Put the table name in your `.env`:
# MAGIC
# MAGIC ```
# MAGIC DATABRICKS_CHUNKS_TABLE=workspace.default.handbook_chunks
# MAGIC ```
# MAGIC
# MAGIC The assistant will pick it up and gain a second tool.
