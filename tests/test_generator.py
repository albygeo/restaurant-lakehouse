"""Checks that the synthetic data is internally consistent. Run: pytest"""
import json
import random

import pytest
from faker import Faker

from master_data import make_customers, make_menu_items, make_restaurants
from orders import make_historical_orders
from reviews import make_reviews


@pytest.fixture(scope="module")
def data():
    rng = random.Random(1)
    Faker.seed(1)
    fake = Faker()
    restaurants = make_restaurants()
    menu = make_menu_items(rng)
    customers = make_customers(rng, fake, 100)
    orders = make_historical_orders(rng, restaurants, customers, menu, 1000, 60)
    reviews, labels = make_reviews(rng, orders, 0.2)
    return restaurants, menu, customers, orders, reviews, labels


def test_ids_are_unique(data):
    restaurants, menu, customers, orders, reviews, _ = data
    assert restaurants["restaurant_id"].is_unique
    assert customers["customer_id"].is_unique
    assert orders["order_id"].is_unique
    assert reviews["review_id"].is_unique
    assert not menu.duplicated(["restaurant_id", "item_id"]).any()


def test_orders_reference_existing_customers_and_restaurants(data):
    restaurants, _, customers, orders, _, _ = data
    assert orders["customer_id"].isin(customers["customer_id"]).all()
    assert orders["restaurant_id"].isin(restaurants["restaurant_id"]).all()


def test_total_equals_sum_of_items(data):
    orders = data[3]
    for row in orders.itertuples():
        items = json.loads(row.items)
        assert 1 <= len(items) <= 5
        assert abs(sum(i["subtotal"] for i in items) - row.total_amount) < 0.01


def test_items_come_from_that_restaurants_menu(data):
    _, menu, _, orders, _, _ = data
    valid = set(zip(menu["restaurant_id"], menu["item_id"]))
    for row in orders.itertuples():
        for item in json.loads(row.items):
            assert (row.restaurant_id, item["item_id"]) in valid


def test_reviews_only_for_completed_orders_and_after_ordering(data):
    orders, reviews = data[3], data[4]
    merged = reviews.merge(orders, on="order_id", suffixes=("", "_order"))
    assert len(merged) == len(reviews)
    assert (merged["order_status"] == "completed").all()
    assert (merged["review_timestamp"] >= merged["order_timestamp"]).all()
    assert (merged["customer_id"] == merged["customer_id_order"]).all()


def test_no_delivery_complaints_on_non_delivery_orders(data):
    orders, reviews, labels = data[3], data[4], data[5]
    merged = labels.merge(reviews, on="review_id").merge(orders, on="order_id")
    non_delivery = merged[merged["order_type"] != "delivery"]
    assert not non_delivery["true_issues"].str.contains("delivery").any()
