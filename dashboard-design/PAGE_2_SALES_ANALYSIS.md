# Page 2: Sales Analysis Dashboard

## Purpose
Deep-dive into sales performance by multiple dimensions. Designed for sales managers and analysts.

---

## Page Structure

### Header: Global Slicers (Sticky)
- **Date Slicer**: Dropdown for date ranges (Month/Quarter/Year)
- **Region Slicer**: Multi-select buttons (North, South, East, West, Central)
- **Product Category Slicer**: Multi-select dropdown
- **Salesperson Slicer**: Dropdown/search field
- **Customer Segment Slicer**: Buttons (Enterprise, Mid-Market, SMB, All)
- **Reset Button**: Clear all filters
- KPI Summary: Total Sales | Total Orders | Avg Order Value (small cards)

---

## Main Visualizations (2x2 Grid)

### Chart 1: Sales by Month (Line Chart with Forecast)
- **Type**: Line chart with confidence interval
- **Series**: 
  - Actual Sales (solid line, blue)
  - Prior Year Sales (dashed line, light gray)
  - Forecast (dotted line, orange)
- **Size**: 50% width × 40% height (top-left)
- **X-Axis**: Month (Jan-Dec or custom date range)
- **Y-Axis**: Sales ($)
- **Data Labels**: Every 3rd month
- **Key Insight**: Seasonal patterns, YoY comparison, forecast accuracy
- **Interaction**: Hover for exact values, click to drill-through

### Chart 2: Sales by Region (Column Chart)
- **Type**: Clustered column chart
- **Series**: [Total Sales] by Region
- **Secondary Series**: [Target Sales] as a line overlay
- **Size**: 50% width × 40% height (top-right)
- **Colors**: Each region unique color (matching donut from page 1)
- **Data Labels**: Yes
- **Sort**: Descending by sales
- **Key Insight**: Regional performance ranking
- **Interaction**: Click region to highlight in other charts

### Chart 3: Sales by Salesperson (Horizontal Bar Chart)
- **Type**: Horizontal bar chart
- **Series**: [Total Sales] by Salesperson
- **Size**: 50% width × 40% height (bottom-left)
- **Limit**: Top 15 salespeople (use dynamic rank)
- **Colors**: 
  - Green if > 100% of target
  - Yellow if 90-100% of target
  - Red if < 90% of target
- **Secondary Metric**: [Total Orders] as data label
- **Sort**: Descending by sales
- **Key Insight**: Sales rep performance ranking
- **Interaction**: Click salesperson to filter other visuals

### Chart 4: Sales by Product Category (Stacked Column)
- **Type**: Stacked column chart
- **Series**: Sales stacked by Product Category
- **X-Axis**: Month or Region (switchable via button)
- **Size**: 50% width × 40% height (bottom-right)
- **Colors**: Different color per category
- **Data Labels**: On total only
- **Key Insight**: Product mix evolution, category performance
- **Interaction**: Legend toggles visibility (show/hide categories)

---

## Lower Section: Performance Tables (Expandable)

### Table 1: Sales Performance Summary (Tab 1)
- **Columns**:
  1. Salesperson Name
  2. Region
  3. Total Sales ($)
  4. # Orders
  5. Avg Order Value
  6. % of Total Sales
  7. Target (if region-specific)
  8. Achievement %
  9. Trend (↑/→/↓ with sparkline)

- **Sorting**: Configurable (default: Sales descending)
- **Conditional Formatting**:
  - Achievement % > 110% = Green
  - Achievement % 90-110% = White
  - Achievement % < 90% = Light Red
- **Totals Row**: Yes, showing aggregates
- **Row Limit**: Top 20 salespeople
- **Exportable**: Yes (to Excel)

### Table 2: Product Performance (Tab 2)
- **Columns**:
  1. Product Category
  2. Product Name
  3. Units Sold
  4. Total Sales ($)
  5. Avg Price per Unit
  6. Gross Margin %
  7. % of Total Sales
  8. Trend (vs prior year)

- **Sorting**: Sales descending
- **Row Grouping**: By Category (expandable)
- **Drill-through**: Click product → Profitability page

---

## Right Sidebar: Key Metrics & Filters

### Active Filters Summary
Shows currently applied filters in a clean layout:
```
📊 Current Filter Selection:
Region: North, Central
Category: Electronics, Software
Salesperson: Top 10 only
Date Range: Last 12 Months
```

### Quick Stats
```
Total Sales: $45.2M
Total Orders: 2,847
Avg Order Value: $15,885
Best Performer: John Smith ($4.2M)
```

### Drill-Through Buttons
- [View All Transactions →]
- [Analyze Profitability →]
- [Customer Analysis →]

