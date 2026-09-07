# Pages 3-6: Dashboard Design Summary

## Page 3: Customer Analysis

### Purpose
Understand customer behavior, segmentation, and lifetime value.

### Key Visuals
1. **Customer Metrics (Top)**: Total Customers | New Customers | Repeat Customers | Avg Revenue/Customer
2. **Customer Growth Trend (Line Chart)**: Cumulative customer count by month with new customer overlay
3. **Top 10 Customers (Horizontal Bar)**: Revenue contribution, orders, segment indicator
4. **Customers by Segment (Donut)**: Enterprise vs Mid-Market vs SMB distribution
5. **Revenue Contribution (Pareto Chart)**: Shows 80/20 rule - cumulative % of revenue vs customer count
6. **Customer Tenure (Scatter)**: Years as customer vs total revenue (size = frequency)

### Measures Used
- Total Customers
- New Customers (first purchase in period)
- Repeat Customers (multiple purchases in period)
- Customer Lifetime Value (Avg Revenue per Customer × expected lifetime)
- Customer Acquisition Cost (optional, if marketing data available)

### Drill-Through
Click customer → Customer detail page showing:
- All transactions (order history)
- Purchase frequency timeline
- Product preferences
- Segment classification
- Churn risk score

### Slicers
- Date range (to see customer acquisition by cohort)
- Segment (Enterprise, Mid-Market, SMB)
- Region
- Product category

---

## Page 4: Profitability Analysis

### Purpose
Analyze margins, costs, and profit drivers by dimension.

### Key Visuals
1. **Profit Waterfall Chart (Center Stage)**
   - Starting: Total Sales
   - Subtract: Total Cost
   - = Gross Profit
   - Shows contribution of cost variance to profit change

2. **Margin by Region (Horizontal Bar)**
   - Gross Margin % by region
   - Color-coded: >40% = green, 30-40% = yellow, <30% = red
   - Data labels showing actual margin $

3. **Margin by Product Category (Column)**
   - Category on X-axis
   - Gross Margin % on Y-axis
   - Secondary axis: Volume (units sold)
   - Identify high-margin, low-volume vs low-margin, high-volume

4. **Margin Trend (Area Chart)**
   - Gross Margin % trend over time
   - Prior year comparison (dashed)
   - Highlights compression/expansion

5. **Cost vs Sales by Segment (Scatter)**
   - X-axis: Total Sales
   - Y-axis: Total Cost
   - Size: Number of orders
   - Color: Segment
   - Shows which segment has best cost-to-sales ratio

6. **Profitability Table**
   - Region | Category | Product | Quantity | Sales | Cost | Profit | Margin %
   - Sorted: Lowest margin first (problem identification)
   - Conditional formatting: Margin % color-coded

### Measures Used
- Total Sales
- Total Cost
- Gross Profit
- Gross Margin %
- Profit Growth %
- Profit by Region/Product/Segment

### Key Insights to Highlight
- Identify low-margin products (candidates for discontinuation or price increase)
- Analyze cost trends (rising COGS as inflation indicator)
- Segment performance (which is most profitable?)
- Regional efficiency (same product different margins?)

### Slicers
- Date range
- Region
- Product category
- Customer segment

---

## Page 5: Forecast & Targets

### Purpose
Compare actuals against targets and show forward-looking forecast.

### Key Visuals
1. **Actual vs Target vs Forecast (Combination Chart)**
   - Column: Actual Sales (solid, blue)
   - Line: Target Sales (orange)
   - Line: Forecast Sales (green dashed)
   - X-axis: Months (past and future)
   - Clear distinction: Historical shaded vs forecast shaded differently

2. **Target Achievement % by Region (Column)**
   - Region on X-axis
   - % of target on Y-axis
   - Reference line at 100%
   - Color zones: Green (>100%), Yellow (90-100%), Red (<90%)

3. **Annual Forecast Summary (Large KPI)**
   - Projected Annual Sales
   - Comparison: Annual Target
   - Variance: $X ahead/behind

4. **Forecast Confidence Interval (Area Chart)**
   - Shows lower-bound, actual forecast, upper-bound
   - Indicates uncertainty in forecast
   - Based on historical forecast accuracy

5. **Days to Target Achievement (Gauge Chart)**
   - Based on current run rate
   - Dial shows days remaining vs 365 days
   - Red: Won't achieve (>365 days)
   - Yellow: At risk (180-365 days)
   - Green: On track (<180 days)

6. **Monthly Variance Analysis (Waterfall)**
   - Current month target
   - Variance by region
   - Variance by product
   - = Total variance (gap from target)

### Measures Used
- Total Sales
- Target Sales
- Annual Forecast (calculated from YTD run rate)
- Target Achievement %
- Variance to Target
- Sales Forecast (if forecast data available)

