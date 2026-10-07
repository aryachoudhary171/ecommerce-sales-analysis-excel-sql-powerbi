-- Create the analysis database and line-item table (MySQL 8+).
CREATE DATABASE IF NOT EXISTS ecommerce_sales;
USE ecommerce_sales;

CREATE TABLE IF NOT EXISTS superstore_sales (
  row_id INT,
  order_id VARCHAR(20) NOT NULL,
  order_date DATE NOT NULL,
  ship_date DATE NOT NULL,
  ship_mode VARCHAR(30),
  customer_id VARCHAR(20),
  customer_name VARCHAR(120),
  segment VARCHAR(30),
  country VARCHAR(80),
  city VARCHAR(100),
  state VARCHAR(100),
  postal_code VARCHAR(20),
  region VARCHAR(30),
  product_id VARCHAR(30),
  category VARCHAR(40),
  sub_category VARCHAR(50),
  product_name VARCHAR(255),
  sales DECIMAL(12,2),
  quantity INT,
  discount DECIMAL(6,4),
  profit DECIMAL(12,4),
  shipping_days INT,
  order_year SMALLINT,
  order_month TINYINT,
  profit_margin_pct DECIMAL(12,6),
  discount_band VARCHAR(20),
  PRIMARY KEY (row_id),
  INDEX idx_order_date (order_date),
  INDEX idx_order_id (order_id),
  INDEX idx_customer_id (customer_id)
);

-- PostgreSQL notes: use CREATE DATABASE separately, then connect to it;
-- replace AUTO-LOAD/MySQL-specific syntax as described in 02_load_data.sql.
