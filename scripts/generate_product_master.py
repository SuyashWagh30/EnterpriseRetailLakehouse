import random
from datetime import datetime

import pandas as pd

from config.product_config import (
    BRANDS,
    CATEGORIES,
    SUPPLIERS,
)

# -------------------------------
# Load Online Retail Dataset
# -------------------------------

file_path = "datasets/raw/online_retail_II.xlsx"

df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

sales_df = pd.concat([df_2009, df_2010], ignore_index=True)

# -------------------------------
# Data Cleaning
# -------------------------------

sales_df = sales_df.dropna(subset=["Description"])

# Remove negative prices (returns/corrections)
sales_df = sales_df[sales_df["Price"] > 0]

# -------------------------------
# Create Product Master
# -------------------------------

product_df = (
    sales_df.sort_values("InvoiceDate")
    .groupby("StockCode", as_index=False)
    .agg(
        ProductName=("Description", "last"),
        SellingPrice=("Price", "mean")
    )
)

products = []
for _, row in product_df.iterrows():

    category = random.choice(list(CATEGORIES.keys()))
    subcategory = random.choice(CATEGORIES[category])

    selling_price = round(row["SellingPrice"], 2)

    cost_price = round(
        selling_price * random.uniform(0.70, 0.90),
        2
    )

    products.append({
        "ProductID": row["StockCode"],
        "ProductName": row["ProductName"],
        "Category": category,
        "SubCategory": subcategory,
        "Brand": random.choice(BRANDS),
        "Supplier": random.choice(SUPPLIERS),
        "CostPrice": cost_price,
        "SellingPrice": selling_price,
        "LaunchDate": "2020-01-01",
        "LastModifiedDate": datetime.now(),
        "IsActive": True
    })
final_df = pd.DataFrame(products)

# -------------------------------
# Save Dataset
# -------------------------------

output_path = "datasets/synthetic/products/product_master.csv"

final_df.to_csv(output_path, index=False)

print("=" * 60)
print("Product Master Created Successfully")
print("=" * 60)
print(f"Products Generated : {len(final_df)}")
print(f"Saved To : {output_path}")