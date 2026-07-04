import pandas as pd
from faker import Faker
import random
from datetime import datetime

fake = Faker()

# Load the retail dataset
file_path = "datasets/raw/online_retail_II.xlsx"

df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

sales_df = pd.concat([df_2009, df_2010], ignore_index=True)

# Get unique Customer IDs
customer_ids = (
    sales_df["Customer ID"]
    .dropna()
    .astype(int)
    .unique()
)

loyalty_tiers = ["Bronze", "Silver", "Gold", "Platinum"]

customers = []

for customer_id in customer_ids:
    customers.append({
        "CustomerID": customer_id,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "Email": fake.email(),
        "Phone": fake.phone_number(),
        "Address": fake.street_address(),
        "City": fake.city(),
        "State": fake.state(),
        "Country": "United Kingdom",
        "LoyaltyTier": random.choice(loyalty_tiers),
        "SignupDate": fake.date_between(start_date="-10y", end_date="today"),
        "LastModifiedDate": datetime.now(),
        "IsActive": True
    })

customer_df = pd.DataFrame(customers)

output_path = "datasets/synthetic/customers/customer_master.csv"

customer_df.to_csv(output_path, index=False)

print("=" * 60)
print("Customer Master Created")
print("=" * 60)
print(f"Customers Generated : {len(customer_df)}")
print(f"Saved To : {output_path}")
