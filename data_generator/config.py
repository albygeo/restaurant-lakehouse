#Settings and master data for the synthetic restaurant dataset.

SEED = 42                  # same seed -> same data every run (reproducible)
N_CUSTOMERS = 500
N_HISTORICAL_ORDERS = 8000
HISTORY_DAYS = 180         # orders are spread over the last ~6 months
REVIEW_SHARE = 0.03        # ~3% of completed orders get a review
CANCELLED_SHARE = 0.03     # ~3% of historical orders are cancelled

RESTAURANTS = [
    {"restaurant_id": "REST-AUH-001", "name": "Tandoor House Corniche", "city": "Abu Dhabi",
     "country": "UAE", "address": "Corniche Road, Abu Dhabi", "opening_date": "2022-03-01", "phone": "+971-2-555-0101"},
    {"restaurant_id": "REST-AUH-002", "name": "Tandoor House Khalidiya", "city": "Abu Dhabi",
     "country": "UAE", "address": "Khalidiya Street, Abu Dhabi", "opening_date": "2023-05-15", "phone": "+971-2-555-0102"},
    {"restaurant_id": "REST-DXB-001", "name": "Tandoor House Marina", "city": "Dubai",
     "country": "UAE", "address": "Marina Walk, Dubai", "opening_date": "2021-11-20", "phone": "+971-4-555-0201"},
    {"restaurant_id": "REST-DXB-002", "name": "Tandoor House Deira", "city": "Dubai",
     "country": "UAE", "address": "Al Rigga Road, Dubai", "opening_date": "2023-09-01", "phone": "+971-4-555-0202"},
    {"restaurant_id": "REST-SHJ-001", "name": "Tandoor House Al Majaz", "city": "Sharjah",
     "country": "UAE", "address": "Al Majaz Waterfront, Sharjah", "opening_date": "2024-02-10", "phone": "+971-6-555-0301"},
]

# One shared menu. Each restaurant gets its own price (base price +/- 10%).
MENU = [
    # item_id, name, category, base price (AED), ingredients, vegetarian, spice level
    ("ITEM-101", "Vegetable Samosa (2 pcs)", "Starter", 16, "Potato, Peas, Pastry, Spices", True, "Medium"),
    ("ITEM-102", "Paneer Tikka", "Starter", 34, "Paneer, Yogurt, Peppers, Spices", True, "Medium"),
    ("ITEM-103", "Chicken 65", "Starter", 36, "Chicken, Curry Leaves, Chilli", False, "Hot"),
    ("ITEM-104", "Onion Bhaji", "Starter", 18, "Onion, Gram Flour, Spices", True, "Mild"),
    ("ITEM-201", "Butter Chicken", "Main Course", 52, "Chicken, Tomato, Butter, Cream", False, "Mild"),
    ("ITEM-202", "Lamb Rogan Josh", "Main Course", 62, "Lamb, Yogurt, Kashmiri Chilli", False, "Medium"),
    ("ITEM-203", "Palak Paneer", "Main Course", 42, "Spinach, Paneer, Garlic", True, "Mild"),
    ("ITEM-204", "Chana Masala", "Main Course", 36, "Chickpeas, Tomato, Onion, Spices", True, "Medium"),
    ("ITEM-205", "Prawn Malabar Curry", "Main Course", 68, "Prawns, Coconut, Tamarind", False, "Medium"),
    ("ITEM-206", "Dal Makhani", "Main Course", 38, "Black Lentils, Butter, Cream", True, "Mild"),
    ("ITEM-301", "Chicken Biryani", "Rice", 48, "Basmati Rice, Chicken, Saffron", False, "Medium"),
    ("ITEM-302", "Vegetable Biryani", "Rice", 40, "Basmati Rice, Vegetables, Saffron", True, "Medium"),
    ("ITEM-303", "Jeera Rice", "Rice", 18, "Basmati Rice, Cumin", True, "None"),
    ("ITEM-401", "Butter Naan", "Bread", 9, "Flour, Butter", True, "None"),
    ("ITEM-402", "Garlic Naan", "Bread", 11, "Flour, Garlic, Butter", True, "None"),
    ("ITEM-403", "Tandoori Roti", "Bread", 7, "Whole Wheat Flour", True, "None"),
    ("ITEM-501", "Gulab Jamun", "Dessert", 18, "Milk Solids, Sugar Syrup, Cardamom", True, "None"),
    ("ITEM-502", "Mango Kulfi", "Dessert", 20, "Milk, Mango, Pistachio", True, "None"),
    ("ITEM-601", "Mango Lassi", "Beverage", 16, "Yogurt, Mango", True, "None"),
    ("ITEM-602", "Masala Chai", "Beverage", 10, "Tea, Milk, Spices", True, "None"),
    ("ITEM-603", "Fresh Lime Soda", "Beverage", 12, "Lime, Soda, Sugar", True, "None"),
]

ORDER_TYPES = {"dine_in": 45, "takeaway": 25, "delivery": 30}        # relative weights
PAYMENT_METHODS = {"card": 55, "wallet": 30, "cash": 15}
# Lunch and dinner peaks; restaurants open 11:00-23:59
HOUR_WEIGHTS = {11: 3, 12: 8, 13: 9, 14: 5, 15: 2, 16: 2, 17: 3,
                18: 5, 19: 9, 20: 10, 21: 8, 22: 4, 23: 2}
WEEKEND_BOOST = 1.4        # Fri/Sat are busier (UAE weekend)
SAME_CITY_SHARE = 0.75     # customers usually order in their own city
