import random
from datetime import datetime
from pathlib import Path

import pandas as pd

from config.employee_config import (
    DESIGNATION_MAPPING,
    SALARY_RANGE,
    FIRST_NAMES,
    LAST_NAMES,
)

# ---------------------------------------
# Load Store Master
# ---------------------------------------

store_df = pd.read_csv("datasets/synthetic/stores/store_master.csv")

employees = []
employee_counter = 1

# Remaining designations after manager
other_designations = [
    "Store Supervisor",
    "Senior Sales Associate",
    "Sales Associate",
    "Sales Associate",
    "Sales Associate",
    "Cashier",
    "Cashier",
    "Inventory Executive",
    "Sales Associate"
]

# ---------------------------------------
# Generate Employees
# ---------------------------------------

for _, store in store_df.iterrows():

    manager_id = f"EMP{employee_counter:04d}"

    salary = random.randint(*SALARY_RANGE["Store Manager"])

    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    employees.append({
        "EmployeeID": manager_id,
        "FirstName": first,
        "LastName": last,
        "Email": f"{first.lower()}.{last.lower()}{employee_counter}@enterpriseretail.com",
        "Department": DESIGNATION_MAPPING["Store Manager"],
        "Designation": "Store Manager",
        "StoreID": store["StoreID"],
        "HireDate": datetime(
            random.randint(2015, 2024),
            random.randint(1, 12),
            random.randint(1, 28)
        ).date(),
        "Salary": salary,
        "ManagerID": None,
        "LastModifiedDate": datetime.now(),
        "IsActive": True
    })

    employee_counter += 1

    # Remaining 9 employees
    for designation in other_designations:

        salary = random.randint(*SALARY_RANGE[designation])

        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        employees.append({
            "EmployeeID": f"EMP{employee_counter:04d}",
            "FirstName": first,
            "LastName": last,
            "Email": f"{first.lower()}.{last.lower()}{employee_counter}@enterpriseretail.com",
            "Department": DESIGNATION_MAPPING[designation],
            "Designation": designation,
            "StoreID": store["StoreID"],
            "HireDate": datetime(
                random.randint(2016, 2025),
                random.randint(1, 12),
                random.randint(1, 28)
            ).date(),
            "Salary": salary,
            "ManagerID": manager_id,
            "LastModifiedDate": datetime.now(),
            "IsActive": True
        })

        employee_counter += 1

# ---------------------------------------
# Save CSV
# ---------------------------------------

employee_df = pd.DataFrame(employees)

output_dir = Path("datasets/synthetic/employees")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "employee_master.csv"

employee_df.to_csv(output_file, index=False)

print("=" * 60)
print("Employee Master Created Successfully")
print("=" * 60)
print(f"Employees Generated : {len(employee_df)}")
print(f"Stores Covered      : {store_df.shape[0]}")
print(f"Saved To            : {output_file}")