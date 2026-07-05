import pandas as pd

print("=" * 60)
print("EMPLOYEE MASTER VALIDATION")
print("=" * 60)

df = pd.read_csv("datasets/synthetic/employees/employee_master.csv")

duplicate_ids = df["EmployeeID"].duplicated().sum()
missing_ids = df["EmployeeID"].isnull().sum()
missing_store = df["StoreID"].isnull().sum()
missing_name = (df["FirstName"].isnull() | df["LastName"].isnull()).sum()
negative_salary = (df["Salary"] < 0).sum()

manager_count = (df["Designation"] == "Store Manager").sum()

store_counts = df.groupby("StoreID").size()
invalid_store_size = (store_counts != 10).sum()

print(f"Total Employees           : {len(df)}")
print(f"Duplicate Employee IDs    : {duplicate_ids}")
print(f"Missing Employee IDs      : {missing_ids}")
print(f"Missing Names             : {missing_name}")
print(f"Missing Store IDs         : {missing_store}")
print(f"Negative Salaries         : {negative_salary}")
print(f"Store Managers            : {manager_count}")
print(f"Stores not having 10 Emp. : {invalid_store_size}")

print("\n" + "=" * 60)

if (
    duplicate_ids == 0
    and missing_ids == 0
    and missing_store == 0
    and missing_name == 0
    and negative_salary == 0
    and manager_count == 100
    and invalid_store_size == 0
):
    print("✅ EMPLOYEE MASTER VALIDATION PASSED")
else:
    print("❌ EMPLOYEE MASTER VALIDATION FAILED")

print("=" * 60)