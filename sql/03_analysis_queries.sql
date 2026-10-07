-- Run these in MySQL 8+ after loading superstore_sales.

-- 1. How do yearly sales, profit, and distinct order counts compare?
SELECT order_year, SUM(sales) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM superstore_sales GROUP BY order_year ORDER BY order_year;

-- 2. How did sales and profit change from the prior year?
WITH yearly AS (
  SELECT order_year, SUM(sales) AS sales, SUM(profit) AS profit
  FROM superstore_sales GROUP BY order_year
), lagged AS (
  SELECT *, LAG(sales) OVER (ORDER BY order_year) AS sales_previous,
            LAG(profit) OVER (ORDER BY order_year) AS profit_previous
  FROM yearly
)
SELECT order_year, sales, profit,
       100 * (sales - sales_previous) / NULLIF(sales_previous, 0) AS sales_yoy_pct,
       100 * (profit - profit_previous) / NULLIF(profit_previous, 0) AS profit_yoy_pct
FROM lagged ORDER BY order_year;

-- 3. Which ten customers generated the most profit?
SELECT customer_id, customer_name, SUM(profit) AS profit
FROM superstore_sales GROUP BY customer_id, customer_name
ORDER BY profit DESC LIMIT 10;

-- 4. Which ten customers generated the most sales, and what segment are they in?
SELECT customer_id, customer_name, segment, SUM(sales) AS sales
FROM superstore_sales GROUP BY customer_id, customer_name, segment
ORDER BY sales DESC LIMIT 10;

-- 5. What sales, profit, and margin did each category/sub-category deliver?
SELECT category, sub_category, SUM(sales) AS sales, SUM(profit) AS profit,
       100 * SUM(profit) / NULLIF(SUM(sales), 0) AS profit_margin_pct
FROM superstore_sales GROUP BY category, sub_category ORDER BY category, sales DESC;

-- 6. Which sub-categories are loss-making?
SELECT sub_category, SUM(sales) AS sales, SUM(profit) AS profit
FROM superstore_sales GROUP BY sub_category HAVING SUM(profit) < 0
ORDER BY profit;

-- 7. Which discount bands have the weakest average profit?
SELECT discount_band, AVG(profit) AS average_profit, SUM(profit) AS total_profit,
       COUNT(*) AS line_items
FROM superstore_sales GROUP BY discount_band
ORDER BY average_profit;

-- 8. How do shipping modes compare on average delivery time?
SELECT ship_mode, AVG(shipping_days) AS average_shipping_days,
       SUM(sales) AS sales, SUM(profit) AS profit
FROM superstore_sales GROUP BY ship_mode ORDER BY average_shipping_days;

-- 9. How many distinct orders and how much profit did each region have by year?
SELECT order_year, region, COUNT(DISTINCT order_id) AS orders, SUM(profit) AS profit
FROM superstore_sales GROUP BY order_year, region ORDER BY order_year, region;

-- 10. What are average sales and profit for each segment/category combination?
SELECT segment, category, AVG(sales) AS average_line_sales,
       AVG(profit) AS average_line_profit
FROM superstore_sales GROUP BY segment, category ORDER BY segment, category;

-- 11. What is the monthly sales trend and cumulative sales total?
WITH monthly AS (
  SELECT DATE_FORMAT(order_date, '%Y-%m-01') AS month_start, SUM(sales) AS sales
  FROM superstore_sales GROUP BY DATE_FORMAT(order_date, '%Y-%m-01')
)
SELECT month_start, sales,
       SUM(sales) OVER (ORDER BY month_start ROWS UNBOUNDED PRECEDING) AS running_sales
FROM monthly ORDER BY month_start;

-- 12. How do states rank by total profit?
WITH state_profit AS (
  SELECT state, SUM(profit) AS profit FROM superstore_sales GROUP BY state
)
SELECT state, profit, RANK() OVER (ORDER BY profit DESC) AS profit_rank
FROM state_profit ORDER BY profit_rank, state;

-- PostgreSQL: LIMIT works; DATE_FORMAT becomes TO_CHAR(order_date, 'YYYY-MM-01');
-- MySQL and PostgreSQL both support LAG, RANK, and SUM() OVER in current versions.
