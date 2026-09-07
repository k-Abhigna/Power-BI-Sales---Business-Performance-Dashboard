# Page 1: Executive Overview Dashboard

## Purpose
High-level business summary for C-suite and executive stakeholders. Designed for 2-minute consumption showing overall health and key trends.

---

## Layout & Visual Hierarchy

### Top Section: KPI Cards (Row 1)
Display in a 6-card row:

1. **Total Sales** (Large KPI Card)
   - Metric: [Total Sales]
   - Format: $X.XM
   - Comparison: YoY growth rate
   - Example: $45.2M ↑ +14% YoY
   - Color: Blue (Primary)

2. **Gross Profit** (Large KPI Card)
   - Metric: [Gross Profit]
   - Format: $X.XM
   - Comparison: YoY growth
   - Example: $18.3M ↑ +12% YoY
   - Color: Green (Profit)

3. **Gross Margin %** (Large KPI Card)
   - Metric: [Gross Margin %]
   - Format: XX.X%
   - Comparison: Change from PY
   - Example: 42.1% ↓ -1.2pp YoY
   - Color: Teal (Efficiency)

4. **YoY Growth %** (Large KPI Card)
   - Metric: [YoY Sales %]
   - Format: +XX.X%
   - Comparison: Previous month growth
   - Example: +14.2%
   - Color: Green/Red (if positive/negative)
   - Sparkline: Last 12 months trend

5. **Target Achievement %** (Large KPI Card)
   - Metric: [Target Achievement %]
   - Format: XXX% / 100%
   - Comparison: $X.XM variance
   - Example: 112% / 100%
   - Status: Green (>100%), Yellow (90-100%), Red (<90%)

6. **Total Customers** (Large KPI Card)
   - Metric: [Total Customers]
   - Format: X,XXX
   - Comparison: New customers this period
   - Example: 8,432 (+142 new)
   - Color: Purple (Customer)

---

### Middle Section: Charts (Row 2)

#### Chart A: Monthly Sales vs Target (Combination Chart)
- **Type**: Column + Line combo chart
- **Series 1 (Column)**: [Total Sales] by Month
- **Series 2 (Line)**: [Target Sales] by Month
- **Size**: 40% of page width
- **Key Insight**: Shows monthly performance against plan
- **Interactivity**: Drill-through to Sales Analysis page
- **Colors**: Sales = Blue, Target = Orange dashed line
- **Data Labels**: Yes, on both series
- **Legend**: Top, horizontal

#### Chart B: Sales by Region (Donut/Pie Chart)
- **Type**: Donut chart (shows hole in middle for label)
- **Series**: [Total Sales] by Region
- **Size**: 30% of page width
- **Key Insight**: Revenue contribution by geographic region
- **Interactivity**: Click region to filter entire page
- **Data Labels**: Region name + $ amount + %
- **Colors**: Use corporate color palette
- **Legend**: Inside donut or adjacent

#### Chart C: Sales by Product Category (Bar Chart)
- **Type**: Horizontal bar chart
- **Series**: [Total Sales] by Category
- **Size**: 30% of page width
- **Sort**: Descending by sales value
- **Key Insight**: Top-performing product categories
- **Data Labels**: Yes, showing amounts
- **Colors**: Gradient from dark to light
- **Legend**: None (categories labeled on axis)

---

### Bottom Section: Trends & Insights (Row 3)

#### Chart D: Monthly Profit Trend (Area Chart)
- **Type**: Stacked area chart
- **Series 1**: [Gross Profit]
- **Series 2**: [Gross Margin %] on secondary axis
- **Size**: 50% of page width
- **Key Insight**: Profitability trend over time
- **Colors**: Profit = Blue, Margin % = Green
- **Data Labels**: Minimal (show on hover via tooltip)
- **Legends**: Top, 2 series

#### Chart E: Top 10 Customers (Table/Bar Chart)
- **Type**: Horizontal bar chart OR Table visual
- **Series**: [Total Sales] by Customer
- **Size**: 50% of page width
- **Sort**: Top 10 by sales descending
- **Key Insight**: Customer concentration risk, key accounts
- **Columns** (if table): 
  - Customer Name
  - Total Sales ($)
  - # Orders
  - Segment
  - % of Total Sales
- **Conditional Formatting**: Top customer highlighted in green
- **Interactivity**: Drill-through to Customer Analysis

---

### Top-Right Corner: Executive Insights Text Box

#### Content
Dynamic text box showing:
```
📊 EXECUTIVE INSIGHTS

✓ Sales increased 14% YoY, driven by North region (+18%) 
  and Electronics category (+16%)

✓ Gross Margin declined 1.2pp despite volume growth - 
  investigate product mix shift toward lower-margin items

✓ Target Achievement at 112% - on pace to exceed annual goal
  by $1.2M

⚠ West region underperforming: only 87% of target after 9M
  - Recommend sales review for regional challenges

✓ Top customer (Acme Corp) represents 12% of total sales
  - Retention risk: ensure account management attention
```

