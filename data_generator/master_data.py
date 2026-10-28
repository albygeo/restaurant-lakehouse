"""Restaurants, menu items and customers: the slowly changing 'master' data."""
import random

import pandas as pd
from faker import Faker

from config import MENU, RESTAURANTS


def make_restaurants() -> pd.DataFrame:
    return pd.DataFrame(RESTAURANTS)


def make_menu_items(rng: random.Random) -> pd.DataFrame:
    rows = []
    for restaurant in RESTAURANTS:
        for item_id, name, category, base_price, ingredients, is_veg, spice in MENU:
            rows.append({
                "restaurant_id": restaurant["restaurant_id"],
                "item_id": item_id,
                "name": name,
                "category": category,
                "price": round(base_price * rng.uniform(0.9, 1.1), 2),
                "ingredients": ingredients,
                "is_vegetarian": is_veg,
                "spice_level": spice,
            })
    return pd.DataFrame(rows)


def make_customers(rng: random.Random, fake: Faker, n: int) -> pd.DataFrame:
    cities = sorted({r["city"] for r in RESTAURANTS})
    rows = []
    for i in range(n):
        rows.append({
            "customer_id": f"CUST-{10000 + i}",
            "name": fake.name(),
            "email": fake.unique.email(),
            "phone": f"+9715{rng.randint(0, 8)}{rng.randint(1_000_000, 9_999_999)}",
            "city": rng.choice(cities),
            # everyone joined before the order history starts
            "join_date": fake.date_between(start_date="-3y", end_date="-200d").isoformat(),
        })
    return pd.DataFrame(rows)
