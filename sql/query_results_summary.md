# SQL query results sanity check

The 12 MySQL queries in `03_analysis_queries.sql` were independently reproduced with pandas on 9,994 cleaned rows. The tables below are representative expected results for checking a MySQL import.

## Yearly sales, profit, orders, and growth

| order_year | sales | profit | orders | profit_margin_pct | sales_yoy_pct | profit_yoy_pct |
|---|---|---|---|---|---|---|
| 2,014 | 484,247.50 | 49,543.97 | 969 | 10.23 | — | — |
| 2,015 | 470,532.51 | 61,618.60 | 1,038 | 13.10 | -2.83 | 24.37 |
| 2,016 | 609,205.60 | 81,795.17 | 1,315 | 13.43 | 29.47 | 32.74 |
| 2,017 | 733,215.26 | 93,439.27 | 1,687 | 12.74 | 20.36 | 14.24 |

## Top 10 customers by profit

| customer_id | customer_name | profit |
|---|---|---|
| TC-20980 | Tamara Chand | 8,981.32 |
| RB-19360 | Raymond Buch | 6,976.10 |
| SC-20095 | Sanjit Chand | 5,757.41 |
| HL-15040 | Hunter Lopez | 5,622.43 |
| AB-10105 | Adrian Barton | 5,444.81 |
| TA-21385 | Tom Ashbrook | 4,703.79 |
| CM-12385 | Christopher Martinez | 3,899.89 |
| KD-16495 | Keith Dawkins | 3,038.63 |
| AR-10540 | Andy Reiter | 2,884.62 |
| DR-12940 | Daniel Raglin | 2,869.08 |

## Category and sub-category

| category | sub_category | sales | profit | profit_margin_pct |
|---|---|---|---|---|
| Technology | Phones | 330,007.05 | 44,515.73 | 13.49 |
| Furniture | Chairs | 328,449.10 | 26,590.17 | 8.10 |
| Office Supplies | Storage | 223,843.61 | 21,278.83 | 9.51 |
| Furniture | Tables | 206,965.53 | -17,725.48 | -8.56 |
| Office Supplies | Binders | 203,412.73 | 30,221.76 | 14.86 |
| Technology | Machines | 189,238.63 | 3,384.76 | 1.79 |
| Technology | Accessories | 167,380.32 | 41,936.64 | 25.05 |
| Technology | Copiers | 149,528.03 | 55,617.82 | 37.20 |
| Furniture | Bookcases | 114,880.00 | -3,472.56 | -3.02 |
| Office Supplies | Appliances | 107,532.16 | 18,138.01 | 16.87 |
| Furniture | Furnishings | 91,705.16 | 13,059.14 | 14.24 |
| Office Supplies | Paper | 78,479.21 | 34,053.57 | 43.39 |
| Office Supplies | Supplies | 46,673.54 | -1,189.10 | -2.55 |
| Office Supplies | Art | 27,118.79 | 6,527.79 | 24.07 |
| Office Supplies | Envelopes | 16,476.40 | 6,964.18 | 42.27 |
| Office Supplies | Labels | 12,486.31 | 5,546.25 | 44.42 |
| Office Supplies | Fasteners | 3,024.28 | 949.52 | 31.40 |

## Discount band

| discount_band | avg_profit | profit | rows |
|---|---|---|---|
| 0% | 66.90 | 320,987.60 | 4,798 |
| 1-10% | 96.06 | 9,029.18 | 94 |
| 11-20% | 24.74 | 91,756.30 | 3,709 |
| 21-30% | -45.68 | -10,369.28 | 227 |
| >30% | -107.21 | -125,006.78 | 1,166 |

## Discounted vs zero-discount profit by category

| category | discounted | avg_profit | total_profit | line_items |
|---|---|---|---|---|
| Furniture | 0.00 | 69.54 | 58,133.08 | 836 |
| Furniture | 1.00 | -30.88 | -39,681.80 | 1,285 |
| Office Supplies | 0.00 | 41.71 | 130,506.11 | 3,129 |
| Office Supplies | 1.00 | -2.77 | -8,015.31 | 2,897 |
| Technology | 0.00 | 158.88 | 132,348.42 | 833 |
| Technology | 1.00 | 12.93 | 13,106.53 | 1,014 |

## Ship mode

| ship_mode | avg_shipping_days | sales | profit |
|---|---|---|---|
| First Class | 2.18 | 351,428.42 | 48,969.84 |
| Same Day | 0.04 | 128,363.12 | 15,891.76 |
| Second Class | 3.24 | 459,193.57 | 57,446.64 |
| Standard Class | 5.01 | 1,358,215.74 | 164,088.79 |

## Loss-making sub-categories

