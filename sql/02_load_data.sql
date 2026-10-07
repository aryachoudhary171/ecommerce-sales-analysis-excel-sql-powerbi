-- Load the cleaned CSV, not the untouched source CSV.
-- Option A (recommended for beginners): MySQL Workbench
-- 1. Create/select ecommerce_sales and run 01_schema.sql.
-- 2. Right-click superstore_sales > Table Data Import Wizard.
-- 3. Select data/cleaned/superstore_cleaned.csv; choose comma delimiter and UTF-8.
-- 4. Map each CSV column to the same-named table column; finish and check row count.
--
-- Option B: MySQL LOAD DATA (server permissions and LOCAL INFILE may need enabling).
-- Use the absolute path to your cleaned CSV and keep the forward slashes.
LOAD DATA LOCAL INFILE 'C:/path/to/project/data/cleaned/superstore_cleaned.csv'
INTO TABLE superstore_sales
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@row_id, order_id, @order_date, @ship_date, ship_mode, customer_id,
 customer_name, segment, country, city, state, postal_code, region,
 product_id, category, sub_category, product_name, sales, quantity,
 discount, profit, shipping_days, order_year, order_month,
 profit_margin_pct, discount_band)
SET row_id = NULLIF(@row_id, ''),
    order_date = STR_TO_DATE(@order_date, '%Y-%m-%d'),
    ship_date = STR_TO_DATE(@ship_date, '%Y-%m-%d');

-- PostgreSQL: use psql \copy superstore_sales FROM '.../superstore_cleaned.csv'
-- WITH (FORMAT csv, HEADER true, ENCODING 'UTF8'); dates are ISO (YYYY-MM-DD).
