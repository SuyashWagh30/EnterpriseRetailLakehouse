import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from config.inventory_config import (
    MIN_PRODUCTS_PER_STORE,
    CURRENT_STOCK_RANGE,
    REORDER_LEVEL_RANGE,
    MAX_STOCK_RANGE,
)


# --------------------------------------------------
# Load Source Data
# --------------------------------------------------

def load_products():
    return pd.read_csv(
        "datasets/synthetic/products/product_master.csv"
    )


def load_stores():
    return pd.read_csv(
        "datasets/synthetic/stores/store_master.csv"
    )


# --------------------------------------------------
# Generate Inventory
# --------------------------------------------------

def generate_inventory(store_df, product_df):

    inventory = []
    inventory_id = 1

    for _, store in store_df.iterrows():

        sampled_products = product_df.sample(
            n=MIN_PRODUCTS_PER_STORE,
            random_state=None
        )

        for _, product in sampled_products.iterrows():

            reorder = random.randint(*REORDER_LEVEL_RANGE)

            maximum = random.randint(
                max(reorder + 50, MAX_STOCK_RANGE[0]),
                MAX_STOCK_RANGE[1]
            )

            current = random.randint(
                CURRENT_STOCK_RANGE[0],
                maximum
            )

            inventory.append({

                "InventoryID": f"INV{inventory_id:06d}",

                "StoreID": store["StoreID"],

                "ProductID": product["ProductID"],

                "CurrentStock": current,

                "ReorderLevel": reorder,

                "MaximumStock": maximum,

                "LastRestockedDate":
                    (
                        datetime.today()
                        - timedelta(days=random.randint(0, 180))
                    ).date(),

                "LastModifiedDate": datetime.now(),

                "IsActive": True

            })

            inventory_id += 1

    return pd.DataFrame(inventory)


# --------------------------------------------------
# Save Dataset
# --------------------------------------------------

def save_inventory(df):

    output_dir = Path("datasets/synthetic/inventory")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "inventory_master.csv"

    df.to_csv(output_file, index=False)

    print("=" * 60)
    print("Inventory Master Created Successfully")
    print("=" * 60)
    print(f"Inventory Records : {len(df)}")
    print(f"Saved To          : {output_file}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    products = load_products()

    stores = load_stores()

    inventory = generate_inventory(
        stores,
        products
    )

    save_inventory(inventory)


if __name__ == "__main__":
    main()