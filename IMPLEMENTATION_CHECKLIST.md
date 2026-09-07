# Power BI Dashboard Implementation Checklist

## Phase 1: Data Preparation ✅

### 1.1 Sample Data Generation
- [x] Generate FactSales.csv (2,500 transactions)
- [x] Generate DimDate.csv (731 days, 2023-2024)
- [x] Generate DimCustomer.csv (100 customers)
- [x] Generate DimProduct.csv (50 products)
- [x] Generate DimSalesperson.csv (25 salespeople)
- [x] Generate DimRegion.csv (5 regions)
- [x] Generate DimTarget.csv (monthly targets)

**Files Location:** `/data/raw/`

### 1.2 Data Quality Validation
- [ ] Verify no null values in key columns
- [ ] Confirm all foreign keys have matching dimension records
- [ ] Validate date range: 2023-01-01 to 2024-12-31
- [ ] Check for duplicate OrderIDs in FactSales
- [ ] Confirm all Sales > 0 and Quantity > 0

---

## Phase 2: Power BI Model Setup

### 2.1 Data Import in Power BI
- [ ] Get Data → Text/CSV
- [ ] Load all 7 CSV files from `data/raw/`
- [ ] Configure column types during import
- [ ] Ensure proper headers are promoted

### 2.2 Power Query Transformations
**Reference:** `power-query/` folder

- [ ] **FactSales Query:**
  - [ ] Type conversion (dates, integers, numbers)
  - [ ] Remove duplicates on OrderID
  - [ ] Filter invalid records (Quantity ≤ 0, Sales ≤ 0)
  - [ ] Add Year, Month, Quarter, YearMonth columns
  - [ ] Calculate MarginPct = Profit / Sales
  
- [ ] **DimDate Query:**
  - [ ] Type conversion
  - [ ] Add YearQuarter, DayOfWeek, WeekOfYear
  - [ ] Add IsCurrentYear, IsCurrentMonth flags
  - [ ] Add PriorYearDate for YoY calculations
  - [ ] Sort by date ascending
  
- [ ] **DimCustomer Query:**
  - [ ] Type conversion
  - [ ] Remove duplicates on CustomerID
  - [ ] Trim whitespace
  - [ ] Create Location concatenation
  
- [ ] **DimProduct Query:**
  - [ ] Type conversion
  - [ ] Standardize category names (proper case)
  - [ ] Remove duplicates
  
- [ ] **DimSalesperson Query:**
  - [ ] Type conversion
  - [ ] Standardize team names
  - [ ] Remove duplicates
  
- [ ] **DimRegion Query:**
  - [ ] Type conversion
  - [ ] Standardize region names

### 2.3 Relationships Configuration
- [ ] FactSales[OrderDate] → DimDate[Date] (Active, Single)
- [ ] FactSales[CustomerID] → DimCustomer[CustomerID] (Active, Single)
- [ ] FactSales[ProductID] → DimProduct[ProductID] (Active, Single)
- [ ] FactSales[SalespersonID] → DimSalesperson[SalespersonID] (Active, Single)
- [ ] FactSales[RegionID] → DimRegion[RegionID] (Active, Single)
- [ ] FactSales[YearMonthTarget] → DimTarget[YearMonth] (optional for targets)

**Verification:**
- [ ] No circular relationships
- [ ] All relationships have arrows pointing from Fact → Dimension
- [ ] Foreign key data types match (all Int64)

### 2.4 Date Table Configuration
- [ ] Mark DimDate as "Date Table"
  - Data View → DimDate → Column Tools → Mark as Date Table
  - Set Date column to DimDate[Date]

---

## Phase 3: DAX Measures Creation

### 3.1 Create Measures Table
- [ ] New Table: "Measures" (or "Calculations")
- [ ] Hide all columns from Measures table
- [ ] Organize in Display Folders:
  - [ ] Core Metrics
  - [ ] Time Intelligence
  - [ ] Target & KPIs
  - [ ] Customer Metrics
  - [ ] Profitability

### 3.2 Core Metrics (Folder: "Core Metrics")
**Reference:** `dax-measures/001_Core_Measures.md`

- [ ] `Total Sales` = SUM(FactSales[Sales])
- [ ] `Total Cost` = SUMX(FactSales, FactSales[Cost] * FactSales[Quantity])
- [ ] `Gross Profit` = [Total Sales] - [Total Cost]
- [ ] `Gross Margin %` = IFERROR(DIVIDE([Gross Profit], [Total Sales], 0), 0)
- [ ] `Total Orders` = COUNTA(FactSales[OrderID])
- [ ] `Total Quantity` = SUM(FactSales[Quantity])
- [ ] `Total Customers` = DISTINCTCOUNT(FactSales[CustomerID])
- [ ] `Average Order Value` = DIVIDE([Total Sales], [Total Orders], 0)

