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
