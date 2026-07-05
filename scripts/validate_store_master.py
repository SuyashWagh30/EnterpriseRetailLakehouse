import pandas as pd

print("=" * 60)
print("STORE MASTER VALIDATION")
print("=" * 60)

df = pd.read_csv("datasets/synthetic/stores/store_master.csv")

duplicate_store_ids = df["StoreID"].duplicated().sum()
missing_store_ids = df["StoreID"].isnull().sum()
missing_store_names = df["StoreName"].isnull().sum()
missing_city = df["City"].isnull().sum()
missing_state = df["State"].isnull().sum()
missing_region = df["Region"].isnull().sum()
missing_manager = df["ManagerID"].isnull().sum()

print(f"Total Records         : {len(df)}")
print(f"Duplicate Store IDs   : {duplicate_store_ids}")
print(f"Missing Store IDs     : {missing_store_ids}")
print(f"Missing Store Names   : {missing_store_names}")
print(f"Missing Cities        : {missing_city}")
print(f"Missing States        : {missing_state}")
print(f"Missing Regions       : {missing_region}")
print(f"Missing Manager IDs   : {missing_manager}")

print("\n" + "=" * 60)

if (
    duplicate_store_ids == 0
    and missing_store_ids == 0
    and missing_store_names == 0
    and missing_city == 0
    and missing_state == 0
    and missing_region == 0
    and missing_manager == 0
):
    print("✅ STORE MASTER VALIDATION PASSED")
else:
    print("❌ STORE MASTER VALIDATION FAILED")

print("=" * 60)