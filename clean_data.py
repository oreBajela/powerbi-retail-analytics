"""
clean_data.py
─────────────
Replicates Power Query transformations in Python.
Outputs a merged, analysis-ready CSV for Power BI or further analysis.

Run: python clean_data.py
Requires: pandas  (pip install pandas)
"""

import pandas as pd


def load_data():
    sales = pd.read_csv("data/sales.csv")
    customers = pd.read_csv("data/customers.csv")
    products = pd.read_csv("data/products.csv")
    return sales, customers, products


def clean_sales(sales):
    # Data type casting (Power Query: "Change Type")
    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])
    sales["Quantity"] = sales["Quantity"].astype(int)
    sales["UnitPrice"] = sales["UnitPrice"].astype(float)
    sales["Discount"] = sales["Discount"].astype(float)

    # Calculated columns (Power Query: "Add Custom Column")
    sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"] * (1 - sales["Discount"])
    sales["Month"] = sales["OrderDate"].dt.month_name()
    sales["MonthNum"] = sales["OrderDate"].dt.month   # for sorting
    sales["Year"] = sales["OrderDate"].dt.year
    sales["Quarter"] = "Q" + sales["OrderDate"].dt.quarter.astype(str)

    return sales


def clean_customers(customers):
    # Merge columns (Power Query: "Merge Columns")
    customers["FullName"] = customers["FirstName"] + " " + customers["LastName"]
    customers["JoinDate"] = pd.to_datetime(customers["JoinDate"])
    customers["JoinYear"] = customers["JoinDate"].dt.year
    return customers


def clean_products(products):
    # Conditional column (Power Query: "Add Conditional Column")
    def price_tier(cost):
        if cost < 20:
            return "Budget"
        elif cost < 80:
            return "Mid-range"
        else:
            return "Premium"

    products["PriceCategory"] = products["CostPrice"].apply(price_tier)
    return products


def merge_and_enrich(sales, customers, products):
    # Table joins (Power Query: "Merge Queries")
    merged = (
        sales
        .merge(customers[["CustomerID", "FullName", "Segment", "JoinYear"]], on="CustomerID")
        .merge(products[["ProductID", "ProductName", "Category", "CostPrice", "PriceCategory"]], on="ProductID")
    )

    # Profit calculation
    merged["Profit"] = merged["Revenue"] - (merged["CostPrice"] * merged["Quantity"])
    merged["ProfitMargin"] = merged["Profit"] / merged["Revenue"]

    return merged


def summarize(merged):
    print("\n" + "="*50)
    print("  RETAIL ANALYTICS — DATA SUMMARY")
    print("="*50)
    print(f"  Total transactions : {len(merged):,}")
    print(f"  Unique customers   : {merged['CustomerID'].nunique()}")
    print(f"  Total revenue      : ${merged['Revenue'].sum():,.2f}")
    print(f"  Total profit       : ${merged['Profit'].sum():,.2f}")
    print(f"  Avg profit margin  : {merged['ProfitMargin'].mean()*100:.1f}%")
    print(f"  Date range         : {merged['OrderDate'].min().date()} → {merged['OrderDate'].max().date()}")
    print("="*50)

    print("\n  Revenue by Category:")
    for cat, rev in merged.groupby("Category")["Revenue"].sum().sort_values(ascending=False).items():
        print(f"    {cat:<20} ${rev:,.2f}")

    print("\n  Revenue by Region:")
    for reg, rev in merged.groupby("Region")["Revenue"].sum().sort_values(ascending=False).items():
        print(f"    {reg:<20} ${rev:,.2f}")

    print("\n  Revenue by Segment:")
    for seg, rev in merged.groupby("Segment")["Revenue"].sum().sort_values(ascending=False).items():
        print(f"    {seg:<20} ${rev:,.2f}")
    print()


def main():
    print("Loading raw data...")
    sales, customers, products = load_data()

    print("Applying Power Query transformations...")
    sales = clean_sales(sales)
    customers = clean_customers(customers)
    products = clean_products(products)

    print("Merging tables (star schema join)...")
    merged = merge_and_enrich(sales, customers, products)

    summarize(merged)

    # Export cleaned files
    merged.to_csv("data/retail_analytics_clean.csv", index=False)
    print("  ✓ Saved: data/retail_analytics_clean.csv")

    customers.to_csv("data/customers_clean.csv", index=False)
    print("  ✓ Saved: data/customers_clean.csv")

    products.to_csv("data/products_clean.csv", index=False)
    print("  ✓ Saved: data/products_clean.csv\n")


if __name__ == "__main__":
    main()
