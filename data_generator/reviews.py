"""Customer reviews whose text matches the rating and contains known issues.

We also return the 'true' labels (sentiment + issues) in a separate table. They are NOT
loaded into Azure SQL: we can compare them with what the LLM detects,
which gives you a real accuracy number for your README.
"""
import json
import random
from datetime import datetime, timedelta

import pandas as pd

RATING_WEIGHTS = {5: 35, 4: 30, 3: 15, 2: 12, 1: 8}

POSITIVE = ["Loved the {dish}, full of flavour.",
            "Great evening, the {dish} was spot on.",
            "Really good {dish} and friendly staff.",
            "The {dish} tasted just like home."]
NEUTRAL = ["The {dish} was okay, nothing special.",
           "Decent meal overall, the {dish} was fine."]
NEGATIVE = ["Disappointed with this order.",
            "Not what I expected from this place."]
ISSUES = {
    "delivery": ["The delivery arrived almost an hour late.",
                 "The rider took ages and the bag was barely warm."],
    "food_quality": ["The {dish} was bland and overcooked.",
                     "The {dish} did not taste fresh."],
    "pricing": ["Far too expensive for what you get.",
                "Prices have gone up a lot since my last visit."],
    "portion_size": ["The portion was tiny.",
                     "Very small portion, I was still hungry afterwards."],
}
CLOSERS = {"positive": ["Will order again!", "Highly recommended."],
           "neutral": ["Might try something else next time.", ""],
           "negative": ["Not coming back soon.", "Please fix this."]}


def sentiment_for(rating: int) -> str:
    return "positive" if rating >= 4 else "neutral" if rating == 3 else "negative"


def write_review(rng, rating, dish, order_type):
    sentiment = sentiment_for(rating)
    issues = []
    if sentiment != "positive":
        candidates = list(ISSUES)
        if order_type != "delivery":
            candidates.remove("delivery")       # no delivery complaints for dine-in orders
        issues = rng.sample(candidates, k=1 if rating == 3 else rng.randint(1, 2))
    if sentiment == "positive":
        parts = [rng.choice(POSITIVE)]
    elif sentiment == "neutral":
        parts = [rng.choice(NEUTRAL)]
    else:
        parts = [rng.choice(NEGATIVE)]
    parts += [rng.choice(ISSUES[i]) for i in issues]
    parts.append(rng.choice(CLOSERS[sentiment]))
    text = " ".join(p for p in parts if p).format(dish=dish)
    return text, sentiment, issues


def make_reviews(rng, orders: pd.DataFrame, share: float, now=None):
    now = now or datetime.now()
    completed = orders[orders["order_status"] == "completed"]
    reviews, labels = [], []
    for order in completed.itertuples():
        if rng.random() >= share:
            continue
        rating = rng.choices(list(RATING_WEIGHTS), weights=list(RATING_WEIGHTS.values()))[0]
        dish = rng.choice(json.loads(order.items))["name"]
        text, sentiment, issues = write_review(rng, rating, dish, order.order_type)
        ordered_at = datetime.fromisoformat(order.order_timestamp)
        reviewed_at = min(ordered_at + timedelta(hours=rng.randint(1, 72)), now)
        review_id = f"REV-{len(reviews) + 1:06d}"
        reviews.append({
            "review_id": review_id,
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "restaurant_id": order.restaurant_id,
            "review_text": text,
            "rating": rating,
            "review_timestamp": reviewed_at.isoformat(timespec="seconds"),
        })
        labels.append({"review_id": review_id, "true_sentiment": sentiment,
                        "true_issues": ",".join(issues)})
    return pd.DataFrame(reviews), pd.DataFrame(labels)
