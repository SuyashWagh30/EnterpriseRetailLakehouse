import random
from datetime import datetime
from pathlib import Path

import pandas as pd

from config.store_config import STORE_TYPES, INDIAN_LOCATIONS

# --------------------------------------------------
# Configuration
# --------------------------------------------------

NUM_STORES = 100

# --------------------------------------------------
# Generate Store Master
# --------------------------------------------------

stores = []

for i in range(1, NUM_STORES + 1):

    city, state, region = random.choice(INDIAN_LOCATIONS)

    stores.append({
        "StoreID": f"STR{i:04d}",
        "StoreName": f"{city} Store {i}",
        "City": city,
        "State": state,
        "Region": region,
        "Country": "India",
        "StoreType": random.choice(STORE_TYPES),
        "OpenDate": datetime(
            random.randint(2015, 2024),
            random.randint(1, 12),
            random.randint(1, 28)
        ).date(),
        "ManagerID": f"EMP{i:04d}",
        "LastModifiedDate": datetime.now(),
        "IsActive": True
    })

# --------------------------------------------------
# Save Dataset
# --------------------------------------------------

store_df = pd.DataFrame(stores)

output_dir = Path("datasets/synthetic/stores")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "store_master.csv"

store_df.to_csv(output_file, index=False)

print("=" * 60)
print("Store Master Created Successfully")
print("=" * 60)
print(f"Stores Generated : {len(store_df)}")
print(f"Saved To : {output_file}")