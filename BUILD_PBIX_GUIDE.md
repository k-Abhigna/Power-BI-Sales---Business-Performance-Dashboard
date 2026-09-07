# 🔨 Step-by-Step Guide: Build Your .PBIX File

## Overview
This guide walks you through building the complete Power BI Dashboard (.pbix file) in **Power BI Desktop** in approximately **2-3 hours**.

All data, DAX code, and specifications are ready to copy/paste.

---

## ⏱️ Time Breakdown

| Step | Task | Time |
|------|------|------|
| 1 | Open Power BI & import data | 15 min |
| 2 | Apply Power Query transformations | 20 min |
| 3 | Create relationships | 10 min |
| 4 | Create DAX measures | 45 min |
| 5 | Build Page 1 (Executive) | 30 min |
| 6 | Build Pages 2-5 (Analysis) | 60 min |
| 7 | Build Page 6 (Drill-through) | 15 min |
| 8 | Format & finalize | 15 min |
| **TOTAL** | | **~3 hours** |

---

## 📋 Prerequisites

✅ Power BI Desktop (free version at https://powerbi.microsoft.com/desktop)
✅ CSV files from `data/raw/` folder
✅ This guide open in another window
✅ DAX measures from `dax-measures/` folder
✅ Dashboard specifications from `dashboard-design/` folder

---

# STEP 1: Open Power BI & Import Data (15 minutes)

## 1.1 Launch Power BI Desktop

1. Open **Power BI Desktop**
2. Click **"Get Data"** button
3. Select **"Text/CSV"**

## 1.2 Load First Table: FactSales

1. Browse to: `data/raw/FactSales.csv`
2. Click **Load**
3. Wait for data preview
4. Click **Load** again to import

**Expected:** 2,500 rows loaded

## 1.3 Load Remaining Tables

Repeat for each file (in this order):

**3️⃣ DimDate.csv**
- Get Data → Text/CSV
- Select `data/raw/DimDate.csv`
- Load

**4️⃣ DimCustomer.csv**
- Get Data → Text/CSV
- Select `data/raw/DimCustomer.csv`
- Load

**5️⃣ DimProduct.csv**
- Get Data → Text/CSV
- Select `data/raw/DimProduct.csv`
- Load

**6️⃣ DimSalesperson.csv**
- Get Data → Text/CSV
- Select `data/raw/DimSalesperson.csv`
- Load

**7️⃣ DimRegion.csv**
- Get Data → Text/CSV
- Select `data/raw/DimRegion.csv`
- Load

**8️⃣ DimTarget.csv**
- Get Data → Text/CSV
- Select `data/raw/DimTarget.csv`
- Load

**Result:** 7 tables loaded in Power BI Desktop

---

# STEP 2: Power Query Transformations (20 minutes)

## 2.1 Access Power Query Editor

1. Home tab → **Transform Data** (or Get Data → Edit Queries)
2. Power Query Editor opens

## 2.2 Transform FactSales

**Reference:** `power-query/01_FactSales_Query.md`

1. Select **FactSales** query
2. Right-click column headers → **Choose Columns**
3. Keep: OrderID, OrderDate, CustomerID, ProductID, SalespersonID, RegionID, Quantity, UnitPrice, Discount, Cost, Sales, Profit

4. Click **"Remove Duplicates"** (Home tab)
   - Select: OrderID
   - This removes duplicate orders

5. **Add Custom Column** (Add Column tab):
   ```
   Name: Year
   Formula: = Date.Year([OrderDate])
   ```

6. **Add Custom Column**:
   ```
   Name: Month
   Formula: = Date.Month([OrderDate])
   ```

7. **Add Custom Column**:
   ```
   Name: Quarter
   Formula: = Date.Quarter([OrderDate])
   ```

8. **Add Custom Column**:
   ```
   Name: YearMonth
   Formula: = Text.From(Date.Year([OrderDate])) & "-" & Text.PadStart(Text.From(Date.Month([OrderDate])), 2, "0")
   ```

9. Click **Close & Apply** (Home tab)

## 2.3 Transform DimDate

**Reference:** `power-query/02_DimDate_Query.md`

1. Select **DimDate** query
2. Keep columns: Date, Day, Month, MonthName, Quarter, Year, YearMonth
3. **Add Custom Column**:
   ```
   Name: DayOfWeek
   Formula: = Date.DayOfWeekName([Date])
   ```

4. **Add Custom Column**:
   ```
   Name: IsCurrentYear
   Formula: = [Year] = Date.Year(DateTime.LocalNow())
   ```

5. Click **Close & Apply**

## 2.4 Transform Dimensions (DimCustomer, DimProduct, etc.)

**Reference:** `power-query/03_Dimensions_Queries.md`

For each dimension table:

1. Select the query
2. **Trim** all text columns:
   - Select column → Transform → Format → Trim
3. **Remove Duplicates** on the ID column
4. Click **Close & Apply**

**Result:** All 7 tables transformed and cleaned

---

# STEP 3: Create Relationships (10 minutes)

## 3.1 Open Model View

1. Click **Model** tab (left sidebar)
2. You see all 7 tables displayed

## 3.2 Create Relationships

Create these 5 relationships by dragging:

**Relationship 1: FactSales → DimDate**
- Drag: `FactSales[OrderDate]` → `DimDate[Date]`
- Cardinality: Many-to-One
- Direction: Single
- ✅ Active

**Relationship 2: FactSales → DimCustomer**
- Drag: `FactSales[CustomerID]` → `DimCustomer[CustomerID]`
- Cardinality: Many-to-One
- Direction: Single
- ✅ Active

**Relationship 3: FactSales → DimProduct**
- Drag: `FactSales[ProductID]` → `DimProduct[ProductID]`
- Cardinality: Many-to-One
- Direction: Single
- ✅ Active

**Relationship 4: FactSales → DimSalesperson**
- Drag: `FactSales[SalespersonID]` → `DimSalesperson[SalespersonID]`
- Cardinality: Many-to-One
- Direction: Single
- ✅ Active

**Relationship 5: FactSales → DimRegion**
- Drag: `FactSales[RegionID]` → `DimRegion[RegionID]`
- Cardinality: Many-to-One
- Direction: Single
- ✅ Active

## 3.3 Mark Date Table

1. Right-click **DimDate** table
2. Select **Mark as date table**
3. Confirm date column: `DimDate[Date]`
4. Click **OK**

**Result:** Star schema complete with all relationships configured

---

# STEP 4: Create DAX Measures (45 minutes)

## 4.1 Create Measures Table

1. Click **Data** tab (left sidebar)
2. Right-click in empty space → **New Table**
3. Enter:
   ```dax
   Measures = BLANK()
   ```
4. Click **✓** to confirm

**New table "Measures" appears**

## 4.2 Create Display Folders

1. Right-click "Measures" table → **Edit**
2. Add custom column:
   ```dax
   _ = BLANK()
   ```
3. In **Modeling** tab → **Display Folder** → Create folders:
   - Core Metrics
   - Time Intelligence
   - Target & KPIs

**Reference:** `dax-measures/001_Core_Measures.md`

## 4.3 Add Core Measures

Click **Modeling** tab → **New Measure**

### Measure 1: Total Sales
```dax
Total Sales = SUM(FactSales[Sales])
```
- Display Folder: Core Metrics
- Format: $#,##0.00

### Measure 2: Total Cost
```dax
Total Cost = SUMX(FactSales, FactSales[Cost] * FactSales[Quantity])
```
- Display Folder: Core Metrics
- Format: $#,##0.00

### Measure 3: Gross Profit
```dax
Gross Profit = [Total Sales] - [Total Cost]
```
- Display Folder: Core Metrics
- Format: $#,##0.00

### Measure 4: Gross Margin %
```dax
Gross Margin % = IFERROR(DIVIDE([Gross Profit], [Total Sales], 0), 0)
```
- Display Folder: Core Metrics
- Format: 0.0%

### Measure 5: Total Orders
```dax
Total Orders = COUNTA(FactSales[OrderID])
```
- Display Folder: Core Metrics
- Format: 0

### Measure 6: Total Quantity
```dax
Total Quantity = SUM(FactSales[Quantity])
```
- Display Folder: Core Metrics
- Format: 0

### Measure 7: Total Customers
```dax
Total Customers = DISTINCTCOUNT(FactSales[CustomerID])
```
- Display Folder: Core Metrics
- Format: 0

### Measure 8: Average Order Value
```dax
Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)
```
- Display Folder: Core Metrics
- Format: $#,##0.00

## 4.4 Add Time Intelligence Measures

**Reference:** `dax-measures/002_Time_Intelligence_Measures.md`

### Measure 9: Sales YTD
```dax
Sales YTD = TOTALYTD([Total Sales], DimDate[Date])
```
- Display Folder: Time Intelligence
- Format: $#,##0.00

### Measure 10: Sales MTD
```dax
Sales MTD = CALCULATE(
    [Total Sales],
    DATESBETWEEN(
        DimDate[Date],
        DATE(YEAR(MAX(DimDate[Date])), MONTH(MAX(DimDate[Date])), 1),
        MAX(DimDate[Date])
    )
)
```
- Display Folder: Time Intelligence
- Format: $#,##0.00

### Measure 11: Sales QTD
```dax
Sales QTD = TOTALQTD([Total Sales], DimDate[Date])
```
- Display Folder: Time Intelligence
- Format: $#,##0.00

### Measure 12: Sales PY (Prior Year)
```dax
Sales PY = CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)
```
- Display Folder: Time Intelligence
- Format: $#,##0.00

### Measure 13: YoY Sales %
```dax
YoY Sales % = IFERROR(
    DIVIDE([Total Sales] - [Sales PY], [Sales PY], 0),
    0
)
```
- Display Folder: Time Intelligence
- Format: 0.0%

### Measure 14: Sales L12M (Last 12 Months)
```dax
Sales L12M = CALCULATE(
    [Total Sales],
    FILTER(
        DimDate,
        DimDate[Date] >= MAX(DimDate[Date]) - 365
        && DimDate[Date] <= MAX(DimDate[Date])
    )
)
```
- Display Folder: Time Intelligence
- Format: $#,##0.00

### Measure 15: Sales L3M (Last 3 Months)
```dax
Sales L3M = CALCULATE(
    [Total Sales],
    FILTER(
        DimDate,
        DimDate[Date] >= MAX(DimDate[Date]) - 90
        && DimDate[Date] <= MAX(DimDate[Date])
    )
)
```
- Display Folder: Time Intelligence
- Format: $#,##0.00

### Measure 16: Profit Growth %
```dax
Profit Growth % = IFERROR(
    DIVIDE(
        [Gross Profit] - CALCULATE([Gross Profit], SAMEPERIODLASTYEAR(DimDate[Date])),
        CALCULATE([Gross Profit], SAMEPERIODLASTYEAR(DimDate[Date])),
        0
    ),
    0
)
```
- Display Folder: Time Intelligence
- Format: 0.0%

## 4.5 Add Target & KPI Measures

**Reference:** `dax-measures/003_Target_KPI_Measures.md`

### Measure 17: Target Sales
```dax
Target Sales = SUMX(
    VALUES(DimDate[Year], DimDate[Month]),
    CALCULATE(
        SUM(DimTarget[TargetSales]),
        MATCHALL(
            DimDate[Year], DimTarget[Year],
            DimDate[Month], DimTarget[Month]
        )
    )
)
```
- Display Folder: Target & KPIs
- Format: $#,##0.00

### Measure 18: Target Achievement %
```dax
Target Achievement % = IFERROR(
    DIVIDE([Total Sales], [Target Sales], 0),
    0
)
```
- Display Folder: Target & KPIs
- Format: 0.0%

### Measure 19: Variance to Target
```dax
Variance to Target = [Total Sales] - [Target Sales]
```
- Display Folder: Target & KPIs
- Format: $#,##0.00

### Measure 20: Annual Forecast
```dax
Annual Forecast = IF(
    MONTH(MAX(DimDate[Date])) > 0,
    ([Sales YTD] / MONTH(MAX(DimDate[Date]))) * 12,
    0
)
```
- Display Folder: Target & KPIs
- Format: $#,##0.00

**Result:** 20+ measures created and organized

---

# STEP 5: Build Page 1 - Executive Overview (30 minutes)

## 5.1 Create New Page

1. Right-click page tab at bottom → **New page**
2. Rename: **Executive Overview**

## 5.2 Add Title

1. **Insert** tab → **Text Box**
2. Type: "Executive Overview"
3. Format: 24pt, Bold, Dark Gray

## 5.3 Add Slicers

**Date Slicer:**
1. **Insert** → **Slicer**
2. Select: **DimDate[Date]**
3. In slicer settings: Change to **Between** range
4. Position: Top-left corner
5. Resize: ~200px wide

**Region Slicer:**
1. **Insert** → **Slicer**
2. Select: **DimRegion[Region]**
3. Position: Next to Date slicer
4. Set to **Buttons** style

## 5.4 Add KPI Cards (Row 1: 6 cards in 3 columns)

**KPI 1: Total Sales**
1. **Insert** → **KPI** visual
2. Value: **[Total Sales]**
3. Trend axis: **DimDate[Date]**
4. Format: $M, 1 decimal

**KPI 2: Gross Profit**
1. Duplicate KPI 1
2. Value: **[Gross Profit]**

**KPI 3: Gross Margin %**
1. Duplicate KPI 1
2. Value: **[Gross Margin %]**
3. Format: 0.0%

**KPI 4: YoY Growth %**
1. Duplicate KPI 1
2. Value: **[YoY Sales %]**
3. Format: 0.0%

**KPI 5: Target Achievement %**
1. Duplicate KPI 1
2. Value: **[Target Achievement %]**
3. Format: 0.0%

**KPI 6: Total Customers**
1. Duplicate KPI 1
2. Value: **[Total Customers]**
3. Format: 0

## 5.5 Add Charts (Row 2: 2 charts side-by-side)

**Chart 1: Monthly Sales Trend**
1. **Insert** → **Line Chart**
2. Axis: **DimDate[Date]** (Month level)
3. Legend: **[Total Sales]**
4. Values: **[Total Sales]**
5. Position: Left half, 50% width

**Chart 2: Sales by Region**
1. **Insert** → **Donut Chart**
2. Legend: **DimRegion[Region]**
3. Values: **[Total Sales]**
4. Position: Right half, 50% width

## 5.6 Add More Charts (Row 3: 2 charts)

**Chart 3: Sales by Category**
1. **Insert** → **Horizontal Bar Chart**
2. Axis: **DimProduct[Category]**
3. Values: **[Total Sales]**
4. Position: Left, 50% width

**Chart 4: Monthly Profit Trend**
1. **Insert** → **Column Chart**
2. Axis: **DimDate[Date]** (Month level)
3. Values: **[Gross Profit]**
4. Position: Right, 50% width

## 5.7 Add Top Customers Table

1. **Insert** → **Table**
2. Columns:
   - DimCustomer[CustomerName]
   - DimCustomer[Segment]
   - [Total Sales]
   - [Total Orders]
3. Position: Full width below charts
4. Sort by: [Total Sales] descending

**Result:** Page 1 complete with 6 KPIs, 4 charts, 1 table, 2 slicers

---

# STEP 6: Build Pages 2-5 (60 minutes)

## 6.1 Page 2: Sales Analysis

**Reference:** `dashboard-design/PAGE_2_SALES_ANALYSIS.md`

1. Create new page: "Sales Analysis"
2. Add slicers: Month, Region, Category, Salesperson, Segment
3. Add charts:
   - Sales by Month (Line)
   - Sales by Region (Column)
   - Top Salespeople (Horizontal Bar)
   - Product Category Performance (Stacked Column)
4. Add table: Sales Performance by Salesperson
5. Add stats cards: Total Sales, Total Orders, AOV, Quantity

## 6.2 Page 3: Customer Analysis

**Reference:** `dashboard-design/PAGES_3_4_5_6_SUMMARY.md`

1. Create new page: "Customer Analysis"
2. Add KPI cards: Total Customers, Avg Revenue/Customer, Repeat Rate
3. Add charts:
   - Customer Growth Trend (Line)
   - Customers by Segment (Donut)
   - Customers by City (Horizontal Bar)
   - Revenue Distribution (Bar)
4. Add table: Top 15 Customers

## 6.3 Page 4: Profitability

**Reference:** `dashboard-design/PAGES_3_4_5_6_SUMMARY.md`

1. Create new page: "Profitability"
2. Add KPI cards: Total Sales, Total Cost, Gross Profit, Gross Margin %
3. Add charts:
   - Margin by Region (Column, color-coded)
   - Margin by Product (Horizontal Bar)
   - Profit Trend (Area)
   - Margin by Segment (Donut)
4. Add table: Profitability by Product

## 6.4 Page 5: Forecast & Targets

**Reference:** `dashboard-design/PAGES_3_4_5_6_SUMMARY.md`

1. Create new page: "Forecast & Targets"
2. Add region filter
3. Add KPI cards: YTD Sales, YTD Target, Achievement %, Annual Forecast
4. Add charts:
   - Actual vs Target vs Forecast (Combo Line/Column)
   - Target Achievement by Region (Column)
   - Cumulative Sales (Area)
5. Add table: Monthly Performance vs Target

**Time:** ~15 min per page

---

# STEP 7: Build Page 6 - Drill-Through (15 minutes)

## 7.1 Create Drill-Through Page

1. Create new page: "Transaction Details"
2. Right-click page tab → **Edit**
3. Check: "Is drill-through page"
4. Click OK

## 7.2 Add Drill-Through Filters

1. **Insert** → **Slicer**
2. Add fields that can be drilled:
   - DimRegion[Region]
   - DimProduct[Category]
   - DimCustomer[CustomerName]
   - DimSalesperson[SalespersonName]

## 7.3 Add Transaction Detail Table

1. **Insert** → **Table**
2. Columns:
   - FactSales[OrderID]
   - FactSales[OrderDate]
   - DimCustomer[CustomerName]
   - DimProduct[ProductName]
   - FactSales[Quantity]
   - FactSales[UnitPrice]
   - FactSales[Discount]
   - FactSales[Sales]
   - FactSales[Cost]
   - FactSales[Profit]
   - FactSales[MarginPct] (or calculated column)
3. Scroll enabled, sort by OrderDate descending

## 7.4 Set Up Drill-Through Actions

Go back to **Page 1**:

1. Select **Region chart (Donut)**
2. **Format** → **Drill through**
3. Enable: "Allow drill-through"
4. Add field: **DimRegion[Region]**
5. Click OK

Repeat for other charts (Customers, Products, etc.)

**Result:** Page 6 complete with drill-through functionality

---

# STEP 8: Format & Finalize (15 minutes)

## 8.1 Apply Color Scheme

1. **File** → **Options and settings** → **Options**
2. **Global** → **Colors**
3. Set theme colors:
   - Primary: #0078D4
   - Secondary: #107C10
   - Accent: #FFB900

## 8.2 Set Report Background

1. Each page: Right-click → **Page settings**
2. Background: Light gray (#F3F2F1)
3. Text color: Dark gray (#333)

## 8.3 Mobile Layout

1. Each page: **View** → **Mobile layout**
2. Resize visuals for mobile view
3. Enable for all pages

## 8.4 Save as .PBIX

1. **File** → **Save As**
2. Filename: `Power BI Sales Dashboard.pbix`
3. Location: Project root folder
4. Click **Save**

**Result:** Production-ready .pbix file created!

---

# ✅ Verification Checklist

Before sharing your .pbix:

- [ ] All 7 tables loaded
- [ ] All relationships created (5 total)
- [ ] DimDate marked as date table
- [ ] 20+ measures created
- [ ] Page 1: Executive Overview complete
- [ ] Page 2: Sales Analysis complete
- [ ] Page 3: Customer Analysis complete
- [ ] Page 4: Profitability complete
- [ ] Page 5: Forecast complete
- [ ] Page 6: Drill-through page complete
- [ ] All slicers working
- [ ] All charts showing data
- [ ] Drill-through actions working
- [ ] Mobile layout responsive
- [ ] File saved as .pbix

---

# 🚀 Advanced Tips

### Performance Optimization
- Disable unnecessary columns in Power Query
- Use aggregated tables for large fact tables
- Set column summarization to "Don't summarize" where appropriate

### Dashboard Interactivity
- Use bookmarks for saved states
- Add buttons for navigation
- Enable/disable slicers for focused views

### Data Refresh
- Set up refresh schedule in Power BI Service
- Use Direct Query for real-time data (if applicable)
- Create incremental refresh partitions

---

# 📞 Troubleshooting

### "Relationship error"
- Verify data types match (both Int64)
- Check for nulls in foreign key columns
- Ensure no circular relationships

### "Measure returns error"
- Wrap aggregations in IFERROR
- Use DIVIDE with default value
- Check date context in time intelligence

### "Charts not showing"
- Verify data is present in tables
- Check slicer filters aren't hiding all data
- Ensure relationships are correct

### "Performance is slow"
- Reduce number of visuals per page
- Hide unused columns
- Use columns instead of tables in visuals

---

# 🎉 You're Done!

You now have a complete, production-ready Power BI dashboard (.pbix file) that:

✅ Demonstrates star schema design
✅ Shows 20+ DAX measures
✅ Includes 6 comprehensive pages
✅ Has interactive filtering & drill-through
✅ Uses professional design
✅ Is ready for portfolio/interview

**Total time: ~2-3 hours**

---

**Save your .pbix file and you're ready to showcase it!** 🎊