### Data Requirements
- DimTarget table with actual targets by month/region
- Historical forecast data (if available)
- Seasonal adjustment factors (if using advanced forecasting)

### Interpretation Guide
```
✓ Chart above 100% line = On track or exceeding
⚠ Chart between 90-100% = At risk, needs attention
❌ Chart below 90% = Significant shortfall, action required
```

### Slicers
- Date range (focus on current year)
- Region (see regional targets vs achievement)
- Product category (if targets exist by category)

---

## Page 6: Detailed Drill-Through

### Purpose
Transaction-level detail accessible from other pages via drill-through.

### Entry Points (Drill-Through from)
- Region (Page 1, Page 2)
- Product Category (Page 1, Page 2, Page 4)
- Customer (Page 3)
- Salesperson (Page 2)
- Top 10 Customers table (Page 1)

### Main Visual: Transaction Table
**Columns:**
1. OrderID (link to source, if applicable)
2. OrderDate (sortable)
3. Customer Name (drill-through to customer profile)
4. Product Name (drill-through to product analysis)
5. Quantity
6. Unit Price
7. Discount %
8. Sales ($)
9. Cost ($)
10. Profit ($)
11. Margin %
12. Salesperson (if available)
13. Region

### Features
- **Sort**: Multi-column sort (Date desc, Customer asc, etc.)
- **Filter**: Quick filter on any column (search on text columns)
- **Conditional Formatting**: 
  - Margin % > 50% = light green
  - Margin % 30-50% = white
  - Margin % < 30% = light red
  - Negative margin = red
- **Row Limit**: 1,000 rows (use pagination for larger result sets)
- **Export**: Download visible rows to Excel
- **Totals Row**: Yes - shows sums for all numeric columns

### Drill-Down Breadcrumb
Shows drill path:
```
Sales Analysis > Region: North > Salesperson: John Smith > Transactions
[← Back to previous level]
```

### Quick Insights (Top of Page)
```
📊 Drill-Through Summary:
Filter: North region | Last 12 Months
Transactions: 342 orders | $4.2M sales | $1.9M profit | 45.2% margin

Top Product: Electronics (234 units, 68% of sales)
Best Day: March 15 (42 orders, $180K)
Largest Order: $45,800 (March 22)
```

### Performance Optimization
- Only load data for filtered context
- Use "Show top 1,000 rows" by default
- Implement pagination: "Load next 1,000"
- Don't load customer details in table (click for detail page)

### Secondary Visuals (if space)
- **Recent Transaction Sparkline**: Last 30 days of orders (small area chart)
- **Customer Distribution**: Pie of top 5 customers in visible data
- **Product Distribution**: Bar of top 5 products in visible data

---

## Cross-Page Navigation

### Bookmark Setup
Create bookmarks to switch between analysis views:
- **View 1: Executive Summary** → Page 1
- **View 2: Detailed Analysis** → Page 2 with default settings
- **View 3: Profitability Deep-Dive** → Page 4
- **View 4: Forecast Review** → Page 5
- **View 5: Transaction Detail** → Page 6

### Button Navigation
Place navigation buttons consistently:
```
┌────────────────────────────────────┐
│ [Executive] [Sales] [Customer]    │
│ [Profit] [Forecast] [Transactions] │
└────────────────────────────────────┘
```

### Global Reset Button
- Resets all slicers to default
- Returns to Page 1
- Clears any drill-through filters

---

## Measure Summary Across All Pages

### Core Metrics (all pages)
- [Total Sales]
- [Gross Profit]
- [Gross Margin %]
- [Total Orders]
- [Average Order Value]

### Time Intelligence (Pages 1, 2, 5)
- [YoY Sales %]
- [Sales YTD]
- [Sales MTD]
- [Sales PY]
- [Sales L12M]

### Target & Performance (Pages 1, 2, 5)
- [Target Sales]
- [Target Achievement %]
- [Variance to Target]
- [Annual Forecast]

### Customer Metrics (Page 3)
- [Total Customers]
- [New Customers]
- [Repeat Customers]
- [Avg Revenue per Customer]

### Profitability (Pages 4, 6)
- [Total Cost]
- [Profit by Region]
- [Margin by Product]
- [Profit Growth %]

---

## Mobile Responsiveness

### Phone Layout (<600px)
- Stack all charts vertically
- Slicers collapse to dropdown
- Table columns: OrderID, Date, Sales, Profit
- Scroll horizontally for additional columns

### Tablet Layout (600-1200px)
- 2-column layout for charts
- Slicers side-by-side
- All table columns visible
- Larger touch targets

### Desktop (>1200px)
- Full design as described
- Multi-column layouts
- Hover interactions on charts

