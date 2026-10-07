# Resume and interview preparation

## Resume bullets
- Cleaned and analyzed 9,994 Superstore order lines with Python and pandas, removing 0 duplicate rows and preparing date, shipping-time, margin, and discount-band fields for Excel, SQL, and Power BI analysis.
- Built Excel formula summaries, 12 MySQL analysis queries, and chart-ready Power BI tables; found $-135,376.06 combined profit for discount levels above 20%, informing a targeted discount review.
- Compared 17 sub-categories and identified Tables as the largest loss-making sub-category at $-17,725.48; documented follow-up checks for pricing and cost drivers.

## LinkedIn draft
I completed an E-Commerce Sales Analysis portfolio project using Excel, SQL, Power BI, and Python on the Superstore dataset. I cleaned 9,994 order lines, analyzed yearly sales and profit, category performance, shipping time, and discount bands. A few findings: $733,215.26 in sales in 2017, Tables was the most loss-making sub-category ($-17,725.48), and discount bands above 20% combined for $-135,376.06 profit. I also prepared SQL queries and a Power BI build guide. The results are descriptive and point to questions for deeper cost and customer analysis.

## Interview questions and short model answers
1. **What was the project goal?** Analyze sales, profit, order, discount, shipping, and customer patterns in the supplied Superstore data.
2. **What does one row represent?** A product line on an order, so an order can have multiple rows.
3. **Why count distinct Order IDs?** Counting rows would overstate the number of orders when an order has several product lines.
4. **Why standardize column names?** Consistent snake_case names are easier to use in Python, SQL, and DAX.
5. **How did you handle duplicates?** Removed exact duplicate rows and reported the before/after row counts; this file had 0 exact duplicates.
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
