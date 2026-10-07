"""Clean the original Superstore CSV and create portfolio analysis outputs.

Run from the project folder with: python data/clean_data.py
The raw source is read-only; all outputs are written to cleaned/, powerbi/,
sql/, and images/.
"""
from pathlib import Path
import re

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "superstore.csv"
if not RAW.exists():
    # Accept the downloaded source name while preserving the exact original.
    alternate = ROOT / "data" / "raw" / "Sample - Superstore.csv"
    if alternate.exists():
        RAW = alternate
    else:
        raise FileNotFoundError(f"Place the dataset at: {ROOT / 'data/raw/superstore.csv'}")
CLEAN = ROOT / "data" / "cleaned" / "superstore_cleaned.csv"


def snake(name):
    name = re.sub(r"[^A-Za-z0-9]+", "_", str(name).strip()).strip("_").lower()
    return name


def money(value):
    return f"${value:,.2f}"


def safe_div(a, b):
    return a / b if b else 0.0


def save_chart(filename, title, labels, values, color=(42, 112, 166), value_format=None):
    """Draw a clear, dependency-light chart as PNG using Pillow."""
    width, height = 1100, 620
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        title_font = ImageFont.truetype("arial.ttf", 28)
        small = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = title_font = small = ImageFont.load_default()
    draw.text((48, 28), title, fill=(28, 45, 63), font=title_font)
    left, right, top, bottom = 100, 1050, 100, 510
    draw.line((left, top, left, bottom, right, bottom), fill=(120, 130, 140), width=2)
    vals = [float(v) if pd.notna(v) else 0.0 for v in values]
    maxv = max([abs(v) for v in vals] + [1.0])
    if len(vals) <= 1:
        step = 0
    else:
        step = (right - left) / len(vals)
    bar_w = max(12, min(58, step * 0.62 if step else 40))
    for i, (label, val) in enumerate(zip(labels, vals)):
        x = left + (i + 0.5) * step if step else (left + right) / 2
        bar_h = (abs(val) / maxv) * (bottom - top - 35)
        y = bottom - bar_h
        fill = color if val >= 0 else (194, 69, 59)
        draw.rectangle((x - bar_w/2, y, x + bar_w/2, bottom), fill=fill)
        label_text = str(label)
        draw.text((x - 30, bottom + 12), label_text[:12], fill=(50, 60, 70), font=small)
        if len(vals) <= 16:
            shown = value_format(val) if value_format else f"{val:,.0f}"
            draw.text((x - 35, max(top + 3, y - 22)), shown, fill=(45, 55, 65), font=small)
    img.save(ROOT / "images" / filename)


def write_csv(frame, filename):
    frame.to_csv(ROOT / "powerbi" / filename, index=False, encoding="utf-8-sig")


