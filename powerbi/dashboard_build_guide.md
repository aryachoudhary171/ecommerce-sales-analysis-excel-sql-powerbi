# Power BI dashboard build guide

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
