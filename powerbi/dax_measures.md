# DAX measures

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
