# Power BI Portfolio Project: Interview Guide

## Overview
This document provides talking points for every section of the dashboard. Use these frameworks to confidently explain technical decisions during your interview.

---

# PART 1: Data Preparation

## Question 1: "Tell me about your data model"

### Framework
```
1. Source → 2. Shape → 3. Validate → 4. Enrich → 5. Model
```

### Answer (2-3 minutes)
"I built a **star schema** with one fact table and four dimensions:

**FactSales** (2,500 transactions) contains:
- Business events: OrderID, OrderDate, Quantity, Sales, Cost
- Foreign keys to dimensions: CustomerID, ProductID, SalespersonID, RegionID
- Pre-calculated fields: Sales (UnitPrice × Quantity × (1 - Discount)), Profit (Sales - Cost × Quantity)

**Dimensions:**
- **DimDate** (731 rows): Every date 2023-2024, with fiscal attributes (Year, Quarter, Month, YearMonth)
- **DimCustomer** (100): Customer attributes (Name, Segment, Location)
- **DimProduct** (50): Product taxonomy (Name, Category, SubCategory)
- **DimSalesperson** (25): Sales rep attributes (Name, Team/Region)
- **DimRegion** (5): Geographic regions

This star schema allows me to:
- Analyze sales by any dimension independently
- Use consistent definitions across all visuals
- Maintain referential integrity (every sales transaction links to valid dimensions)
- Scale efficiently even with millions of transactions"

### Key Points to Emphasize
- ✓ Why star schema? "Simplifies calculations, optimizes aggregations"
- ✓ Why no bridge tables? "Not needed - each dimension is atomic"
- ✓ Why separate DimRegion vs Region in DimSalesperson? "Allows analysis independent of sales team structure"
- ✓ Why 2,500 transactions? "Real-world sized - large enough to be interesting, small enough for demos"

---

## Question 2: "How did you clean the data?"

### Answer (1-2 minutes)
"In Power Query, I applied these transformations to each table:

**Data Quality Checks:**
1. **Type Conversion**: Cast all columns to correct types (dates, integers, decimals)
2. **Duplicate Detection**: Remove duplicate OrderIDs in FactSales
3. **Null Validation**: Remove rows with missing keys (CustomerID, ProductID, etc.)
4. **Data Range Validation**: 
   - Quantity > 0 (no zero or negative orders)
   - UnitPrice > 0 (no free products)
   - Sales > 0 (valid transactions)
5. **Text Standardization**: Trim whitespace, apply proper case to names

**Example - FactSales cleaning:**
```
Source → Promote Headers → Change Types → Remove Duplicates 
→ Filter Invalid Records → Add Calculated Columns → Sort by Date
```

**Why this matters:**
- Garbage in = garbage out
- Invalid data ruins dashboards (negative sales, orphaned orders)
- Proper cleaning saves months of troubleshooting later"