| sub_category | sales | profit | profit_margin_pct |
|---|---|---|---|
| Tables | 206,965.53 | -17,725.48 | -8.56 |
| Bookcases | 114,880.00 | -3,472.56 | -3.02 |
| Supplies | 46,673.54 | -1,189.10 | -2.55 |

## Top 10 customers by sales

| customer_id | customer_name | segment | sales |
|---|---|---|---|
| SM-20320 | Sean Miller | Home Office | 25,043.05 |
| TC-20980 | Tamara Chand | Corporate | 19,052.22 |
| RB-19360 | Raymond Buch | Consumer | 15,117.34 |
| TA-21385 | Tom Ashbrook | Home Office | 14,595.62 |
| AB-10105 | Adrian Barton | Consumer | 14,473.57 |
| KL-16645 | Ken Lonsdale | Consumer | 14,175.23 |
| SC-20095 | Sanjit Chand | Consumer | 14,142.33 |
| HL-15040 | Hunter Lopez | Consumer | 12,873.30 |
| SE-20110 | Sanjit Engle | Consumer | 12,209.44 |
| CC-12370 | Christopher Conant | Consumer | 12,129.07 |
| TS-21370 | Todd Sumrall | Corporate | 11,891.75 |
| GT-14710 | Greg Tran | Consumer | 11,820.12 |
| BM-11140 | Becky Martin | Consumer | 11,789.63 |
| SV-20365 | Seth Vernon | Consumer | 11,470.95 |
| CJ-12010 | Caroline Jumper | Consumer | 11,164.97 |
| CL-12565 | Clay Ludtke | Consumer | 10,880.55 |
| ME-17320 | Maria Etezadi | Home Office | 10,663.73 |
| KF-16285 | Karen Ferguson | Home Office | 10,604.27 |
| BS-11365 | Bill Shonely | Corporate | 10,501.65 |
| EH-13765 | Edward Hooks | Corporate | 10,310.88 |
| JL-15835 | John Lee | Consumer | 9,799.92 |
| GT-14635 | Grant Thornton | Corporate | 9,351.21 |
| HW-14935 | Helen Wasserman | Corporate | 9,300.25 |
| TB-21400 | Tom Boeckenhauer | Consumer | 9,133.99 |
| PF-19120 | Peter Fuller | Consumer | 9,062.86 |
| CM-12385 | Christopher Martinez | Consumer | 8,954.02 |
| JD-16150 | Justin Deggeller | Corporate | 8,828.03 |
| JE-15715 | Joe Elijah | Consumer | 8,697.84 |
| LA-16780 | Laura Armstrong | Corporate | 8,673.22 |
| PK-19075 | Pete Kriz | Consumer | 8,646.93 |

## Region by year

| order_year | region | orders | sales | profit |
|---|---|---|---|---|
| 2,014 | Central | 230 | 103,838.16 | 539.55 |
| 2,014 | East | 261 | 128,680.46 | 17,059.61 |
| 2,014 | South | 165 | 103,845.84 | 11,879.12 |
| 2,014 | West | 313 | 147,883.03 | 20,065.69 |
| 2,015 | Central | 234 | 102,874.22 | 11,716.80 |
| 2,015 | East | 296 | 156,332.06 | 21,091.01 |
| 2,015 | South | 170 | 71,359.98 | 8,318.59 |
| 2,015 | West | 338 | 139,966.25 | 20,492.19 |
| 2,016 | Central | 305 | 147,429.38 | 19,899.16 |
| 2,016 | East | 374 | 180,685.82 | 20,141.60 |
| 2,016 | South | 214 | 93,610.22 | 17,702.81 |
| 2,016 | West | 422 | 187,480.18 | 24,051.61 |
| 2,017 | Central | 406 | 147,098.13 | 7,550.84 |
| 2,017 | East | 470 | 213,082.90 | 33,230.56 |
| 2,017 | South | 273 | 122,905.86 | 8,848.91 |
| 2,017 | West | 538 | 250,128.37 | 43,808.96 |

## Segment by category averages

| segment | category | avg_sales | avg_profit |
|---|---|---|---|
| Consumer | Furniture | 351.35 | 6.28 |
| Consumer | Office Supplies | 116.39 | 18.01 |
| Consumer | Technology | 427.34 | 74.45 |
| Corporate | Furniture | 354.52 | 11.74 |
| Corporate | Office Supplies | 126.75 | 22.10 |
| Corporate | Technology | 444.86 | 79.72 |
| Home Office | Furniture | 336.83 | 10.71 |
| Home Office | Office Supplies | 115.31 | 24.03 |
| Home Office | Technology | 535.98 | 89.15 |

## Monthly sales and running total

