# data_gen/generate_data.py

import csv
import random
from datetime import datetime, timedelta
import uuid
import os

# Make sure output folder exists
os.makedirs("output", exist_ok=True)

# Categories for sample products
categories = ["Beverages", "Snacks", "Household", "Electronics", "Clothing"]

# Create product list
def make_products(n=20):
    products = []
    for i in range(n):
        sku = f"P{i+1000}"
        name = f"Product {i+1}"
        category = random.choice(categories)
        quality = random.randint(1, 10)
        price = round(5 + quality * random.uniform(0.8, 2.5), 2)
        products.append((sku, name, category, quality, price))
    return products

# Create customer list
def make_customers(n=50):
    customers = []
    for i in range(n):
        name = f"Customer {i+1}"
        has_loyalty = random.random() < 0.4  # 40% loyalty members
        customers.append((str(uuid.uuid4()), name, has_loyalty))
    return customers

# Create transaction list
def make_transactions(products, customers, days=60, tx_per_day_avg=30):
    tx = []
    start = datetime.now() - timedelta(days=days)
    for d in range(days):
        day = start + timedelta(days=d)
        count = max(5, int(random.gauss(tx_per_day_avg, tx_per_day_avg * 0.3)))
        for _ in range(count):
            product = random.choice(products)
            customer = random.choice(customers)
            qty = random.choice([1, 2, 3])
            price = round(product[4] * random.uniform(0.9, 1.05), 2)
            timestamp = day + timedelta(seconds=random.randint(0, 86400))

            pc_points = 0
            if customer[2]:  # loyalty member
                pc_points = int(price * qty * (product[3] / 10))

            tx.append((product[0], customer[0], timestamp.isoformat(), qty, price, pc_points))
    return tx

# Generate the data
products = make_products(25)
customers = make_customers(80)
transactions = make_transactions(products, customers)

# Write CSV files
with open("output/products.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sku", "name", "category", "quality", "price"])
    writer.writerows(products)

with open("output/customers.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["customer_uuid", "name", "has_loyalty"])
    writer.writerows(customers)

with open("output/transactions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sku", "customer_uuid", "sale_ts", "quantity", "unit_price", "pc_points"])
    writer.writerows(transactions)

print("Data generated successfully into data_gen/output/")
