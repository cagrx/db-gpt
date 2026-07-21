# Databricks notebook source
# MAGIC %md
# MAGIC # Explore the schema
# MAGIC
# MAGIC Before you can tell a language model what is in a database, you have to know
# MAGIC yourself. This notebook is that step.
# MAGIC
# MAGIC Run it in Databricks. Everything here is read-only.

# COMMAND ----------

TABLE = "samples.nyctaxi.trips"

# COMMAND ----------

# MAGIC %md
# MAGIC ## What columns exist, and what type is each?
# MAGIC
# MAGIC `DESCRIBE TABLE` asks the database about *itself* rather than about the data. It
# MAGIC returns one row per column — name, type, and any comment. This is exactly what
# MAGIC goes into the assistant's instructions later.
# MAGIC
# MAGIC `display()` is a Databricks function, not standard Python. It renders a result as
# MAGIC a sortable, filterable table with charting built in, rather than the wall of text
# MAGIC `print()` would give you. Use it for anything you actually want to look at.

# COMMAND ----------

display(spark.sql(f"DESCRIBE TABLE {TABLE}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## What does the data actually look like?
# MAGIC
# MAGIC Column names lie. `fare_amount` could be dollars or cents; `pickup_zip` could be
# MAGIC a number or a string with leading zeros. Look before you assume.

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {TABLE} LIMIT 20"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## How much data is there, and over what period?

# COMMAND ----------

display(
    spark.sql(
        f"""
        SELECT
          count(*)                AS trips,
          min(tpep_pickup_datetime) AS earliest,
          max(tpep_pickup_datetime) AS latest,
          round(avg(fare_amount), 2) AS avg_fare,
          round(avg(trip_distance), 2) AS avg_miles
        FROM {TABLE}
        """
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Is it clean?
# MAGIC
# MAGIC It is not. Real data never is — there are zero-distance trips and negative fares
# MAGIC in here. Worth seeing now, because when your assistant returns a strange average
# MAGIC later, this is why.

# COMMAND ----------

display(
    spark.sql(
        f"""
        SELECT
          sum(CASE WHEN fare_amount <= 0 THEN 1 ELSE 0 END)   AS non_positive_fares,
          sum(CASE WHEN trip_distance <= 0 THEN 1 ELSE 0 END) AS zero_distance,
          sum(CASE WHEN pickup_zip IS NULL THEN 1 ELSE 0 END) AS missing_pickup_zip
        FROM {TABLE}
        """
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write down what you learned
# MAGIC
# MAGIC You should now be able to say, without looking it up:
# MAGIC
# MAGIC - which columns exist and roughly what they hold
# MAGIC - what one row represents (one taxi trip)
# MAGIC - one thing that is untidy about the data
# MAGIC
# MAGIC That is what you are about to hand to the model. Back to your laptop.
