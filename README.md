🚀 Project Overview

This end-to-end project analyzes customer purchasing behavior, product performance, and loyalty trends for a fictional retail company.

The solution includes:

1.Synthetic data generation (Python)

Creates realistic datasets for:

Products

Customers

Transactions (with timestamps, quantities, prices, loyalty points)

2. Oracle Database (SQL Developer)

Stores data in a structured star schema:

dim_product

dim_customer

fact_sales
3. ETL Pipeline (Python)

Loads the generated CSV files into Oracle using:

Validation

Transformation

Safe reloading (fact → dims to avoid FK errors)

4. Power BI Dashboard

Final analytics dashboard with:

Sales KPIs

Loyalty vs non-loyalty comparison

Price vs quality visuals

Time-series sales trends

Top customers

Same-price/different-quality insights

Designed for analytical queries and reporting.

