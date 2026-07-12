# Databricks notebook source
display(dbutils.fs.ls("abfss://bronze@stretaillakehouse001.dfs.core.windows.net/"))

# COMMAND ----------

# MAGIC %md
# MAGIC #Import

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time
start_time = time.time()

# COMMAND ----------

dbutils.widgets.text("dataset_name", "customers")
dbutils.widgets.text(
    "source_path",
    "abfss://bronze@stretaillakehouse001.dfs.core.windows.net/customers/"
)
dbutils.widgets.text(
    "target_path",
    "abfss://silver@stretaillakehouse001.dfs.core.windows.net/customers/"
)
dbutils.widgets.dropdown(
    "write_mode",
    "overwrite",
    ["overwrite", "append"],
    "Write Mode"
)

# COMMAND ----------

dataset_name = dbutils.widgets.get("dataset_name")
source_path = dbutils.widgets.get("source_path")
target_path = dbutils.widgets.get("target_path")
write_mode = dbutils.widgets.get("write_mode")

# COMMAND ----------

print("=" * 50)
print(f"Dataset      : {dataset_name}")
print(f"Source Path  : {source_path}")
print(f"Target Path  : {target_path}")
print(f"Write Mode   : {write_mode}")
print("=" * 50)

# COMMAND ----------

# MAGIC %md
# MAGIC # reading Files

# COMMAND ----------

df = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(source_path)
)

# COMMAND ----------

print("=" * 50)
print("Reading Bronze Dataset")
print("=" * 50)

print(f"Dataset Name : {dataset_name}")
print(f"Row Count    : {df.count()}")
print(f"Columns      : {len(df.columns)}")

df.printSchema()

display(df.limit(5))

# COMMAND ----------

import re

def clean_column_names(df):
    """
    Standardize dataframe column names to snake_case.
    """

    cleaned_columns = []

    for column in df.columns:

        # Convert CamelCase / PascalCase to snake_case
        column = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', column)

        # Convert to lowercase
        column = column.lower()

        # Remove leading/trailing spaces
        column = column.strip()

        # Replace spaces and hyphens with underscores
        column = re.sub(r'[\s\-]+', '_', column)

        # Remove all special characters except underscore
        column = re.sub(r'[^a-z0-9_]', '', column)

        # Replace multiple underscores with a single underscore
        column = re.sub(r'_+', '_', column)

        # Remove leading/trailing underscores
        column = column.strip('_')

        cleaned_columns.append(column)

    return df.toDF(*cleaned_columns)

# COMMAND ----------

df = clean_column_names(df)

# COMMAND ----------

print(df.columns)


# COMMAND ----------

print(type(df))

# COMMAND ----------

def trim_string_columns(df):
    """
    Trim leading and trailing spaces from all string columns.
    """

    for field in df.schema.fields:

        if isinstance(field.dataType, StringType):

            df = df.withColumn(
                field.name,
                trim(col(field.name))
            )

    return df

# COMMAND ----------

df=trim_string_columns(df)

# COMMAND ----------

def add_audit_columns(df):
    df=df.withColumn('load_timestamp',current_timestamp())
    df=df.withColumn('source_system', lit('ADF'))
    df=df.withColumn('dataset_name', lit(dataset_name))
    df=df.withColumn('processing_date', current_date())
    return df

# COMMAND ----------

df = add_audit_columns(df)

# COMMAND ----------

df.printSchema()

display(df.limit(5))

# COMMAND ----------

from pyspark.sql.functions import col, when, count

def validate_dataframe(df):
    """
    Validate dataframe before writing to Silver layer.
    """

    row_count = df.count()
    column_count = len(df.columns)

    duplicate_rows = row_count - df.dropDuplicates().count()

    print("=" * 50)
    print("Validation Report")
    print("=" * 50)

    print(f"Dataset          : {dataset_name}")
    print(f"Rows             : {row_count}")
    print(f"Columns          : {column_count}")
    print(f"Duplicate Rows   : {duplicate_rows}")

    print("\nNull Count Per Column")
    print("-" * 50)

    for column in df.columns:

        null_count = (
            df.select(
                count(
                    when(col(column).isNull(), column)
                ).alias("null_count")
            )
            .collect()[0]["null_count"]
        )

        print(f"{column:25} : {null_count}")

    print("=" * 50)

    return True

# COMMAND ----------

validate_dataframe(df)

# COMMAND ----------

def apply_business_rules(df, dataset_name):
    """
    Apply dataset-specific business rules.
    """

    print("=" * 50)
    print("Applying Business Rules")
    print("=" * 50)

    rows_before = df.count()

    if dataset_name == "customers":

        # Remove records with null customer_id
        df = df.filter(col("customer_id").isNotNull())

        # Remove duplicate customer_ids
        df = df.dropDuplicates(["customer_id"])

    rows_after = df.count()

    print(f"Dataset      : {dataset_name}")
    print(f"Rows Before  : {rows_before}")
    print(f"Rows After   : {rows_after}")
    print(f"Rows Removed : {rows_before - rows_after}")

    print("=" * 50)

    return df

# COMMAND ----------

df = apply_business_rules(df, dataset_name)

# COMMAND ----------

(
    df.write
      .format("delta")
      .mode(write_mode)
      .save(target_path)
)

# COMMAND ----------

silver_df = spark.read.format("delta").load(target_path)

display(silver_df.limit(5))

# COMMAND ----------

print(f"Rows Written : {silver_df.count()}")

# COMMAND ----------

print("=" * 60)
print("Bronze → Silver Completed Successfully")
print("=" * 60)

print(f"Dataset      : {dataset_name}")
print(f"Rows Written : {silver_df.count()}")
print(f"Target Path  : {target_path}")

print("=" * 60)

# COMMAND ----------

