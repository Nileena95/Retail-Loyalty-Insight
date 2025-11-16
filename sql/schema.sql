-- Enable UUID generation extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Product dimension
CREATE TABLE dim_product (
  product_id SERIAL PRIMARY KEY,
  sku TEXT UNIQUE,
  name TEXT,
  category TEXT,
  quality INTEGER,
  price NUMERIC(10,2)
);

-- Customer dimension
CREATE TABLE dim_customer (
  customer_id SERIAL PRIMARY KEY,
  customer_uuid UUID DEFAULT gen_random_uuid(),
  name TEXT,
  has_loyalty BOOLEAN
);

-- Sales fact table
CREATE TABLE fact_sales (
  sale_id SERIAL PRIMARY KEY,
  product_id INTEGER NOT NULL REFERENCES dim_product(product_id),
  customer_id INTEGER NOT NULL REFERENCES dim_customer(customer_id),
  sale_ts TIMESTAMP WITHOUT TIME ZONE,
  quantity INTEGER,
  unit_price NUMERIC(10,2),
  pc_points_awarded INTEGER
);
