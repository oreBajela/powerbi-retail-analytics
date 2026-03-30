# 📊 Retail Sales & Customer Analytics Dashboard

An interactive business intelligence dashboard replicating a Power BI report, built to demonstrate data analysis, transformation, and visualization.

---

## 🔍 Project Overview

This project analyzes 12 months of retail sales data (Jan–Dec 2023) for a multi-region retailer. The goal was to build a dashboard that provides KPI cards, trend analysis, customer segmentation, and interactive slicers.

The dataset covers **91 transactions**, **15 customers**, **5 products** across **4 regions**, with product categories spanning Electronics, Fitness, Footwear, and Accessories.

---

## 📁 Repository Structure

```
powerbi-retail-analytics/
│
├── dashboard.html          # Interactive dashboard (open in any browser)
├── data/
│   ├── sales.csv           # Raw sales transactions
│   ├── customers.csv       # Customer profiles and segments
│   └── products.csv        # Product catalog with cost prices
├── clean_data.py           # Python script replicating Power Query transformations
└── README.md
```

---

## 🚀 How to View the Dashboard

1. Clone or download this repository
2. Open `dashboard.html` in any browser (Chrome, Firefox, Safari)
3. No server or install required — it runs entirely in the browser

> 

---

## 📊 Dashboard Features

### KPI Cards
| Metric | Description |
|--------|-------------|
| Total Revenue | Sum of all order revenue after discounts |
| Total Orders | Count of all transactions |
| Average Order Value | Revenue ÷ Orders |
| Profit Margin % | (Revenue − Cost) ÷ Revenue |

### Visualizations
- **Monthly Revenue Trend** — Line chart tracking revenue across all 12 months
- **Revenue by Region** — Donut chart comparing North / South / East / West
- **Revenue by Category** — Bar chart across Electronics, Fitness, Footwear, Accessories
- **Orders vs Revenue Scatter Plot** — Each dot is a customer, colored by segment
- **Premium vs Standard Segment** — Pie chart of revenue share by customer tier
- **Top Customers Table** — Ranked by total spend with inline bar charts

### Interactive Slicers
All charts update in real time when you filter by:
- **Region** (North, South, East, West)
- **Customer Segment** (Premium, Standard)
- **Product Category** (Electronics, Fitness, Footwear, Accessories)

---

## 🔧 Power Query Transformations (replicated in Python)

The `clean_data.py` script replicates the following Power Query steps:

| Step | Transformation |
|------|----------------|
| Data type casting | OrderDate → Date, Quantity → Integer, Price → Decimal |
| Calculated column | `Revenue = Quantity × UnitPrice × (1 − Discount)` |
| Calculated column | `Profit = Revenue − (CostPrice × Quantity)` |
| Date parts | Extract Month name and Year from OrderDate |
| Column merge | FirstName + LastName → FullName |
| Conditional column | CostPrice bucketed into Budget / Mid-range / Premium |
| Table merge | Sales joined to Customers and Products (star schema) |

---

## 📐 Data Model

The data follows a **star schema** — the standard structure used in Power BI:

```
Customers (dim)  ──┐
                   ├──  Sales (fact)
Products (dim)   ──┘
```

- `Sales` is the **fact table** containing transaction-level data
- `Customers` and `Products` are **dimension tables** with descriptive attributes
- Relationships are: `Sales.CustomerID → Customers.CustomerID` and `Sales.ProductID → Products.ProductID`

---

## 📏 DAX Measures (implemented as JavaScript)

The following measures were written in DAX for Power BI and replicated in the dashboard:

```dax
Total Revenue = SUM(Sales[Revenue])

Total Orders = COUNTROWS(Sales)

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Total Profit =
SUMX(
    Sales,
    Sales[Revenue] - (RELATED(Products[CostPrice]) * Sales[Quantity])
)

Profit Margin % = DIVIDE([Total Profit], [Total Revenue]) * 100

Premium Customer Revenue =
CALCULATE(
    [Total Revenue],
    Customers[Segment] = "Premium"
)
```

---

## 🛠 Tools & Technologies

| Tool | Purpose |
|------|---------|
| Power BI Service | Dashboard design and report building |
| Power Query | Data cleaning and transformation |
| DAX | Calculated measures and KPIs |
| Python (pandas) | Data pipeline replication (`clean_data.py`) |
| Chart.js | Interactive chart rendering in the HTML dashboard |
| HTML / CSS / JavaScript | Dashboard layout and interactivity |

---

## 📈 Key Insights from the Data

- **Electronics** is the highest-revenue category driven by Smart Watch and Wireless Headphones
- **Premium customers** (6 of 15) account for a disproportionately large share of total revenue
- Revenue shows a **steady upward trend** through Q4, with a notable spike in holiday months
- The **East region** leads in order volume, while **North** has the highest average order value
- Customers with **5+ orders** are exclusively in the Premium segment

---

## 👤 About

Built by a Data Science student as a portfolio project demonstrating business intelligence skills.

**Skills demonstrated:** Power BI · Power Query · DAX · Star schema modeling · Data cleaning · KPI design · Dashboard storytelling