### 3.3 Time Intelligence Measures (Folder: "Time Intelligence")
**Reference:** `dax-measures/002_Time_Intelligence_Measures.md`

- [ ] `Sales YTD` = TOTALYTD([Total Sales], DimDate[Date])
- [ ] `Sales MTD` = CALCULATE([Total Sales], DATESBETWEEN(DimDate[Date], DATE(YEAR(MAX(DimDate[Date])), MONTH(MAX(DimDate[Date])), 1), MAX(DimDate[Date])))
- [ ] `Sales QTD` = TOTALQTD([Total Sales], DimDate[Date])
- [ ] `Sales PY` = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))
- [ ] `YoY Sales %` = IFERROR(DIVIDE([Total Sales] - [Sales PY], [Sales PY], 0), 0)
- [ ] `Sales L12M` = CALCULATE([Total Sales], FILTER(DimDate, DimDate[Date] >= MAX(DimDate[Date]) - 365))
- [ ] `Sales L3M` = CALCULATE([Total Sales], FILTER(DimDate, DimDate[Date] >= MAX(DimDate[Date]) - 90))
- [ ] `Profit PY` = CALCULATE([Gross Profit], SAMEPERIODLASTYEAR(DimDate[Date]))
- [ ] `Profit Growth %` = IFERROR(DIVIDE([Gross Profit] - [Profit PY], [Profit PY], 0), 0)

### 3.4 Target & KPI Measures (Folder: "Target & KPIs")
**Reference:** `dax-measures/003_Target_KPI_Measures.md`

- [ ] `Target Sales` = CALCULATE(SUM(DimTarget[TargetSales]), MATCHALL(...))
- [ ] `Target Achievement %` = IFERROR(DIVIDE([Total Sales], [Target Sales], 0), 0)
- [ ] `Variance to Target` = [Total Sales] - [Target Sales]
- [ ] `Target Achievement Status` = IF([Target Achievement %] >= 1, "Achieved", IF([Target Achievement %] >= 0.9, "At Risk", "Below Target"))
- [ ] `Days to Target` = (Calculated days needed at current run rate)
- [ ] `Annual Forecast` = IF(MONTH(MAX(DimDate[Date])) > 0, ([Sales YTD] / MONTH(MAX(DimDate[Date]))) * 12, 0)
- [ ] `Target Variance %` = IFERROR(DIVIDE([Variance to Target], [Target Sales], 0), 0)

### 3.5 Verify All Measures
- [ ] Each measure returns a single value
- [ ] No measure references a calculated column
- [ ] All DIVIDE functions have default values
- [ ] All IFERROR functions wrap aggregations
- [ ] Consistent naming (no spaces, use [square brackets])
- [ ] All measures tested in a table visual

---

## Phase 4: Dashboard Pages

### 4.1 Page 1: Executive Overview
**Reference:** `dashboard-design/PAGE_1_EXECUTIVE_OVERVIEW.md`

#### Header Section
- [ ] Date range slicer (dropdown, default: Current Year)
- [ ] Region slicer (multi-select buttons)
- [ ] Reset All button
- [ ] 6 KPI cards (2x3 layout)

#### KPI Cards
- [ ] Total Sales (blue, with YoY comparison)
- [ ] Gross Profit (green, with YoY comparison)
- [ ] Gross Margin % (teal, with change indicator)
- [ ] YoY Growth % (green/red, with sparkline)
- [ ] Target Achievement % (status colors: red/yellow/green)
- [ ] Total Customers (purple, with new customer count)

#### Charts Section
- [ ] Monthly Sales vs Target (combo: column + line)
- [ ] Sales by Region (donut chart)
- [ ] Sales by Product Category (bar chart)
- [ ] Monthly Profit Trend (area chart)
- [ ] Top 10 Customers (bar chart or table)

#### Executive Insights
- [ ] Text box with auto-generated insights
- [ ] 4-6 bullet points (growth, margin, targets, concerns)
- [ ] Format with indicators (✓, ⚠, ↑)

### 4.2 Page 2: Sales Analysis
**Reference:** `dashboard-design/PAGE_2_SALES_ANALYSIS.md`

#### Slicers (Sticky Header)
- [ ] Date range (month/quarter/year selector)
- [ ] Region (multi-select)
- [ ] Product Category (multi-select)
- [ ] Salesperson (search dropdown)
- [ ] Customer Segment (multi-select)
- [ ] Reset button
- [ ] Quick KPI summary