| month | sales | running_sales |
|---|---|---|
| 2014-01-01 00:00:00 | 14,236.90 | 14,236.90 |
| 2014-02-01 00:00:00 | 4,519.89 | 18,756.79 |
| 2014-03-01 00:00:00 | 55,691.01 | 74,447.80 |
| 2014-04-01 00:00:00 | 28,295.35 | 102,743.14 |
| 2014-05-01 00:00:00 | 23,648.29 | 126,391.43 |
| 2014-06-01 00:00:00 | 34,595.13 | 160,986.56 |
| 2014-07-01 00:00:00 | 33,946.39 | 194,932.95 |
| 2014-08-01 00:00:00 | 27,909.47 | 222,842.42 |
| 2014-09-01 00:00:00 | 81,777.35 | 304,619.77 |
| 2014-10-01 00:00:00 | 31,453.39 | 336,073.16 |
| 2014-11-01 00:00:00 | 78,628.72 | 414,701.88 |
| 2014-12-01 00:00:00 | 69,545.62 | 484,247.50 |
| 2015-01-01 00:00:00 | 18,174.08 | 502,421.57 |
| 2015-02-01 00:00:00 | 11,951.41 | 514,372.98 |
| 2015-03-01 00:00:00 | 38,726.25 | 553,099.24 |
| 2015-04-01 00:00:00 | 34,195.21 | 587,294.45 |
| 2015-05-01 00:00:00 | 30,131.69 | 617,426.13 |
| 2015-06-01 00:00:00 | 24,797.29 | 642,223.42 |
| 2015-07-01 00:00:00 | 28,765.33 | 670,988.75 |
| 2015-08-01 00:00:00 | 36,898.33 | 707,887.08 |
| 2015-09-01 00:00:00 | 64,595.92 | 772,483.00 |
| 2015-10-01 00:00:00 | 31,404.92 | 803,887.92 |
| 2015-11-01 00:00:00 | 75,972.56 | 879,860.49 |
| 2015-12-01 00:00:00 | 74,919.52 | 954,780.01 |
| 2016-01-01 00:00:00 | 18,542.49 | 973,322.50 |
| 2016-02-01 00:00:00 | 22,978.81 | 996,301.31 |
| 2016-03-01 00:00:00 | 51,715.88 | 1,048,017.19 |
| 2016-04-01 00:00:00 | 38,750.04 | 1,086,767.23 |
| 2016-05-01 00:00:00 | 56,987.73 | 1,143,754.96 |
| 2016-06-01 00:00:00 | 40,344.53 | 1,184,099.49 |
| 2016-07-01 00:00:00 | 39,261.96 | 1,223,361.45 |
| 2016-08-01 00:00:00 | 31,115.37 | 1,254,476.83 |
| 2016-09-01 00:00:00 | 73,410.02 | 1,327,886.85 |
| 2016-10-01 00:00:00 | 59,687.75 | 1,387,574.60 |
| 2016-11-01 00:00:00 | 79,411.97 | 1,466,986.56 |
| 2016-12-01 00:00:00 | 96,999.04 | 1,563,985.61 |
| 2017-01-01 00:00:00 | 43,971.37 | 1,607,956.98 |
| 2017-02-01 00:00:00 | 20,301.13 | 1,628,258.11 |
| 2017-03-01 00:00:00 | 58,872.35 | 1,687,130.47 |
| 2017-04-01 00:00:00 | 36,521.54 | 1,723,652.00 |
| 2017-05-01 00:00:00 | 44,261.11 | 1,767,913.11 |
| 2017-06-01 00:00:00 | 52,981.73 | 1,820,894.84 |
| 2017-07-01 00:00:00 | 45,264.42 | 1,866,159.25 |
| 2017-08-01 00:00:00 | 63,120.89 | 1,929,280.14 |
| 2017-09-01 00:00:00 | 87,866.65 | 2,017,146.79 |
| 2017-10-01 00:00:00 | 77,776.92 | 2,094,923.72 |
| 2017-11-01 00:00:00 | 118,447.82 | 2,213,371.54 |
| 2017-12-01 00:00:00 | 83,829.32 | 2,297,200.86 |

## State profit ranking (top 15)

| state | profit | profit_rank |
|---|---|---|
| California | 76,381.39 | 1 |
| New York | 74,038.55 | 2 |
| Washington | 33,402.65 | 3 |
| Michigan | 24,463.19 | 4 |
| Virginia | 18,597.95 | 5 |
| Indiana | 18,382.94 | 6 |
| Georgia | 16,250.04 | 7 |
| Kentucky | 11,199.70 | 8 |
| Minnesota | 10,823.19 | 9 |
| Delaware | 9,977.37 | 10 |
| New Jersey | 9,772.91 | 11 |
| Wisconsin | 8,401.80 | 12 |
| Rhode Island | 7,285.63 | 13 |
| Maryland | 7,031.18 | 14 |
| Massachusetts | 6,785.50 | 15 |

## Validation note

Order counts use distinct `order_id`, not line count. Margins are profit divided by sales. Monthly running totals are sorted by calendar month. All amounts are computed from the cleaned source file.