### Common Follow-Up
**Q: "How would you handle records with missing values?"**
**A:** "Depends on the field:
- Missing key (CustomerID) → Delete row (can't link to fact)
- Missing text field (CityName) → Use 'Unknown' placeholder
- Missing numeric field (Discount) → Use 0 (no discount given)
- But first, I'd investigate root cause: Is it a data extraction issue or legitimate missing value?"

---

## Question 3: "Walk me through your Power Query steps for FactSales"

### Answer (Include M Code)
"Here's the process:

```powerquery
Step 1: Load CSV
Source = Csv.Document(File.Contents("FactSales.csv"))

Step 2: Promote headers & convert types
ChangeTypes = Table.TransformColumnTypes(Source, {
  {"OrderID", Int64},
  {"OrderDate", Date},
  {"CustomerID", Int64},
  {"Quantity", Int64},
  {"UnitPrice", Number},
  {"Sales", Number},
  {"Profit", Number}
})

Step 3: Remove duplicates and invalid records
RemovedDuplicates = Table.Distinct(ChangeTypes, {"OrderID"})
FilteredRecords = Table.SelectRows(RemovedDuplicates, each 
  [OrderDate] <> null 
  && [Quantity] > 0 
  && [Sales] > 0
)

Step 4: Add temporal attributes
AddYear = Table.AddColumn(FilteredRecords, "Year", each Date.Year([OrderDate]))
AddMonth = Table.AddColumn(AddYear, "Month", each Date.Month([OrderDate]))
```

**Why denormalize temporal fields into FactSales?**
- Performance: Faster than DATEVALUE lookups in DAX
- Simplicity: Easy to filter by Year/Month in pivot tables
- Consistency: All transactions get same attributes as DimDate"

---

# PART 2: Data Modeling in Power BI

## Question 4: "How did you set up relationships?"

### Answer (1-2 minutes)
"In the Power BI data model:

**Relationships (All one-to-many):**

| Fact Table | Dimension | Relationship | Type |
|-----------|-----------|--------------|------|
| FactSales | DimDate | OrderDate → Date | Active |
| FactSales | DimCustomer | CustomerID → CustomerID | Active |
| FactSales | DimProduct | ProductID → ProductID | Active |
| FactSales | DimSalesperson | SalespersonID → SalespersonID | Active |
| FactSales | DimRegion | RegionID → RegionID | Active |

**Why all active?** 
Each foreign key uniquely identifies a dimension, so cross-filter direction is single.

**Referential Integrity:**
- Every OrderDate in FactSales has a matching row in DimDate
- Every CustomerID in FactSales links to exactly one customer
- No orphaned transactions (sales without a valid customer, product, region)

**Performance Implications:**
- One-to-many relationships are optimized in Vertipaq
- Active relationships enable natural cross-filtering
- I avoid circular relationships (none exist in this schema)"

### Follow-Up: "What if you had multiple date columns?"

"Great question. If I had both OrderDate and ShipDate, I'd:

1. Make OrderDate → DimDate the **active** relationship (used by default)
2. Make ShipDate → DimDate a **inactive** relationship (use in specific measures)
3. In DAX, use USERELATIONSHIP() to activate the inactive relationship:

```dax
Sales by ShipDate = 
CALCULATE(
    [Total Sales],
    USERELATIONSHIP(FactSales[ShipDate], DimDate[Date])
)
```

This allows analysis by order date OR ship date, not both simultaneously."

---

# PART 3: DAX Measures

## Question 5: "Walk me through your key DAX measures"

### Answer Framework
"I organized measures into 3 groups:

### GROUP 1: Core Metrics (Foundation)"

**Total Sales**
```dax
Total Sales = SUM(FactSales[Sales])
```
"Sums pre-calculated Sales column. Simple and efficient."

**Gross Profit**
```dax
Gross Profit = [Total Sales] - [Total Cost]
```
"Composes two measures - shows profit decomposition."

**Total Cost**
```dax
Total Cost = SUMX(FactSales, FactSales[Cost] * FactSales[Quantity])
```
"Cost is per-unit, so multiply by Quantity. SUMX iterates for correctness."

**Gross Margin %**
```dax
Gross Margin % = IFERROR(DIVIDE([Gross Profit], [Total Sales], 0), 0)
```
"DIVIDE with default prevents #DIV/0! errors. Useful for profitability."

---

### GROUP 2: Time Intelligence"

**Sales YTD** (Year-To-Date)
```dax
Sales YTD = TOTALYTD([Total Sales], DimDate[Date])
```
"Cumulative from Jan 1 to today. Essential for budget tracking."

**Sales PY** (Prior Year)
```dax
Sales PY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))
```
"Same dates but prior year - enables YoY comparison."

**YoY Sales Growth %**
```dax
YoY Sales % = IFERROR(DIVIDE([Total Sales] - [Sales PY], [Sales PY], 0), 0)
```
"Percentage change. Shows +14% growth is a key metric."

**Sales L12M** (Last 12 Months)
```dax
Sales L12M = CALCULATE(
    [Total Sales],
    FILTER(DimDate, DimDate[Date] >= MAX(DimDate[Date]) - 365)
)
```
"Rolling 12-month smooths seasonality."

---

### GROUP 3: Target & KPIs"

**Target Achievement %**
```dax
Target Achievement % = IFERROR(
    DIVIDE([Total Sales], [Target Sales], 0),
    0
)
```
"If > 100%, exceeding target. Used for bonus calculations."

**Variance to Target**
```dax
Variance to Target = [Total Sales] - [Target Sales]
```
"Dollar gap from target. Actionable metric."

---

## Question 6: "Why did you use measures instead of calculated columns?"

### Answer (Very Important for Interview)
"This shows deep understanding of Power BI performance.

**Calculated Columns:**
```dax
// DON'T DO THIS
FactSales[YearColumn] = YEAR(FactSales[OrderDate])
```
Pros: Appears in field list, can use in visuals
Cons: 
- Takes up memory (stored for every row)
- Can't be filtered dynamically
- Not appropriate for aggregations

**Measures (DO THIS):**
```dax
// DO THIS
[Sales YTD] = TOTALYTD([Total Sales], DimDate[Date])
```
Pros:
- Calculated on-demand, not stored
- Responsive to filter context
- Essential for time intelligence
- Optimized by Vertipaq engine

**My approach:**
- Calculated columns ONLY for non-aggregated attributes (Customer name, Region, etc.)
- Measures for ALL aggregations and calculations
- This keeps my FactSales table lean (~50 columns instead of 100+)
- Queries stay fast even with millions of rows"

---

# PART 4: Dashboard Design

## Question 7: "Walk me through Page 1: Executive Overview"

### Answer (2-3 minutes, structured)
"This is designed for C-suite: 2-minute consumption, tells complete story.

**Top Row - 6 KPI Cards:**
1. Total Sales ($45.2M) - Revenue
2. Gross Profit ($18.3M) - Bottom line
3. Gross Margin % (42%) - Efficiency
4. YoY Growth % (+14%) - Growth trajectory
5. Target Achievement % (112%) - Execution
6. Total Customers (8,432) - Lead indicator

**Why these 6?**
- **Sales & Profit**: Traditional P&L
- **Margin %**: Shows if growth is profitable
- **YoY Growth**: Investors care about growth rate, not absolute dollars
- **Target Achievement**: Shows execution vs. plan
- **Customers**: Customer acquisition = future revenue

**Middle Section - Regional Distribution & Category Mix**
- Donut chart: Sales by Region (shows North dominates at 35%)
- Bar chart: Sales by Category (Electronics, Software, etc.)
- Tells story: Where is revenue coming from?

**Bottom Section - Trend Analysis**
- Area chart: Monthly profit trend (is profit accelerating?)
- Line chart: Top 10 customers (concentration risk - top 3 = 35% of sales)

**Executive Insights Text Box**
Auto-generated observations:
- Sales +14% YoY ✓
- Margin compression -1.2pp ⚠
- Target on track to exceed by $1.2M ✓
- West region 87% of target needs attention ⚠

**Key Insight:** Everything is comparative (vs. prior year, vs. target) because absolute numbers mean nothing without context."

---

## Question 8: "How did you approach the design?"

### Answer
"Design is driven by business questions:

1. **Executive Overview (Page 1)**: 'Is the business healthy?'
   - KPIs answer: Yes, 14% growth, 112% of target
   
2. **Sales Analysis (Page 2)**: 'Which regions/reps/products are driving growth?'
   - Multiple charts by dimension
   - Drill-through for investigation
   
3. **Customer Analysis (Page 3)**: 'Are we acquiring/retaining customers?'
   - Customer growth, segmentation, Pareto analysis
   
4. **Profitability (Page 4)**: 'Which businesses are profitable?'
   - Margin analysis by region/product/segment
   
5. **Forecast (Page 5)**: 'Will we hit our annual target?'
   - Actual vs. forecast vs. target

6. **Drill-Through (Page 6)**: 'Show me the transactions'
   - Transaction detail accessible from any other page

**Design Philosophy:**
- Minimal clutter: 4-5 visuals per page max
- Clear hierarchy: KPIs at top, detail below
- Navigation: Consistent drill-through from every page
- Responsiveness: Works on desktop, tablet, mobile"

---

# PART 5: Interview Scenarios

## Scenario 1: "Sales decreased 5% this month. What happened?"

### Your Approach (2 minutes)
"I'd investigate systematically:

**Step 1: Check the facts (Page 1)**
- Confirm 5% decrease is real (vs. prior month, not vs. prior year)
- Check if it's company-wide or specific region

**Step 2: Break down by dimension (Page 2)**
- Is it all regions declining, or one region?
- Are all products down, or just one category?
- Are all salespeople affected, or specific reps?

**Step 3: Customer analysis (Page 3)**
- Did we lose major customers?
- Is customer count declining?

**Step 4: Drill into detail (Page 6)**
- Click the declined region
- See transactions: Which products? Which customers?
- Identify the root cause transaction

**Example Root Causes I might find:**
- Large customer didn't place order this month (cyclical)
- Product shortage reduced sales (supply)
- Price increase caused volume drop (pricing)
- Sales rep left (personnel)
- Seasonal pattern (common for retail)

**Recommendation:**
Once root cause is identified, propose solution:
- If customer cyclical: Expected to return, no action needed
- If supply issue: Escalate to operations
- If pricing issue: Consider discount strategy
- If rep left: Coverage plan needed"

---

## Scenario 2: "Gross margin is declining despite growing sales"

### Your Approach (2 minutes)
"Classic problem - revenue growth doesn't equal profit growth.

**Diagnosis (Page 4 - Profitability):**

1. **Check product mix:**
   - Product margin by category chart
   - Are we selling more low-margin products?
   - Example: Electronics (20% margin) growing faster than Software (50% margin)?

2. **Check regional mix:**
   - Margin by region
   - Is a low-margin region growing faster?

3. **Check customer segment:**
   - Are we selling more to SMB (lower margins) vs Enterprise (higher)?
   - Price pressure from larger customers?

4. **Check input costs:**
   - Cost per unit increasing?
   - Supply chain inflation?

5. **Check discounting:**
   - Discount % increasing to drive volume?

**Root Cause Tree:**

```
Margin ↓
├─ Product Mix Shift ← Most common in diversified companies
│  └─ Solution: Re-prioritize high-margin products in sales incentives
├─ Customer Mix Shift
│  └─ Solution: Adjust pricing by segment
├─ Cost Inflation
│  └─ Solution: Negotiate supplier contracts
└─ Aggressive Discounting
   └─ Solution: Implement discount governance policy
```

**Recommendation:**
Most likely: Sales team is discounting to hit volume targets. Need to rebalance incentives to reward profitability, not just sales volume."

---

## Scenario 3: "We're 87% of target. Will we hit the goal?"

### Your Approach (Page 5 - Forecast & Targets)
"Depends on the runway.

**Metrics to Check:**

1. **Days to Target Achievement**
   - If 30 days left and need 20% more sales
   - Daily run rate needed: $X/day
   - Current daily run rate: $Y/day
   - If Y < X: Unlikely to achieve without extraordinary effort

2. **Sales Forecast (based on YTD)**
   - Year-to-date sales: $X
   - Months elapsed: N
   - Annualized run rate: (X/N) * 12
   - If run rate < target: Won't achieve

3. **Trend Analysis**
   - Are we accelerating or decelerating?
   - If accelerating: Maybe catch up
   - If decelerating: Unlikely

**Example Math:**
- Target: $12M annual
- Today: Sept 15 (9.4 months in)
- Sales YTD: $10.4M
- Percentage: 87%
- Remaining: $1.6M needed
- Days left: 107 (Sept 15 to Dec 31)
- Daily need: $1.6M / 107 = $15K/day
- Current daily rate: $10.4M / 284 days = $36.6K/day ✓

**Recommendation:**
At current pace, will exceed target by ~$3M. BUT:
- Q4 often has seasonality (holiday spending or lower activity)
- Watch October/November closely
- Plan for Q1 carry-over if market slows"

---

## Scenario 4: "Why should we invest in Power BI vs. Excel?"

### Your Answer
"This dashboard illustrates the key benefits:

**Excel Limitations:**
- Manual updates (2+ hours/week)
- No drill-through (users stuck at summary)
- Static relationships (what-if analysis requires new models)
- No real-time (stale data for decisions)
- Poor collaboration (emailed files, version confusion)

**Power BI Advantages:**
- Automated refresh (updates nightly, users always have current data)
- Drill-through (explore root causes in seconds)
- Interactive filtering (what-if scenarios instantly)
- Real-time sharing (team sees same data simultaneously)
- Governance (one source of truth, no conflicting versions)
- Scalability (hundreds of visuals, millions of rows, still fast)

**ROI Example:**
- Current: 25 analysts x 2 hrs/week = 50 hrs/week on reporting
- With Power BI: 5 hrs/week maintenance = 45 hrs freed
- 45 hrs/week x $50/hr = $2,250/week = $117K/year cost savings
- Power BI cost: ~$500/user/year = $12.5K/year
- Net savings: $104.5K/year (8.4x ROI)

**Intangible Benefits:**
- Faster decisions (instant dashboards vs. 3-day wait)
- Better decisions (drill-through reveals patterns Excel hides)
- Strategic vs. tactical (stop firefighting reports, start analyzing trends)"

---

# PART 6: Performance Optimization

## Question: "How did you optimize this dashboard for performance?"

### Answer (2-3 minutes)
"Performance is critical for adoption. I applied these principles:

1. **Data Modeling:**
   - Removed calculated columns (not stored, calculated on-demand)
   - De-duplicated dimension tables (no redundancy)
   - Used INT for foreign keys (more efficient than string matching)
   - Ensured relationships don't create cycles (Vertipaq filter bloat)

2. **Power Query:**
   - Filter at source when possible (don't import 5M rows to filter to 2M)
   - Remove unnecessary columns (only import what visuals need)
   - Use native SQL queries for large imports (vs. CSV)

3. **DAX Measures:**
   - Avoid SUMPRODUCT (slow, use SUMX)
   - Avoid complex CALCULATE filters (chain filters instead)
   - Use DIVIDE with default (prevents #DIV/0! errors)
   - Pre-calculate simple values in Power Query if needed

4. **Visuals:**
   - Limit visuals per page (4-5 max, not 15)
   - Use appropriate chart types (scatter for 1M+ points, other charts for <10K)
   - Minimize custom visuals (slower than native)
   - Set 'Display units' to millions (reduces numbers, faster renders)

5. **Caching:**
   - Mark DimDate as date table (enables Vertipaq optimizations)
   - Arrange relationships so most active filtering is on highest cardinality
   - Schedule refreshes during off-hours, not business hours

**Result:**
- Data model: 15MB (vs. 250MB in Excel files)
- Page load time: <2 seconds
- Query response: <1 second on any filter
- Can handle 10x current data size without performance hit"

---

# PART 7: Closing Statement

## Question: "Why should we hire you based on this project?"

### Answer (1 minute, confident)
"This dashboard demonstrates that I can:

1. **Understand Business Requirements**
   - Started with business questions, not technical constraints
   - Dashboard tells a story (revenue, profit, growth, targets)
   - Each page answers a specific business question

2. **Engineer Data Solutions**
   - Designed normalized star schema
   - Built 20+ DAX measures from scratch
   - Implemented time intelligence correctly

3. **Create Compelling Visualizations**
   - Professional, minimal design
   - Actionable insights (not just charts)
   - Multi-level drill-through for investigation

4. **Think Like a Data Analyst**
   - Scenario planning (if sales drop, how to investigate)
   - Root cause analysis
   - Translating business metrics to technical implementation

5. **Communicate Effectively**
   - Can explain technical decisions (why star schema, why measures not columns)
   - Can translate to business stakeholders (what do margins mean)
   - Documentation for interview prep (this guide)

I'm not just a tool operator - I'm a strategic thinker who uses data tools to drive business decisions."

---

# Quick Reference: Common Interview Questions

| Question | Answer Location | Key Points |
|----------|-----------------|------------|
| "Tell me about your data model" | PART 1, Q1 | Star schema, 1:M relationships, 5 tables |
| "How did you clean the data?" | PART 1, Q2 | Type conversion, duplicates, nulls, validation |
| "Show me your DAX" | PART 3, Q5-Q6 | Measures not columns, time intelligence, best practices |
| "Walk me through the dashboard" | PART 4, Q7 | Business questions drive design |
| "How do you troubleshoot issues?" | PART 5, Scenario 1 | Systematic approach: facts → dimensions → detail |
| "Why Power BI over Excel?" | PART 5, Scenario 4 | Scale, automation, collaboration, ROI |
| "How do you optimize?" | PART 6 | Modeling, measures, visuals, caching |