#### Main Charts
- [ ] Sales by Month (line + forecast)
- [ ] Sales by Region (column + target overlay)
- [ ] Top 15 Salespeople (horizontal bar, color-coded by achievement)
- [ ] Sales by Product Category (stacked column, switchable)

#### Detail Tables
- [ ] **Tab 1:** Sales Performance Summary (Salesperson ranking)
- [ ] **Tab 2:** Product Performance (Category breakdown)
- [ ] Conditional formatting on achievement %
- [ ] Sortable columns
- [ ] Export to Excel

### 4.3 Page 3: Customer Analysis
**Reference:** `dashboard-design/PAGES_3_4_5_6_SUMMARY.md`

- [ ] Key metrics cards (Total Customers, New, Repeat, Avg Revenue)
- [ ] Customer Growth Trend (line chart)
- [ ] Top 10 Customers (bar chart)
- [ ] Customers by Segment (donut)
- [ ] Revenue Contribution - Pareto (cumulative %)
- [ ] Customer Tenure vs Revenue (scatter)
- [ ] Customer detail table (exportable)

### 4.4 Page 4: Profitability Analysis
**Reference:** `dashboard-design/PAGES_3_4_5_6_SUMMARY.md`

- [ ] Profit Waterfall (Sales → Cost → Profit)
- [ ] Margin by Region (bar chart, color-coded)
- [ ] Margin by Product Category (column + volume)
- [ ] Gross Margin Trend (area chart YoY)
- [ ] Cost vs Sales by Segment (scatter)
- [ ] Profitability Table (all dimensions)

### 4.5 Page 5: Forecast & Targets
**Reference:** `dashboard-design/PAGES_3_4_5_6_SUMMARY.md`

- [ ] Actual vs Target vs Forecast (combo chart, historical shaded differently)
- [ ] Target Achievement % by Region (column + 100% reference line)
- [ ] Annual Forecast Summary (large KPI)
- [ ] Forecast Confidence Interval (area chart)
- [ ] Days to Target Achievement (gauge chart)
- [ ] Monthly Variance Analysis (waterfall)

### 4.6 Page 6: Drill-Through Detail
**Reference:** `dashboard-design/PAGES_3_4_5_6_SUMMARY.md`

- [ ] Breadcrumb navigation (← Back button)
- [ ] Drill filter summary (what was selected)
- [ ] Quick metrics (total sales, orders, profit for filtered set)
- [ ] Transaction table (all columns, 1,000 row limit)
- [ ] Conditional formatting on Margin %
- [ ] Export button
- [ ] Optional: recent 30-day sparkline

---

## Phase 5: Interactivity & Navigation

### 5.1 Slicers Configuration
- [ ] All slicers respect filter context
- [ ] Date slicer filters all pages
- [ ] Region slicer cross-filters charts
- [ ] Product slicer filters visuals
- [ ] Segment slicer filters by customer type
- [ ] Reset button clears all slicers

### 5.2 Drill-Through Actions
- [ ] Region (Page 1, 2) → Page 6 (detail filtered by region)
- [ ] Product (Page 2, 4) → Page 6 (detail filtered by product)
- [ ] Customer (Page 3) → Page 6 (detail filtered by customer)
- [ ] Salesperson (Page 2) → Page 6 (detail filtered by salesperson)
- [ ] Cross-filters preserved when drilling

### 5.3 Bookmarks (Optional)
- [ ] "Executive View" → Page 1 defaults
- [ ] "Sales By Region" → Page 2 with region pre-selected
- [ ] "Sales By Salesperson" → Page 2 with rep view
- [ ] "Profitability Deep-Dive" → Page 4
- [ ] "Forecast Review" → Page 5

### 5.4 Navigation Buttons
- [ ] Home button (returns to Page 1)
- [ ] Previous/Next page buttons
- [ ] Consistent placement on all pages
- [ ] Consistent styling

---

## Phase 6: Design & Formatting

### 6.1 Color Scheme
- [ ] Sales/Primary: #0078D4 (blue)
- [ ] Profit/Positive: #107C10 (green)
- [ ] Target/Goal: #FFB900 (orange)
- [ ] Efficiency: #00B4EF (teal)
- [ ] Alert/Neutral: #FFC914 (yellow)
- [ ] Negative: #D83B01 (red)
- [ ] Background: #F3F2F1 (light gray)

### 6.2 Conditional Formatting
- [ ] KPI cards: Change color based on value
- [ ] Achievement %: Green (>100%), Yellow (90-100%), Red (<90%)
- [ ] Margin %: Green (>40%), Yellow (30-40%), Red (<30%)
- [ ] Tables: Margin % color-coded per row