---

## Advanced Features

### Dynamic Segmentation Toggle
Buttons to switch analysis dimension:
- [ ] By Salesperson
- [ ] By Region
- [ ] By Product
- [ ] By Customer Segment
(Updates Chart 2 X-axis accordingly)

### Variance Analysis
Optional visualization showing:
- Actual vs Target
- Waterfall breakdown of variance by region/salesperson
- Most impactful drivers of over/under-achievement

### Forecast Section
If historical forecast data available:
- Actual vs Forecast chart
- Forecast accuracy metric
- Forecast confidence interval

---

## Interactivity & Navigation

### Cross-Filtering Rules
- Region filter → Filters all charts to that region
- Salesperson filter → Shows only that person's sales trend
- Category filter → Products and region mix filtered
- Date filter → Timeline updates globally
- Segment filter → All metrics filtered to segment

### Drill-Through Options
1. **From Salesperson** → Transaction Details page (salesperson highlighted)
2. **From Region** → Sales Analysis filtered to region
3. **From Product** → Profitability Analysis (product highlighted)
4. **From Order** → Customer Analysis (customer highlighted)

### Bookmarks
- **Bookmark 1: "By Salesperson"** - Configured to show top salespeople
- **Bookmark 2: "By Region"** - Regional performance view
- **Bookmark 3: "YoY Comparison"** - Prior year comparison enabled
- **Bookmark 4: "Top Products"** - Top 10 products by sales

---

## Measures & Metrics Used

### Primary Measures
- [Total Sales]
- [Total Orders]
- [Average Order Value]
- [Total Quantity]

### Comparative Measures
- [Sales PY] (for YoY comparison)
- [Target Sales] (for achievement)
- [Sales YTD] (cumulative)

### Derived Metrics (calculated in visuals)
- Rank: Ranking salespeople by sales
- % of Total: Each salesperson's share
- Trend: Sales growth rate

---

## Design Guidelines

### Color Coding
- **Blue**: Current period (2024)
- **Gray**: Prior period (2023)
- **Orange**: Target/Forecast
- **Green**: Over-achievement (>100%)
- **Red**: Under-achievement (<90%)

### Performance Indicators
- ↑ Green: Growing trend
- → Gray: Flat trend
- ↓ Red: Declining trend

### Typography
- Chart Titles: 14pt, Semi-bold
- Axis Labels: 11pt, Regular
- Data Labels: 10pt, Regular
- Table Headers: 12pt, Semi-bold

---

## Mobile/Print Considerations

### Responsive Layout
- On mobile: Charts stack vertically
- Table scrolls horizontally
- Slicers collapse into dropdown menu

### Print Layout
- Page breaks after Chart 4
- Tables print on separate pages
- Header repeats on each page
- Landscape orientation recommended

---

## Common Analysis Scenarios

### Scenario 1: "Who's the top performer?"
**Use:** Bar chart sorted by sales, look at green highlight for achievement

### Scenario 2: "Which region is growing fastest?"
**Use:** Line chart YoY comparison, note slope of current year vs prior year

### Scenario 3: "What caused the sales spike in March?"
**Use:** Drill-through to transaction level, filter by date, analyze by product/region/salesperson

### Scenario 4: "Are we maintaining market share?"
**Use:** Compare % of Total sales period-over-period

### Scenario 5: "Which products are trending up?"
**Use:** Product tab, sort by trend metric, identify accelerating categories

---

## Interview Discussion Points

### "Walk me through the sales analysis"
**Response:**
1. "This dashboard breaks down sales by three key dimensions: Region, Salesperson, and Product."
2. "The top charts show trend (YoY comparison), regional distribution, and individual rep performance."
3. "I can instantly identify top performers (green bars) vs those needing support (red bars)."
4. "The tables provide transaction-level detail for root cause analysis."

### "How would you identify a problem?"
**Response:**
- "Red bars in the salesperson chart indicate below-target performance."
- "I'd click that salesperson to filter all charts to their data."
- "Then compare their monthly trend to the company trend to see if they're falling behind."
- "Finally, drill into their transactions to see which product/region is underperforming."

### "How do you handle data volume?"
**Response:**
- "With 2,500 transactions, this page stays performant by limiting detail tables to top 20."
- "Drill-through provides access to full transaction data when needed."
- "Slicers allow users to narrow scope before viewing all rows."

### "Why these specific charts?"
**Response:**
- "Line chart shows trends - critical for spotting acceleration/deceleration."
- "Column charts compare across regions - easy to rank and identify leaders."
- "Bar chart for salespeople - easier to read many names than a column chart."
- "Stacked columns show product mix - tells if revenue growth is from volume or mix."

