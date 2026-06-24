import json
import random
from faker import Faker
from datetime import datetime

fake = Faker('en_IN')

PRODUCTS = [
    {"product_id": "P001", "product_name": "Rice 5kg", "category": "Grocery", "price": 299.0},
    {"product_id": "P002", "product_name": "Surf Excel 1kg", "category": "Household", "price": 189.0},
    {"product_id": "P003", "product_name": "Amul Butter 500g", "category": "Dairy", "price": 275.0},
    {"product_id": "P004", "product_name": "Colgate Toothpaste", "category": "Personal Care", "price": 99.0},
    {"product_id": "P005", "product_name": "Tata Salt 1kg", "category": "Grocery", "price": 24.0},
    {"product_id": "P006", "product_name": "Maggi Noodles", "category": "Instant Food", "price": 14.0},
    {"product_id": "P007", "product_name": "Dettol Soap", "category": "Personal Care", "price": 45.0},
    {"product_id": "P008", "product_name": "Fortune Oil 1L", "category": "Grocery", "price": 180.0},
]

STORES = ["Mumbai_Andheri", "Mumbai_Dadar", "Pune_Kothrud", "Delhi_Connaught", "Bangalore_Indiranagar"]

PAYMENT_METHODS = ["UPI", "Cash", "Credit Card", "Debit Card"]

def generate_event():
    product = random.choice(PRODUCTS)
    quantity = random.randint(1, 5)
    discount = round(random.uniform(0, 0.2), 2)
    unit_price = product["price"]
    total_amount = round(unit_price * quantity * (1 - discount), 2)

    return {
        "order_id": fake.uuid4(),
        "customer_id": f"C{random.randint(1000, 9999)}",
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "customer_phone": fake.phone_number(),
        "store_id": random.choice(STORES),
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "category": product["category"],
        "quantity": quantity,
        "unit_price": unit_price,
        "discount": discount,
        "total_amount": total_amount,
        "payment_method": random.choice(PAYMENT_METHODS),
        "order_status": random.choice(["PLACED", "CONFIRMED", "CANCELLED"]),
        "event_timestamp": datetime.utcnow().isoformat(),
    }