### 6.3 Typography & Spacing
- [ ] KPI values: 48pt, Bold
- [ ] KPI labels: 14pt, Regular
- [ ] Chart titles: 16pt, Semi-bold
- [ ] Legend/Axis: 11pt, Regular
- [ ] 20px padding inside containers
- [ ] 10px gap between visuals
- [ ] 15px margin from edges

### 6.4 Data Labels
- [ ] All charts have labels
- [ ] KPI cards show value + comparison
- [ ] Pie/donut: Category + % + $
- [ ] Bars: Values at end of bar
- [ ] Lines: Every 3rd point

### 6.5 Accessibility
- [ ] Minimum text contrast 4.5:1
- [ ] No information conveyed by color alone
- [ ] Alt text on all visuals
- [ ] Keyboard-navigable slicers

---

## Phase 7: Testing & Validation

### 7.1 Data Accuracy
- [ ] Total Sales = Sum of FactSales[Sales]
- [ ] Gross Profit = Sales - (Cost × Quantity)
- [ ] Margin % between 0 and 100%
- [ ] YTD values accumulate correctly
- [ ] YoY % calculated properly
- [ ] Target Achievement % within 0-200% range

### 7.2 Dashboard Functionality
- [ ] All slicers filter correctly
- [ ] All cross-filter relationships work
- [ ] Drill-through filters propagate
- [ ] No circular filter loops
- [ ] Date range changes update all pages
- [ ] Reset button clears all filters
- [ ] Mobile responsiveness works

### 7.3 Performance
- [ ] Page load time < 2 seconds
- [ ] Slicer response < 1 second
- [ ] Drill-through query < 2 seconds
- [ ] No visual rendering errors
- [ ] No measure #DIV/0! errors

### 7.4 Edge Cases
- [ ] Empty filter (no results) shows 0 or blank appropriately
- [ ] Date range with no data shows 0
- [ ] Division by zero handled gracefully
- [ ] Missing dimensions don't break relationships
- [ ] Null values in optional fields don't break measures

---

## Phase 8: Documentation & Interview Prep

### 8.1 Documentation Complete
- [ ] Power Query scripts documented (in `power-query/`)
- [ ] DAX measures documented (in `dax-measures/`)
- [ ] Dashboard page specs documented (in `dashboard-design/`)
- [ ] README created with full project overview
- [ ] Implementation checklist completed (this file)

### 8.2 Interview Preparation
- [ ] Read INTERVIEW_GUIDE.md 3 times
- [ ] Practice explaining data model (2 min)
- [ ] Practice explaining dashboard structure (6 min = 1 min per page)
- [ ] Prepare for scenario questions:
  - [ ] "Sales dropped 5% - what happened?"
  - [ ] "Margin compressed - why?"
  - [ ] "Will we hit annual target?"
  - [ ] "Which region/product/rep is best?"
- [ ] Practice showing drill-through functionality
- [ ] Prepare DAX code examples:
  - [ ] TOTALYTD
  - [ ] SAMEPERIODLASTYEAR
  - [ ] IFERROR + DIVIDE
  - [ ] Time intelligence pattern

### 8.3 Presentation Ready
- [ ] Dashboard opens cleanly
- [ ] All slicers work
- [ ] Charts render without errors
- [ ] Drill-through actions functional
- [ ] Mobile preview tested
- [ ] Export functionality works

---

## Phase 9: Final Delivery

### 9.1 Project Packaging
- [ ] All CSV files in `data/raw/`
- [ ] All Power Query scripts documented
- [ ] All DAX measures created
- [ ] All dashboard pages complete
- [ ] All documentation files present
- [ ] README has clear instructions

### 9.2 Repository
- [ ] Git repository initialized
- [ ] All files committed
- [ ] Clear commit messages
- [ ] README visible in main folder
- [ ] No sensitive data in repo

### 9.3 Handoff Checklist
- [ ] Can explain every measure
- [ ] Can explain every visual
- [ ] Can troubleshoot any issue
- [ ] Can extend dashboard for new requirements
- [ ] Confident presenting to technical and business audiences

---

## Sign-Off

**Status:** ⏳ In Progress → ✅ Complete

**Completion Date:** _________________

**Reviewed By:** _________________

**Interview Date:** _________________

**Interview Result:** _______________

---

## Notes

```
Use this section to track:
- Issues encountered and solutions
- Customizations made from template
- Performance tuning applied
- Interview feedback
- Follow-up items
```

