"""Orders. build_order() is reused in Phase 2 for the live Event Hubs stream."""
import json
import random
from datetime import date, datetime, timedelta

import pandas as pd

from config import (CANCELLED_SHARE, HOUR_WEIGHTS, ORDER_TYPES, PAYMENT_METHODS,
                    SAME_CITY_SHARE, WEEKEND_BOOST)


def weighted_choice(rng: random.Random, weights: dict):
    return rng.choices(list(weights), weights=list(weights.values()))[0]


def build_order(rng, order_id, ts, restaurant_id, customer_id, menu, status="completed") -> dict:
    """One order. `menu` = list of menu-item dicts for this restaurant."""
    dishes = rng.sample(menu, k=rng.randint(1, 5))
    items = []
    for dish in dishes:
        qty = rng.choices([1, 2, 3], weights=[70, 22, 8])[0]
        items.append({
            "item_id": dish["item_id"],
            "name": dish["name"],
            "category": dish["category"],
            "quantity": qty,
            "unit_price": float(dish["price"]),
            "subtotal": round(qty * float(dish["price"]), 2),
        })
    return {
        "order_id": order_id,
        "order_timestamp": ts.isoformat(timespec="seconds"),
        "restaurant_id": restaurant_id,
        "customer_id": customer_id,
        "order_type": weighted_choice(rng, ORDER_TYPES),
        "items": json.dumps(items),          # JSON array stored as text, like many real APIs
        "total_amount": round(sum(i["subtotal"] for i in items), 2),
        "payment_method": weighted_choice(rng, PAYMENT_METHODS),
        "order_status": status,
    }


def random_timestamp(rng, days):
    # Fri (4) and Sat (5) are the UAE weekend
    day_weights = [WEEKEND_BOOST if d.weekday() in (4, 5) else 1.0 for d in days]
    day = rng.choices(days, weights=day_weights)[0]
    hour = weighted_choice(rng, HOUR_WEIGHTS)
    return datetime(day.year, day.month, day.day, hour, rng.randint(0, 59), rng.randint(0, 59))


def make_historical_orders(rng, restaurants, customers, menu_items, n, history_days, end=None):
    end = end or date.today() - timedelta(days=1)
    days = [end - timedelta(days=d) for d in range(history_days)]
    menu_by_restaurant = {rid: grp.to_dict("records") for rid, grp in menu_items.groupby("restaurant_id")}
    by_city = restaurants.groupby("city")["restaurant_id"].apply(list).to_dict()
    all_restaurants = restaurants["restaurant_id"].tolist()
    customer_rows = customers[["customer_id", "city"]].to_dict("records")

    # draw timestamps first and sort them, so order IDs increase with time
    timestamps = sorted(random_timestamp(rng, days) for _ in range(n))
    orders = []
    for i, ts in enumerate(timestamps, start=1):
        customer = rng.choice(customer_rows)
        if rng.random() < SAME_CITY_SHARE:
            restaurant_id = rng.choice(by_city[customer["city"]])
        else:
            restaurant_id = rng.choice(all_restaurants)
        status = "cancelled" if rng.random() < CANCELLED_SHARE else "completed"
        orders.append(build_order(rng, f"ORD-H{i:07d}", ts, restaurant_id,
                                  customer["customer_id"], menu_by_restaurant[restaurant_id], status))
    return pd.DataFrame(orders)