def main():
    for folder in ["data/cleaned", "excel", "sql", "powerbi", "images"]:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    # The commonly shared extract is Windows-1252 encoded rather than UTF-8.
    frame = pd.read_csv(RAW, dtype={"Postal Code": "string"}, encoding="cp1252")
    rows_before = len(frame)
    # Empty strings and whitespace-only cells are treated as missing.
    frame = frame.replace(r"^\s*$", pd.NA, regex=True)
    duplicates = int(frame.duplicated().sum())
    frame = frame.drop_duplicates().copy()
    original_columns = list(frame.columns)
    frame.columns = [snake(c) for c in frame.columns]
    # This Superstore extract stores dates in month/day/year format.
    for col in ["order_date", "ship_date"]:
        frame[col] = pd.to_datetime(frame[col], errors="coerce", format="mixed")
    numeric = ["sales", "quantity", "discount", "profit"]
    for col in numeric:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    null_before = int(frame.isna().sum().sum())
    text_cols = [c for c in frame.columns if c not in numeric + ["order_date", "ship_date"]]
    for col in text_cols:
        frame[col] = frame[col].astype("string").str.strip().fillna("Unknown")
    for col in numeric:
        frame[col] = frame[col].fillna(0)
    # A date that cannot be parsed is unusable for time analysis; fill it from
    # the other date only when possible, otherwise use the earliest valid date.
    earliest = min(frame["order_date"].min(), frame["ship_date"].min())
    for col, other in [("order_date", "ship_date"), ("ship_date", "order_date")]:
        frame[col] = frame[col].fillna(frame[other]).fillna(earliest)
    null_after = int(frame.isna().sum().sum())
    frame["shipping_days"] = (frame["ship_date"] - frame["order_date"]).dt.days
    # Negative transit time indicates source date inconsistency; retain the
    # observed difference for auditability rather than silently changing it.
    frame["order_year"] = frame["order_date"].dt.year
    frame["order_month"] = frame["order_date"].dt.month
    frame["profit_margin_pct"] = (frame["profit"] / frame["sales"].replace(0, pd.NA) * 100).fillna(0)
    frame["discount_band"] = pd.cut(
        frame["discount"], [-float("inf"), 0, 0.1, 0.2, 0.3, float("inf")],
        labels=["0%", "1-10%", "11-20%", "21-30%", ">30%"],
        include_lowest=True, right=True,
    ).astype("string")
    frame.to_csv(CLEAN, index=False, date_format="%Y-%m-%d", encoding="utf-8-sig")

    # Reusable, real-data aggregations for the workbook, Power BI, SQL checks,
    # visuals, and written insights.
    orders = frame.groupby("order_year").agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")).reset_index()
    orders["profit_margin_pct"] = orders["profit"] / orders["sales"] * 100
    for metric in ["sales", "profit", "orders"]:
        orders[f"{metric}_yoy_pct"] = orders[metric].pct_change() * 100
    write_csv(orders, "yearly_summary.csv")
    monthly = frame.groupby(["order_year", "order_month"]).agg(sales=("sales", "sum"), profit=("profit", "sum")).reset_index()
    monthly["month"] = pd.to_datetime({"year": monthly.order_year, "month": monthly.order_month, "day": 1})
    write_csv(monthly[["month", "sales", "profit"]], "monthly_summary.csv")
    category = frame.groupby(["category", "sub_category"]).agg(sales=("sales", "sum"), profit=("profit", "sum"), quantity=("quantity", "sum")).reset_index()
    category["profit_margin_pct"] = category["profit"] / category["sales"] * 100
    write_csv(category, "category_subcategory_summary.csv")
    region = frame.groupby(["order_year", "region"]).agg(orders=("order_id", "nunique"), sales=("sales", "sum"), profit=("profit", "sum")).reset_index()
    write_csv(region, "region_year_summary.csv")
    customer = frame.groupby(["customer_id", "customer_name", "segment"]).agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")).reset_index()
    write_csv(customer.sort_values("sales", ascending=False).head(10), "top_customers.csv")

    discount = frame.groupby("discount_band", observed=False).agg(sales=("sales", "sum"), profit=("profit", "sum"), avg_profit=("profit", "mean"), rows=("order_id", "size")).reset_index()
    discount_category = frame.assign(discounted=frame.discount.gt(0)).groupby(["category", "discounted"]).agg(avg_profit=("profit", "mean"), total_profit=("profit", "sum"), line_items=("profit", "size")).reset_index()
    ship = frame.groupby("ship_mode").agg(avg_shipping_days=("shipping_days", "mean"), sales=("sales", "sum"), profit=("profit", "sum")).reset_index()
    segment_cat = frame.groupby(["segment", "category"]).agg(avg_sales=("sales", "mean"), avg_profit=("profit", "mean")).reset_index()
    state = frame.groupby("state").agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")).reset_index().sort_values("profit", ascending=False)
    for data, name in [(discount, "discount_summary.csv"), (discount_category, "discount_category_summary.csv"), (ship, "ship_mode_summary.csv"), (segment_cat, "segment_category_summary.csv"), (state, "state_summary.csv")]:
        write_csv(data, name)

    # Business observations are computed directly from the cleaned rows.
    best_year = orders.loc[orders.sales.idxmax()]
    best_profit_cat = category.loc[category.profit.idxmax()]
    worst_subcat = category.loc[category.profit.idxmin()]
    best_ship = ship.loc[ship.avg_shipping_days.idxmin()]
    worst_ship = ship.loc[ship.avg_shipping_days.idxmax()]
    high_discount = discount[discount.discount_band.isin(["21-30%", ">30%"])]
    no_discount = discount[discount.discount_band == "0%"]
    furniture_disc = frame[(frame.category == "Furniture") & (frame.discount > 0)]
    furniture_full = frame[(frame.category == "Furniture") & (frame.discount == 0)]
    tech_disc = frame[(frame.category == "Technology") & (frame.discount > 0)]
    office_disc = frame[(frame.category == "Office Supplies") & (frame.discount > 0)]
    region_orders = frame.groupby("region")["order_id"].nunique().sort_values(ascending=False)
    insights = [
        f"The strongest sales year was {int(best_year.order_year)}, with {money(best_year.sales)} in sales and {money(best_year.profit)} in profit.",
        f"{best_profit_cat.sub_category} led category/sub-category profit at {money(best_profit_cat.profit)} (within {best_profit_cat.category}).",
        f"{worst_subcat.sub_category} had the lowest sub-category profit at {money(worst_subcat.profit)}; review its pricing, discounting, and costs.",
        f"{best_ship.ship_mode} had the shortest average shipping time ({best_ship.avg_shipping_days:.2f} days); {worst_ship.ship_mode} averaged {worst_ship.avg_shipping_days:.2f} days.",
        f"Discount bands of 21% or higher produced {money(high_discount.profit.sum())} combined profit across {int(high_discount.rows.sum()):,} rows.",
        f"The zero-discount band produced {money(no_discount.profit.sum())} profit; compare this with higher-discount bands before setting discount policy.",
        f"Discounted Technology rows stayed profitable at {money(tech_disc.profit.mean())} average profit ({money(tech_disc.profit.sum())} total), while discounted Furniture averaged {money(furniture_disc.profit.mean())} and Office Supplies {money(office_disc.profit.mean())}; treat Technology only as a controlled test candidate, not proof discounts improve profit.",
        f"{region_orders.index[0]} had the most distinct orders ({int(region_orders.iloc[0]):,}) across the full dataset.",
    ]
    # Determine any threshold statement only from computed results.
    high_band_loss = bool((high_discount.profit.sum() < 0) and (no_discount.profit.sum() > 0))
    insight_path = ROOT / "excel" / "insights.txt"
    insight_path.write_text("\n".join(f"- {x}" for x in insights), encoding="utf-8")

    (ROOT / "sql" / "01_schema.sql").write_text(r'''-- Create the analysis database and line-item table (MySQL 8+).
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
''', encoding="utf-8")
    (ROOT / "sql" / "02_load_data.sql").write_text(r'''-- Load the cleaned CSV, not the untouched source CSV.
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
''', encoding="utf-8")
    (ROOT / "sql" / "03_analysis_queries.sql").write_text(r'''-- Run these in MySQL 8+ after loading superstore_sales.

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
''', encoding="utf-8")

    # Markdown table helper for the compact SQL parity report.
    def md_table(df, columns, limit=30):
        out = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
        for _, row in df.head(limit).iterrows():
            vals = []
            for col in columns:
                val = row[col]
                if pd.isna(val):
                    vals.append("—")
                elif col in {"order_year", "orders", "rows", "line_items", "profit_rank"}:
                    vals.append(f"{int(val):,}")
                elif isinstance(val, (float, int)):
                    vals.append(f"{val:,.2f}")
                else:
                    vals.append(str(val))
            out.append("| " + " | ".join(vals) + " |")
        return "\n".join(out)
    sql_report = [
        "# SQL query results sanity check", "",
        f"The 12 MySQL queries in `03_analysis_queries.sql` were independently reproduced with pandas on {len(frame):,} cleaned rows. The tables below are representative expected results for checking a MySQL import.", "",
        "## Yearly sales, profit, orders, and growth", "", md_table(orders, ["order_year", "sales", "profit", "orders", "profit_margin_pct", "sales_yoy_pct", "profit_yoy_pct"]), "",
        "## Top 10 customers by profit", "", md_table(customer.sort_values("profit", ascending=False), ["customer_id", "customer_name", "profit"], limit=10), "",
        "## Category and sub-category", "", md_table(category.sort_values("sales", ascending=False), ["category", "sub_category", "sales", "profit", "profit_margin_pct"]), "",
        "## Discount band", "", md_table(discount, ["discount_band", "avg_profit", "profit", "rows"]), "",
        "## Discounted vs zero-discount profit by category", "", md_table(discount_category, ["category", "discounted", "avg_profit", "total_profit", "line_items"]), "",
        "## Ship mode", "", md_table(ship, ["ship_mode", "avg_shipping_days", "sales", "profit"]), "",
        "## Loss-making sub-categories", "", md_table(category[category.profit < 0].sort_values("profit"), ["sub_category", "sales", "profit", "profit_margin_pct"]), "",
        "## Top 10 customers by sales", "", md_table(customer.sort_values("sales", ascending=False), ["customer_id", "customer_name", "segment", "sales"]), "",
        "## Region by year", "", md_table(region, ["order_year", "region", "orders", "sales", "profit"]), "",
        "## Segment by category averages", "", md_table(segment_cat, ["segment", "category", "avg_sales", "avg_profit"]), "",
        "## Monthly sales and running total", "", md_table(monthly.assign(running_sales=monthly.sales.cumsum()), ["month", "sales", "running_sales"], limit=48), "",
        "## State profit ranking (top 15)", "", md_table(state.assign(profit_rank=state.profit.rank(method="min", ascending=False).astype(int)), ["state", "profit", "profit_rank"], limit=15), "",
        "## Validation note", "", "Order counts use distinct `order_id`, not line count. Margins are profit divided by sales. Monthly running totals are sorted by calendar month. All amounts are computed from the cleaned source file.", ""
    ]
    (ROOT / "sql" / "query_results_summary.md").write_text("\n".join(sql_report), encoding="utf-8")

    (ROOT / "powerbi" / "data_model_notes.md").write_text(r'''# Power BI data model notes

## Import and prepare data
1. In Power BI Desktop choose **Get data > Text/CSV** and select `data/cleaned/superstore_cleaned.csv`.
2. Confirm UTF-8 and comma delimiter. Set `order_date` and `ship_date` to **Date**; sales/profit to **Fixed decimal number**; discount and margin to **Decimal number**; quantity, years, months, and shipping days to **Whole number**.
3. Use **Transform data** to verify types and trim text. The cleaning script already standardizes column names and text values; avoid applying different filters on refresh.
4. Choose **Close & Apply**.

## Date table
Create a calculated table, then mark it as the date table using `Date[Date]`:

```DAX
Date =
ADDCOLUMNS (
    CALENDAR ( MIN ( superstore_cleaned[order_date] ), MAX ( superstore_cleaned[order_date] ) ),
    "Year", YEAR ( [Date] ),
    "Month Number", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "Year Month", FORMAT ( [Date], "YYYY-MM" )
)
```

Sort `Date[Month]` by `Date[Month Number]`, and `Date[Year Month]` by `Date[Date]` if you use it as a label. Create a one-to-many relationship from `Date[Date]` to `superstore_cleaned[order_date]`. Keep it single-direction. Use this date table for time-intelligence visuals.

## Grain and interpretation
Each row is an order line, not a whole order. Use `DISTINCTCOUNT(order_id)` for orders. The CSV includes the full Superstore extract with three segments and four calendar years. Discounts and profit are analyzed at line level; this is descriptive analysis and does not establish causation.
''', encoding="utf-8")
    (ROOT / "powerbi" / "dax_measures.md").write_text(r'''# DAX measures

Create these measures on the `superstore_cleaned` table. The Date table must be related and marked as the date table for prior-year calculations.

```DAX
Total Sales = SUM ( superstore_cleaned[sales] )
Total Profit = SUM ( superstore_cleaned[profit] )
Total Quantity = SUM ( superstore_cleaned[quantity] )
Number of Orders = DISTINCTCOUNT ( superstore_cleaned[order_id] )
Profit Margin % = DIVIDE ( [Total Profit], [Total Sales], 0 )
Avg Shipping Days = AVERAGE ( superstore_cleaned[shipping_days] )
Sales LY = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
Sales YoY % = DIVIDE ( [Total Sales] - [Sales LY], [Sales LY] )
Profit LY = CALCULATE ( [Total Profit], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
Profit YoY % = DIVIDE ( [Total Profit] - [Profit LY], [Profit LY] )
```

- Total Sales, Total Profit, and Total Quantity aggregate their respective line-item values.
- Number of Orders counts unique order IDs, avoiding counting each line as a separate order.
- Profit Margin % is total profit divided by total sales in the current filter context.
- Avg Shipping Days averages the observed difference between ship and order dates.
- Sales LY and Profit LY shift the current date filter one year back; the YoY measures compare the current value with that prior-year value.

Format Profit Margin %, Sales YoY %, and Profit YoY % as percentages. Format sales/profit as currency and quantity/orders as whole numbers.
''', encoding="utf-8")
    (ROOT / "powerbi" / "dashboard_build_guide.md").write_text(r'''# Power BI dashboard build guide

## Page layout
1. Add five KPI cards across the top: **Total Sales**, **Total Profit**, **Total Quantity**, **Number of Orders**, **Profit Margin %**.
2. Add a line chart with `Date[Year Month]` on the axis and **Total Sales** plus **Total Profit** as values.
3. Add a clustered bar chart with Category on the axis and Sales/Profit as values.
4. Add a filled map using State as location and Total Sales as the color/value; confirm state geocoding before interpreting it.
5. Add a table or bar chart for the top 10 customers by sales. Use a visual-level Top N filter on customer name and sort by Total Sales descending.
6. Add a doughnut chart for category share of Total Sales.
7. Add a bar chart for the top 5 sub-categories by Total Sales, using a Top N filter.
8. Add slicers for Date[Year], Region, and Segment. Set interactions so all visuals respond consistently.

## Formatting
- Use a restrained navy/teal palette, light background, and consistent currency formatting.
- Use clear titles and subtitles that state the metric and date grain.
- Avoid 3D visuals; sort category bars by sales; display negative profit distinctly.
- Add a tooltip with Sales, Profit, and Profit Margin where it helps explain a point.
- Check the page at typical laptop size and test every slicer before saving the `.pbix` locally.

The project contains chart-ready summary CSV files for alternate visuals. Create and save the actual dashboard in Power BI Desktop; the `.pbix` is a manual step.
''', encoding="utf-8")
    (ROOT / "excel" / "how_to_make_real_pivots.md").write_text(r'''# Recreate the formula summaries as real PivotTables

The workbook uses formulas for summaries because the Python/JavaScript workbook writer does not reliably export native Excel PivotTables. To make a PivotTable in desktop Excel:

1. Open `ecommerce_sales_analysis.xlsx` and go to `Cleaned_Data`.
2. Click inside the data and choose **Insert > PivotTable > From Table/Range**.
3. Select **New Worksheet** and confirm. Rename the new sheet for the analysis.
4. Drag the requested fields into Rows, Columns, Values, and Filters. For distinct order counts, tick **Add this data to the Data Model** when creating the PivotTable, then set Order ID to **Distinct Count**.
5. In Value Field Settings choose Sum, Average, or Count as appropriate. For margins, add a calculated measure (profit divided by sales) or place summary totals beside the PivotTable and calculate `Profit / Sales`.
6. Insert a PivotChart from the PivotTable and add slicers for Year, Region, or Segment.

Suggested layouts: Year in Rows with Sales/Profit in Values; Ship Mode in Rows with Average of Shipping Days; Segment in Rows and Category in Columns with Average Sales/Profit; Category and Sub-Category in Rows with Sales/Profit; Discount Band in Rows with Profit; Region in Rows and Year in Columns with distinct Order ID; Year in Rows with Sales, Profit, and distinct Orders for YoY calculations.

PivotTables are optional additions; the existing formula summary tabs remain available as a transparent reference.
''', encoding="utf-8")

    readme = f'''# E-Commerce Sales Analysis (Excel + SQL + Power BI)

## Problem statement
Explore four years of Superstore order-line data to identify sales and profit trends, product/category performance, shipping patterns, discount outcomes, and regional/customer opportunities.

## Dataset
The original Superstore dataset supplied for this project is preserved under `data/raw/`. The analysis uses {len(frame):,} order-line records spanning {frame.order_date.min():%Y}–{frame.order_date.max():%Y}. A row represents a product line on an order; order counts therefore use distinct Order IDs. No data was fabricated.

## Tools
Python and pandas for cleaning and analysis; Excel formulas and native charts for the workbook; MySQL 8+ SQL with PostgreSQL notes; Power BI Desktop instructions and DAX. Charts are written as PNG using Pillow because matplotlib is not installed in the bundled runtime; the project data and chart values are real.

## Folder structure
```text
data/raw/       original CSV files (unchanged)
data/cleaned/   cleaned import-ready CSV
data/           clean_data.py and cleaning summaries
excel/          analysis workbook and PivotTable guide
sql/            schema, load steps, 12 queries, result checks
powerbi/        model/DAX/build notes and chart-ready CSVs
images/         generated PNG charts
```

## Business questions answered
- How did annual sales, profit, and order counts change?
- Which categories and sub-categories create or lose profit?
- How do discount levels relate to average and total profit?
- Which shipping modes are fastest on average?
- How do segments, regions, states, and customers compare?

## Methodology
`data/clean_data.py` trims text, standardizes column names, removes exact duplicates, parses dates, handles blanks, derives shipping days/year/month/margin/discount band, and writes a separate cleaned file. Summary tables are computed from that cleaned data. SQL queries use distinct order counts and window functions. Excel summaries use formulas rather than pretending to be PivotTables.

Cleaning summary: **{rows_before:,} rows before**, **{duplicates:,} duplicate rows removed**, **{len(frame):,} rows after**, and **{null_before:,} missing cells handled**. See [`data/cleaning_summary.md`](data/cleaning_summary.md).

## Findings from this dataset
{chr(10).join(insights[:5])}

The high-discount finding is descriptive association only; customer/order mix and product costs may also explain the observed profit.

## Charts
![Yearly sales](images/yearly_sales.png)
![Yearly profit](images/yearly_profit.png)
![Sub-category profit](images/category_profit.png)
![Discount band profit](images/discount_profit.png)
![Shipping time by ship mode](images/ship_mode_days.png)
![Orders by region](images/region_orders.png)
![Year-over-year sales growth](images/yoy_sales.png)

## Recommendations
- Review discount approvals above 20%; compare incremental revenue and profit at product/order level before changing policy.
- Investigate loss-making sub-categories and Furniture discount outcomes with pricing and cost data.
- Use customer, region, and segment filters to prioritize follow-up analysis; do not infer causality from the summaries.
- Compare shipping speed with cost and customer satisfaction before changing fulfillment mode.

## How to run
From the project folder, run `python data/clean_data.py` with pandas and Pillow installed. Open `excel/ecommerce_sales_analysis.xlsx` in Excel. In MySQL Workbench, run `sql/01_schema.sql`, import the cleaned CSV using `sql/02_load_data.sql`, then run queries from `sql/03_analysis_queries.sql`. Follow `powerbi/dashboard_build_guide.md` to create the `.pbix` dashboard.

## Future improvements
- Add product cost, returns, and customer satisfaction data to measure drivers and net outcomes.
- Add automated refresh and a documented validation pipeline.
- Extend the forecast with holdout error metrics and compare simple baseline models.
- Build an interactive Power BI report and add a verified map.
'''
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    resume = f'''# Resume and interview preparation

## Resume bullets
- Cleaned and analyzed {len(frame):,} Superstore order lines with Python and pandas, removing {duplicates:,} duplicate rows and preparing date, shipping-time, margin, and discount-band fields for Excel, SQL, and Power BI analysis.
- Built Excel formula summaries, 12 MySQL analysis queries, and chart-ready Power BI tables; found {money(high_discount.profit.sum())} combined profit for discount levels above 20%, informing a targeted discount review.
- Compared {len(category)} sub-categories and identified {worst_subcat.sub_category} as the largest loss-making sub-category at {money(worst_subcat.profit)}; documented follow-up checks for pricing and cost drivers.

## LinkedIn draft
I completed an E-Commerce Sales Analysis portfolio project using Excel, SQL, Power BI, and Python on the Superstore dataset. I cleaned 9,994 order lines, analyzed yearly sales and profit, category performance, shipping time, and discount bands. A few findings: {money(best_year.sales)} in sales in {int(best_year.order_year)}, {worst_subcat.sub_category} was the most loss-making sub-category ({money(worst_subcat.profit)}), and discount bands above 20% combined for {money(high_discount.profit.sum())} profit. I also prepared SQL queries and a Power BI build guide. The results are descriptive and point to questions for deeper cost and customer analysis.

## Interview questions and short model answers
1. **What was the project goal?** Analyze sales, profit, order, discount, shipping, and customer patterns in the supplied Superstore data.
2. **What does one row represent?** A product line on an order, so an order can have multiple rows.
3. **Why count distinct Order IDs?** Counting rows would overstate the number of orders when an order has several product lines.
4. **Why standardize column names?** Consistent snake_case names are easier to use in Python, SQL, and DAX.
5. **How did you handle duplicates?** Removed exact duplicate rows and reported the before/after row counts; this file had {duplicates} exact duplicates.
6. **How did you calculate shipping days?** Ship Date minus Order Date in whole calendar days.
7. **How did you calculate profit margin?** Profit divided by Sales times 100 at row level; for aggregate margin, divide total profit by total sales.
8. **How is YoY growth calculated?** (Current year value minus previous year value) divided by previous year value, times 100.
9. **What does SQL LAG() do?** It returns a value from a preceding row in the ordered result, here the prior year's sales or profit.
10. **Why use SUM() and COUNT(DISTINCT)?** Sales/profit add across lines, while order IDs repeat across those lines.
11. **What does the Sales LY DAX measure do?** SAMEPERIODLASTYEAR shifts the selected Date table period back one year.
12. **How does the simple forecast work?** FORECAST.LINEAR fits a straight line to yearly sales and extrapolates one year; it is illustrative, not a production forecast.
13. **What does a negative profit mean?** The recorded profit for that row or group is below zero; it warrants follow-up on price, discount, and cost.
14. **What are key limitations?** The data lacks cost detail, returns context, customer satisfaction, and causal controls; descriptive group comparisons do not prove discounts caused a loss.
15. **What would you improve next?** Validate against more operational data, assess forecast error on a held-out period, and build/QA the interactive Power BI report.
'''
    (ROOT / "RESUME_AND_INTERVIEW.md").write_text(resume, encoding="utf-8")

    # Chart PNGs are generated with Pillow because matplotlib is not present in
    # the bundled Python runtime. The source remains beginner-friendly and the
    # output images are genuine plots of the source data.
    save_chart("yearly_sales.png", "Yearly Sales", orders.order_year.astype(str), orders.sales, value_format=money)
    save_chart("yearly_profit.png", "Yearly Profit", orders.order_year.astype(str), orders.profit, color=(48, 142, 105), value_format=money)
    save_chart("category_profit.png", "Profit by Sub-Category", category.sub_category, category.profit, color=(52, 125, 150), value_format=money)
    save_chart("discount_profit.png", "Profit by Discount Band", discount.discount_band, discount.profit, color=(202, 141, 50), value_format=money)
    save_chart("ship_mode_days.png", "Average Shipping Days by Ship Mode", ship.ship_mode, ship.avg_shipping_days, color=(112, 92, 159), value_format=lambda x: f"{x:.1f}")
    save_chart("region_orders.png", "Distinct Orders by Region", region_orders.index, region_orders.values, color=(62, 135, 95))
    save_chart("yoy_sales.png", "Year-over-Year Sales Growth (%)", orders.order_year.iloc[1:].astype(str), orders.sales_yoy_pct.iloc[1:], color=(44, 122, 185), value_format=lambda x: f"{x:.1f}%")
    save_chart("region_profit.png", "Profit by Region", region.region.unique(), region.groupby("region").profit.sum().reindex(region.region.unique()), color=(66, 125, 156), value_format=money)

    (ROOT / "data" / "cleaning_summary.md").write_text(
        f"# Cleaning summary\n\n- Raw file: `{RAW.name}`\n- Rows before cleaning: {rows_before:,}\n- Exact duplicate rows removed: {duplicates:,}\n- Rows after duplicate removal: {len(frame):,}\n- Missing cells before imputation: {null_before:,}\n- Missing cells after cleaning: {null_after:,}\n- Original input columns: {len(original_columns)}\n- Output rows retain all source fields, standardized to snake_case, plus five derived fields.\n- Date range: {frame.order_date.min():%Y-%m-%d} to {frame.order_date.max():%Y-%m-%d}\n- Shipping day values below zero: {int((frame.shipping_days < 0).sum())} (retained as source-date quality flags)\n",
        encoding="utf-8",
    )
    (ROOT / "data" / "cleaning_summary.json").write_text(
        pd.Series({"rows_before": rows_before, "duplicates_removed": duplicates, "rows_after": len(frame), "null_cells_before": null_before, "null_cells_after": null_after}).to_json(indent=2), encoding="utf-8"
    )
    print(f"Rows before: {rows_before:,}; after: {len(frame):,}; duplicates removed: {duplicates:,}; missing cells before/after: {null_before:,}/{null_after:,}")
    print(f"Cleaning summary saved to {ROOT / 'data' / 'cleaning_summary.md'}")


if __name__ == "__main__":
    main()
