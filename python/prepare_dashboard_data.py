import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# --------------------------------------------------
# Load the four datasets
# --------------------------------------------------

customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
order_items = pd.read_csv(DATA_DIR / "order_items.csv")

# Convert date
orders["Order_Date"] = pd.to_datetime(orders["Order_Date"])

# --------------------------------------------------
# Join Order Items → Orders
# --------------------------------------------------

sales = order_items.merge(
    orders,
    on="Order_ID",
    how="left"
)

# --------------------------------------------------
# Join Sales → Products
# --------------------------------------------------

sales = sales.merge(
    products,
    on="Product_ID",
    how="left"
)

# --------------------------------------------------
# Join Sales → Customers
# --------------------------------------------------

sales = sales.merge(
    customers,
    on="Customer_ID",
    how="left"
)

# --------------------------------------------------
# Select useful dashboard columns
# --------------------------------------------------

sales_analysis = sales[
    [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Customer_Name",
        "Customer_Segment",
        "City",
        "State",
        "Region",
        "Product_ID",
        "Product_Name",
        "Category",
        "Sub_Category",
        "Quantity",
        "Discount",
        "Sales",
        "Profit"
    ]
].copy()

# --------------------------------------------------
# Create additional useful metrics
# --------------------------------------------------

sales_analysis["Profit_Margin"] = (
    sales_analysis["Profit"] /
    sales_analysis["Sales"]
).fillna(0)

sales_analysis["Year"] = (
    sales_analysis["Order_Date"].dt.year
)

sales_analysis["Month"] = (
    sales_analysis["Order_Date"].dt.month
)

sales_analysis["Month_Name"] = (
    sales_analysis["Order_Date"].dt.strftime("%B")
)

sales_analysis["Year_Month"] = (
    sales_analysis["Order_Date"].dt.strftime("%Y-%m")
)

# --------------------------------------------------
# Sort data
# --------------------------------------------------

sales_analysis = sales_analysis.sort_values(
    "Order_Date"
)

# --------------------------------------------------
# Save final dashboard dataset
# --------------------------------------------------

output_file = DATA_DIR / "sales_analysis.csv"

sales_analysis.to_csv(
    output_file,
    index=False
)

# --------------------------------------------------
# Display summary
# --------------------------------------------------

print("\n==============================================")
print(" DASHBOARD DATASET CREATED")
print("==============================================")

print(f"\nRows       : {len(sales_analysis):,}")
print(f"Columns    : {len(sales_analysis.columns)}")
print(f"Total Sales: ₹{sales_analysis['Sales'].sum():,.2f}")
print(f"Total Profit: ₹{sales_analysis['Profit'].sum():,.2f}")

print("\nOutput file:")
print(f"  {output_file}")

print("\nDataset preparation completed successfully! 🚀")