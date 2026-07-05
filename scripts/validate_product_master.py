import pandas as pd

print("=" * 60)
print("PRODUCT MASTER VALIDATION")
print("=" * 60)

# Load dataset
file_path = "datasets/synthetic/products/product_master.csv"
df = pd.read_csv(file_path)

# -------------------------------
# Validation Checks
# -------------------------------

total_records = len(df)

duplicate_product_ids = df["ProductID"].duplicated().sum()

missing_product_ids = df["ProductID"].isnull().sum()

missing_product_names = df["ProductName"].isnull().sum()

negative_cost_price = (df["CostPrice"] < 0).sum()

negative_selling_price = (df["SellingPrice"] < 0).sum()

invalid_price = (df["SellingPrice"] < df["CostPrice"]).sum()

null_values = df.isnull().sum().sum()

# -------------------------------
# Print Results
# -------------------------------

print(f"Total Records              : {total_records}")
print(f"Duplicate Product IDs      : {duplicate_product_ids}")
print(f"Missing Product IDs        : {missing_product_ids}")
print(f"Missing Product Names      : {missing_product_names}")
print(f"Negative Cost Price        : {negative_cost_price}")
print(f"Negative Selling Price     : {negative_selling_price}")
print(f"Selling Price < Cost Price : {invalid_price}")
print(f"Total Null Values          : {null_values}")

print("\n" + "=" * 60)

if (
    duplicate_product_ids == 0
    and missing_product_ids == 0
    and missing_product_names == 0
    and negative_cost_price == 0
    and negative_selling_price == 0
    and invalid_price == 0
):
    print("✅ PRODUCT MASTER VALIDATION PASSED")
else:
    print("❌ PRODUCT MASTER VALIDATION FAILED")

print("=" * 60)