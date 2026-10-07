# Recreate the formula summaries as real PivotTables

The workbook uses formulas for summaries because the Python/JavaScript workbook writer does not reliably export native Excel PivotTables. To make a PivotTable in desktop Excel:

1. Open `ecommerce_sales_analysis.xlsx` and go to `Cleaned_Data`.
2. Click inside the data and choose **Insert > PivotTable > From Table/Range**.
3. Select **New Worksheet** and confirm. Rename the new sheet for the analysis.
4. Drag the requested fields into Rows, Columns, Values, and Filters. For distinct order counts, tick **Add this data to the Data Model** when creating the PivotTable, then set Order ID to **Distinct Count**.
5. In Value Field Settings choose Sum, Average, or Count as appropriate. For margins, add a calculated measure (profit divided by sales) or place summary totals beside the PivotTable and calculate `Profit / Sales`.
6. Insert a PivotChart from the PivotTable and add slicers for Year, Region, or Segment.

Suggested layouts: Year in Rows with Sales/Profit in Values; Ship Mode in Rows with Average of Shipping Days; Segment in Rows and Category in Columns with Average Sales/Profit; Category and Sub-Category in Rows with Sales/Profit; Discount Band in Rows with Profit; Region in Rows and Year in Columns with distinct Order ID; Year in Rows with Sales, Profit, and distinct Orders for YoY calculations.

PivotTables are optional additions; the existing formula summary tabs remain available as a transparent reference.