### Implementation
- Use text box or R visual with dynamic content
- Generate using DAX calculations or Python/R visual
- Update monthly with new insights
- Format with emojis for quick scanning
- Keep to 4-6 bullet points maximum

---

### Slicers (Top Left Corner)

1. **Date Range Slicer** (Dropdown, single selection)
   - Default: Current Year
   - Options: Current Month, Current Quarter, Current Year, Last 12 Months, Custom Date Range
   - Position: Top-left

2. **Region Slicer** (Buttons, multiple selection)
   - Regions: North, South, East, West, Central, All
   - Position: Below Date slicer
   - Allow multi-select for comparing regions

3. **Reset All Slicers** Button
   - Clears all filters
   - Returns to default view
   - Position: Top-left corner

---

## Color Scheme

| Element | Color | Hex | Usage |
|---------|-------|-----|-------|
| Primary (Sales) | Blue | #0078D4 | Total Sales KPI, Sales charts |
| Profit | Green | #107C10 | Gross Profit, positive trends |
| Target/Goal | Orange | #FFB900 | Target lines, achievement |
| Efficiency | Teal | #00B4EF | Margin %, percentages |
| Alert/At-Risk | Yellow | #FFB900 | 90-100% achievement |
| Problem/Below Target | Red | #D83B01 | <90% achievement |
| Neutral/Background | Gray | #F3F2F1 | Backgrounds, borders |

---

## Recommended Dimensions & Measures

### Fact Table Columns Needed
- OrderDate, Sales, Quantity, Profit

### Dimension Columns Needed
- DimDate[Date, Month, Year, YearMonth]
- DimRegion[Region]
- DimProduct[Category]
- DimCustomer[CustomerName, Segment]

### Measures Needed
- Total Sales
- Gross Profit
- Gross Margin %
- YoY Sales %
- Target Achievement %
- Total Customers
- Sales by Region (implicit in chart)
- Sales by Category (implicit in chart)

---

## Interactivity & Drill-Through

### Cross-Filtering
- Clicking region in donut → filters sales chart to that region
- Clicking category in bar chart → shows only that category's top customers
- Date slicer → filters all charts globally

### Drill-Through Actions
- From KPI card → Sales Analysis page (filtered by selected metric)
- From Region chart → Sales Analysis page (region highlighted)
- From Top Customers → Customer Analysis page (customer highlighted)

### Tooltips
- Every chart should have enhanced tooltips showing:
  - 3-month trend sparkline
  - YoY comparison
  - % of total
  - Any relevant status indicator

---

## Design Guidelines

### Typography
- KPI Values: 48pt, Bold, Brand Color
- KPI Labels: 14pt, Regular, Dark Gray
- Chart Titles: 16pt, Semi-bold, Dark Gray
- Legend/Axis: 11pt, Regular, Medium Gray

### Spacing
- 20px padding inside containers
- 10px gap between charts
- 15px margin from page edges
- Balanced white space

### Accessibility
- Minimum contrast ratio 4.5:1 for text
- No information conveyed by color alone (use icons, labels)
- All charts have axis labels
- Alt text for all visuals

### Mobile Responsiveness
- Stack KPIs on smaller screens
- Consider horizontal scrolling for tables
- Larger touch targets for slicers (min 44px)

---

## Interview Discussion Points

### "Walk me through this dashboard"
**Response Framework:**
1. **Purpose**: "This is the executive overview designed for C-suite, showing health of the business in 2 minutes."
2. **Top Row**: "These 6 KPIs tell you the story - we're growing 14% YoY, maintaining healthy margins, and exceeding targets."
3. **Charts**: "The regional mix shows where sales are concentrated, and the profit trend identifies the profitability story."
4. **Insights**: "The text box at top-right automatically highlights key findings and any concerns for the executive to act on."

### "Why these specific KPIs?"
**Response:**
- **Total Sales**: Revenue is the primary metric; everything else is commentary
- **Gross Profit/Margin %**: Shows profitability, not just top-line growth
- **YoY Growth**: External stakeholders care about growth trajectory
- **Target Achievement**: Directly tied to incentives and strategy execution
- **Total Customers**: Leads indicator of future sales
- **Regional breakdown**: Identifies geographic performance variations

### "How do you ensure data accuracy?"
**Response:**
- "All measures are built on the fact table with proper filtering"
- "KPIs are compared monthly against source system totals"
- "Time intelligence uses proper DAX patterns (TOTALYTD, etc.)"
- "The page respects all filter context automatically"

