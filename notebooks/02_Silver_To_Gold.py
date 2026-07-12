# Databricks notebook source
import json
import re

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

print(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get())

# COMMAND ----------

dbutils.widgets.text("dataset_name", "")
dbutils.widgets.text("silver_path", "")
dbutils.widgets.text("gold_path", "")
dbutils.widgets.text("write_mode", "overwrite")
dbutils.widgets.text("config_file", "")

config_file = dbutils.widgets.get("config_file")
dataset_name = "customers"

silver_path = "abfss://silver@stretaillakehouse001.dfs.core.windows.net/customers/"

gold_path = "abfss://gold@stretaillakehouse001.dfs.core.windows.net/dim_customers/"

write_mode = "overwrite"

# COMMAND ----------

config_file = "abfss://config@stretaillakehouse001.dfs.core.windows.net/gold_metadata.json"

# COMMAND ----------

df = spark.read.format("delta").load(silver_path)

display(df.limit(5))


# COMMAND ----------

metadata_df = spark.read.option("multiline", "true").json(config_file)

display(metadata_df)

# COMMAND ----------

