import pandas as pd

print("=" * 60)
print("INVENTORY MASTER VALIDATION")
print("=" * 60)

inventory = pd.read_csv("datasets/synthetic/inventory/inventory_master.csv")
stores = pd.read_csv("datasets/synthetic/stores/store_master.csv")
products = pd.read_csv("datasets/synthetic/products/product_master.csv")

duplicate_inventory = inventory["InventoryID"].duplicated().sum()

missing_inventory = inventory["InventoryID"].isnull().sum()

missing_store = inventory["StoreID"].isnull().sum()

missing_product = inventory["ProductID"].isnull().sum()

negative_stock = (inventory["CurrentStock"] < 0).sum()

invalid_reorder = (
    inventory["ReorderLevel"] >= inventory["MaximumStock"]
).sum()

invalid_store_fk = (
    ~inventory["StoreID"].isin(stores["StoreID"])
).sum()

invalid_product_fk = (
    ~inventory["ProductID"].isin(products["ProductID"])
).sum()

print(f"Total Inventory Records      : {len(inventory)}")
print(f"Duplicate Inventory IDs      : {duplicate_inventory}")
print(f"Missing Inventory IDs        : {missing_inventory}")
print(f"Missing Store IDs            : {missing_store}")
print(f"Missing Product IDs          : {missing_product}")
print(f"Negative Stock               : {negative_stock}")
print(f"Invalid Reorder Levels       : {invalid_reorder}")
print(f"Invalid Store Foreign Keys   : {invalid_store_fk}")
print(f"Invalid Product Foreign Keys : {invalid_product_fk}")

print("\n" + "=" * 60)

if (
    duplicate_inventory == 0
    and missing_inventory == 0
    and missing_store == 0
    and missing_product == 0
    and negative_stock == 0
    and invalid_reorder == 0
    and invalid_store_fk == 0
    and invalid_product_fk == 0
):
    print("✅ INVENTORY MASTER VALIDATION PASSED")
else:
    print("❌ INVENTORY MASTER VALIDATION FAILED")

print("=" * 60)