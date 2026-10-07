# Power BI data model notes

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
