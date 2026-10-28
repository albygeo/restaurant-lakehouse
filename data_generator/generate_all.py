"""Generate all CSV files into data_generator/data/.

Run from the repo root:  python data_generator/generate_all.py
"""
import random
from pathlib import Path

from faker import Faker

from config import HISTORY_DAYS, N_CUSTOMERS, N_HISTORICAL_ORDERS, REVIEW_SHARE, SEED
from master_data import make_customers, make_menu_items, make_restaurants
from orders import make_historical_orders
from reviews import make_reviews

OUT = Path(__file__).parent / "data"


def main():
    rng = random.Random(SEED)
    Faker.seed(SEED)
    fake = Faker()

    restaurants = make_restaurants()
    menu_items = make_menu_items(rng)
    customers = make_customers(rng, fake, N_CUSTOMERS)
    orders = make_historical_orders(rng, restaurants, customers, menu_items,
                                    N_HISTORICAL_ORDERS, HISTORY_DAYS)
    reviews, review_labels = make_reviews(rng, orders, REVIEW_SHARE)

    OUT.mkdir(exist_ok=True)
    tables = {"restaurants": restaurants, "menu_items": menu_items, "customers": customers,
              "historical_orders": orders, "reviews": reviews, "review_labels": review_labels}
    for name, df in tables.items():
        df.to_csv(OUT / f"{name}.csv", index=False)
        print(f"{name:<18} {len(df):>6} rows")
    print(f"\nWritten to {OUT}")


if __name__ == "__main__":
    main()
