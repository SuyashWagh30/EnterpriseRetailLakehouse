import pandas as pd

# File path
file_path = "datasets/raw/online_retail_II.xlsx"

# Read both sheets
df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

# Combine both years
df = pd.concat([df_2009, df_2010], ignore_index=True)

print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print(df.shape)

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)
print(df.columns.tolist())

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isnull().sum())

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)
print(df.duplicated().sum())

print("\n" + "=" * 60)
print("NEGATIVE QUANTITY")
print("=" * 60)
print((df["Quantity"] < 0).sum())

print("\n" + "=" * 60)
print("NEGATIVE PRICE")
print("=" * 60)
print((df["Price"] < 0).sum())

print("\n" + "=" * 60)
print("CANCELLED ORDERS")
print("=" * 60)
print(df["Invoice"].astype(str).str.startswith("C").sum())

print("\n" + "=" * 60)
print("UNIQUE CUSTOMERS")
print("=" * 60)
print(df["Customer ID"].nunique())

print("\n" + "=" * 60)
print("UNIQUE PRODUCTS")
print("=" * 60)
print(df["StockCode"].nunique())