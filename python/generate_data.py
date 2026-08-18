import pandas as pd
import numpy as np
import random
from pathlib import Path

# ============================================================
# E-COMMERCE POWER BI PROJECT - DATA GENERATOR
# ============================================================

# Reproducibility
random.seed(42)
np.random.seed(42)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# 1. CUSTOMERS
# ------------------------------------------------------------

first_names = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rahul",
    "Rohan", "Vikram", "Karan", "Ananya", "Aisha",
    "Priya", "Neha", "Sneha", "Kavya", "Isha",
    "Meera", "Zoya", "Sara", "Riya", "Diya"
]

last_names = [
    "Sharma", "Verma", "Reddy", "Patel", "Khan",
    "Gupta", "Singh", "Kumar", "Rao", "Mehta",
    "Joshi", "Malik", "Das", "Nair", "Iyer"
]

cities = {
    "Hyderabad": ("Telangana", "South"),
    "Bengaluru": ("Karnataka", "South"),
    "Chennai": ("Tamil Nadu", "South"),
    "Mumbai": ("Maharashtra", "West"),
    "Pune": ("Maharashtra", "West"),
    "Ahmedabad": ("Gujarat", "West"),
    "Delhi": ("Delhi", "North"),
    "Jaipur": ("Rajasthan", "North"),
    "Lucknow": ("Uttar Pradesh", "North"),
    "Kolkata": ("West Bengal", "East"),
    "Bhubaneswar": ("Odisha", "East"),
    "Patna": ("Bihar", "East")
}

num_customers = 1200

customer_records = []

for i in range(1, num_customers + 1):

    first = random.choice(first_names)
    last = random.choice(last_names)

    city = random.choice(list(cities.keys()))
    state, region = cities[city]

    customer_records.append({
        "Customer_ID": f"CUST{i:05d}",
        "Customer_Name": f"{first} {last}",
        "City": city,
        "State": state,
        "Region": region,
        "Customer_Segment": random.choice(
            ["Consumer", "Corporate", "Small Business"]
        )
    })

customers = pd.DataFrame(customer_records)

# ------------------------------------------------------------
# 2. PRODUCTS
# ------------------------------------------------------------

product_catalog = [
    ("Laptop Pro 14", "Electronics", "Computers", 85000, 68000),
    ("Laptop Air 13", "Electronics", "Computers", 65000, 51000),
    ("Gaming Laptop X", "Electronics", "Computers", 105000, 85000),
    ("Wireless Mouse", "Electronics", "Accessories", 1200, 650),
    ("Mechanical Keyboard", "Electronics", "Accessories", 4500, 2700),
    ("USB-C Hub", "Electronics", "Accessories", 2200, 1200),
    ("27-inch Monitor", "Electronics", "Monitors", 22000, 15500),
    ("24-inch Monitor", "Electronics", "Monitors", 15000, 10500),
    ("Smartphone Pro", "Electronics", "Mobiles", 55000, 42000),
    ("Smartphone Lite", "Electronics", "Mobiles", 22000, 16000),

    ("Office Chair", "Furniture", "Chairs", 12000, 7500),
    ("Ergonomic Chair", "Furniture", "Chairs", 18000, 11000),
    ("Office Desk", "Furniture", "Tables", 16000, 10000),
    ("Standing Desk", "Furniture", "Tables", 28000, 19000),
    ("Bookshelf", "Furniture", "Storage", 8500, 5000),
    ("Filing Cabinet", "Furniture", "Storage", 7000, 4200),

    ("Notebook Pack", "Office Supplies", "Paper", 450, 220),
    ("Premium Notebook", "Office Supplies", "Paper", 650, 330),
    ("Printer", "Office Supplies", "Machines", 15000, 10500),
    ("Laser Printer", "Office Supplies", "Machines", 24000, 17000),
    ("Printer Ink", "Office Supplies", "Supplies", 1800, 950),
    ("Desk Organizer", "Office Supplies", "Accessories", 900, 450),

    ("Backpack", "Accessories", "Bags", 2500, 1300),
    ("Laptop Backpack", "Accessories", "Bags", 4200, 2200),
    ("Travel Bag", "Accessories", "Bags", 3500, 1800),
    ("Wireless Earbuds", "Accessories", "Audio", 5500, 3200),
    ("Bluetooth Speaker", "Accessories", "Audio", 6500, 3900),
    ("Power Bank", "Accessories", "Mobile Accessories", 1800, 950)
]

product_records = []

for i, product in enumerate(product_catalog, start=1):

    name, category, subcategory, price, cost = product

    product_records.append({
        "Product_ID": f"PROD{i:04d}",
        "Product_Name": name,
        "Category": category,
        "Sub_Category": subcategory,
        "Unit_Price": price,
        "Unit_Cost": cost
    })

products = pd.DataFrame(product_records)

# ------------------------------------------------------------
# 3. ORDERS
# ------------------------------------------------------------

num_orders = 10000

date_range = pd.date_range(
    start="2024-01-01",
    end="2025-12-31",
    freq="D"
)

order_records = []

for i in range(1, num_orders + 1):

    order_date = random.choice(date_range)

    customer_id = random.choice(
        customers["Customer_ID"].tolist()
    )

    order_records.append({
        "Order_ID": f"ORD{i:06d}",
        "Order_Date": order_date,
        "Customer_ID": customer_id
    })

orders = pd.DataFrame(order_records)

# ------------------------------------------------------------
# 4. ORDER ITEMS
# ------------------------------------------------------------

order_item_records = []

for _, order in orders.iterrows():

    # Most orders contain 1-3 products
    number_of_products = random.choices(
        [1, 2, 3, 4],
        weights=[55, 30, 12, 3]
    )[0]

    selected_products = random.sample(
        products["Product_ID"].tolist(),
        number_of_products
    )

    for product_id in selected_products:

        product = products[
            products["Product_ID"] == product_id
        ].iloc[0]

        quantity = random.choices(
            [1, 2, 3, 4, 5],
            weights=[55, 25, 12, 6, 2]
        )[0]

        discount = random.choice(
            [0, 0, 0, 0.05, 0.10, 0.15, 0.20]
        )

        gross_sales = product["Unit_Price"] * quantity

        discount_amount = gross_sales * discount

        sales = gross_sales - discount_amount

        cost = product["Unit_Cost"] * quantity

        profit = sales - cost

        order_item_records.append({
            "Order_ID": order["Order_ID"],
            "Product_ID": product_id,
            "Quantity": quantity,
            "Discount": discount,
            "Sales": round(sales, 2),
            "Profit": round(profit, 2)
        })

order_items = pd.DataFrame(order_item_records)

# ------------------------------------------------------------
# 5. SAVE DATA
# ------------------------------------------------------------

customers.to_csv(
    DATA_DIR / "customers.csv",
    index=False
)

products.to_csv(
    DATA_DIR / "products.csv",
    index=False
)

orders.to_csv(
    DATA_DIR / "orders.csv",
    index=False
)

order_items.to_csv(
    DATA_DIR / "order_items.csv",
    index=False
)

# ------------------------------------------------------------
# 6. SUMMARY
# ------------------------------------------------------------

print("\n==============================================")
print(" E-COMMERCE POWER BI DATASET GENERATED")
print("==============================================")

print(f"\nCustomers : {len(customers):,}")
print(f"Products  : {len(products):,}")
print(f"Orders    : {len(orders):,}")
print(f"Line Items: {len(order_items):,}")

print("\nFiles created:")

print("  data/customers.csv")
print("  data/products.csv")
print("  data/orders.csv")
print("  data/order_items.csv")

print("\nDataset generation completed successfully! 🚀")