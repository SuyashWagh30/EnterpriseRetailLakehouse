from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()

NUM_CUSTOMERS = 50000

customers = []

loyalty_tiers = ["Bronze", "Silver", "Gold", "Platinum"]

for customer_id in range(1, NUM_CUSTOMERS + 1):

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

df = pd.DataFrame(customers)

output_path = "datasets/synthetic/customers/customer_master.csv"

df.to_csv(output_path, index=False)

print("=" * 60)
print("Customer Master Dataset Created Successfully")
print("=" * 60)
print(f"Total Customers : {len(df)}")
print(f"Saved To : {output_path}")