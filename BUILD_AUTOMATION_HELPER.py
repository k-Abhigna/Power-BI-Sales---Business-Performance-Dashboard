#!/usr/bin/env python3
"""
Power BI Dashboard Build Automation Helper
==========================================

This script generates configuration files that can be used to
accelerate the Power BI Desktop dashboard build process.

Usage:
    python3 BUILD_AUTOMATION_HELPER.py

Outputs:
    - dax_measures_reference.txt     (All DAX measures in copy-paste format)
    - power_query_reference.txt      (All M code snippets)
    - build_checklist.txt            (Complete verification checklist)
"""

import os
import json

def generate_dax_reference():
    """Generate a structured DAX measures reference file."""

    dax_measures = {
        "Core Metrics": [
            ("Total Sales", "SUM(FactSales[Sales])", "$#,##0.00"),
            ("Total Cost", "SUMX(FactSales, FactSales[Cost] * FactSales[Quantity])", "$#,##0.00"),
            ("Gross Profit", "[Total Sales] - [Total Cost]", "$#,##0.00"),
            ("Gross Margin %", "IFERROR(DIVIDE([Gross Profit], [Total Sales], 0), 0)", "0.0%"),
            ("Total Orders", "COUNTA(FactSales[OrderID])", "0"),
            ("Total Quantity", "SUM(FactSales[Quantity])", "0"),
            ("Total Customers", "DISTINCTCOUNT(FactSales[CustomerID])", "0"),
            ("Average Order Value", "DIVIDE([Total Sales], [Total Orders], 0)", "$#,##0.00"),
        ],
        "Time Intelligence": [
            ("Sales YTD", "TOTALYTD([Total Sales], DimDate[Date])", "$#,##0.00"),
            ("Sales MTD", "CALCULATE([Total Sales], DATESBETWEEN(DimDate[Date], DATE(YEAR(MAX(DimDate[Date])), MONTH(MAX(DimDate[Date])), 1), MAX(DimDate[Date])))", "$#,##0.00"),
            ("Sales QTD", "TOTALQTD([Total Sales], DimDate[Date])", "$#,##0.00"),
            ("Sales PY", "CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))", "$#,##0.00"),
            ("YoY Sales %", "IFERROR(DIVIDE([Total Sales] - [Sales PY], [Sales PY], 0), 0)", "0.0%"),
            ("Sales L12M", "CALCULATE([Total Sales], FILTER(DimDate, DimDate[Date] >= MAX(DimDate[Date]) - 365 && DimDate[Date] <= MAX(DimDate[Date])))", "$#,##0.00"),
            ("Sales L3M", "CALCULATE([Total Sales], FILTER(DimDate, DimDate[Date] >= MAX(DimDate[Date]) - 90 && DimDate[Date] <= MAX(DimDate[Date])))", "$#,##0.00"),
            ("Profit Growth %", "IFERROR(DIVIDE([Gross Profit] - CALCULATE([Gross Profit], SAMEPERIODLASTYEAR(DimDate[Date])), CALCULATE([Gross Profit], SAMEPERIODLASTYEAR(DimDate[Date])), 0), 0)", "0.0%"),
        ],
        "Target & KPIs": [
            ("Target Sales", "SUMX(VALUES(DimDate[Year], DimDate[Month]), CALCULATE(SUM(DimTarget[TargetSales]), MATCHALL(DimDate[Year], DimTarget[Year], DimDate[Month], DimTarget[Month])))", "$#,##0.00"),
            ("Target Achievement %", "IFERROR(DIVIDE([Total Sales], [Target Sales], 0), 0)", "0.0%"),
            ("Variance to Target", "[Total Sales] - [Target Sales]", "$#,##0.00"),
            ("Annual Forecast", "IF(MONTH(MAX(DimDate[Date])) > 0, ([Sales YTD] / MONTH(MAX(DimDate[Date]))) * 12, 0)", "$#,##0.00"),
        ]
    }

    output = """# ═════════════════════════════════════════════════════════════════════════════
# POWER BI DAX MEASURES REFERENCE
# ═════════════════════════════════════════════════════════════════════════════
# Copy each measure into Power BI Desktop (Modeling → New Measure)
# Format: Display Folder: [Folder Name] | Format: [Format Code]
# ═════════════════════════════════════════════════════════════════════════════

"""

    for folder, measures in dax_measures.items():
        output += f"\n## {folder.upper()}\n"
        output += f"{'─' * 75}\n"

        for i, (name, dax, fmt) in enumerate(measures, 1):
            output += f"\n[Measure {i}]\n"
            output += f"Name:              {name}\n"
            output += f"Display Folder:    {folder}\n"
            output += f"Format:            {fmt}\n"
            output += f"\nDAX Code:\n```\n{name} = {dax}\n```\n"

    return output


def generate_power_query_reference():
    """Generate Power Query M code reference."""

    output = """# ═════════════════════════════════════════════════════════════════════════════
# POWER QUERY M CODE REFERENCE
# ═════════════════════════════════════════════════════════════════════════════

## STEP 1: IMPORT DATA
───────────────────────────────────────────────────────────────────────────────
1. Open Power BI Desktop
2. Home → Get Data → Text/CSV
3. Select data/raw/FactSales.csv → Load
4. Repeat for each CSV file in data/raw/:
   - DimDate.csv
   - DimCustomer.csv
   - DimProduct.csv
   - DimSalesperson.csv
   - DimRegion.csv
   - DimTarget.csv


## STEP 2: APPLY POWER QUERY TRANSFORMATIONS
───────────────────────────────────────────────────────────────────────────────

### FactSales Transformations
────────────────────────────
1. Select all columns (keep all 12 columns)
2. Remove Duplicates on OrderID
3. Add Custom Column - Year:
   = Date.Year([OrderDate])
4. Add Custom Column - Month:
   = Date.Month([OrderDate])
5. Add Custom Column - Quarter:
   = Date.Quarter([OrderDate])
6. Add Custom Column - YearMonth:
   = Text.From(Date.Year([OrderDate])) & "-" & Text.PadStart(Text.From(Date.Month([OrderDate])), 2, "0")

### DimDate Transformations
──────────────────────────
1. Keep columns: Date, Day, Month, MonthName, Quarter, Year, YearMonth
2. Add Custom Column - DayOfWeek:
   = Date.DayOfWeekName([Date])
3. Add Custom Column - IsCurrentYear:
   = [Year] = Date.Year(DateTime.LocalNow())

### Dimension Transformations (DimCustomer, DimProduct, etc.)
────────────────────────────────────────────────────────────
For each dimension:
1. Trim all text columns (Transform → Format → Trim)
2. Remove Duplicates on ID column


## STEP 3: CREATE RELATIONSHIPS
───────────────────────────────────────────────────────────────────────────────
Model View → Drag to create these relationships:

1. FactSales[OrderDate]      → DimDate[Date]         (Many-to-One)
2. FactSales[CustomerID]     → DimCustomer[CustomerID] (Many-to-One)
3. FactSales[ProductID]      → DimProduct[ProductID]  (Many-to-One)
4. FactSales[SalespersonID]  → DimSalesperson[SalespersonID] (Many-to-One)
5. FactSales[RegionID]       → DimRegion[RegionID]   (Many-to-One)

All relationships: Single direction, Active


## STEP 4: MARK DATE TABLE
───────────────────────────
1. Right-click DimDate table
2. Mark as date table
3. Confirm date column: DimDate[Date]
"""

    return output


def generate_build_checklist():
    """Generate a comprehensive build checklist."""

    output = """# ═════════════════════════════════════════════════════════════════════════════
# POWER BI DASHBOARD BUILD CHECKLIST
# ═════════════════════════════════════════════════════════════════════════════
# Use this checklist to track progress while building your .pbix file
# ═════════════════════════════════════════════════════════════════════════════

## PHASE 1: DATA IMPORT & TRANSFORMATION (15-20 minutes)
─────────────────────────────────────────────────────────

### Import Data (5 min)
  ☐ Open Power BI Desktop
  ☐ Get Data → Text/CSV
  ☐ Load FactSales.csv (2,500 rows)
  ☐ Load DimDate.csv (731 rows)
  ☐ Load DimCustomer.csv (100 rows)
  ☐ Load DimProduct.csv (50 rows)
  ☐ Load DimSalesperson.csv (25 rows)
  ☐ Load DimRegion.csv (5 rows)
  ☐ Load DimTarget.csv (120 rows)

### Power Query Transformations (15 min)
  ☐ Transform FactSales:
    ☐ Remove duplicates on OrderID
    ☐ Add Year column
    ☐ Add Month column
    ☐ Add Quarter column
    ☐ Add YearMonth column
  ☐ Transform DimDate:
    ☐ Add DayOfWeek column
    ☐ Add IsCurrentYear column
  ☐ Transform Dimensions:
    ☐ Trim all text columns
    ☐ Remove duplicates

### Data Validation
  ☐ FactSales: 2,500 rows loaded
  ☐ DimDate: 731 rows loaded
  ☐ DimCustomer: 100 rows loaded
  ☐ DimProduct: 50 rows loaded
  ☐ DimSalesperson: 25 rows loaded
  ☐ DimRegion: 5 rows loaded
  ☐ DimTarget: 120 rows loaded
  ☐ No error messages in Power Query


## PHASE 2: DATA MODELING (10 minutes)
──────────────────────────────────────

### Create Relationships (5 min)
  ☐ Switch to Model view
  ☐ Create relationship: FactSales[OrderDate] → DimDate[Date]
  ☐ Create relationship: FactSales[CustomerID] → DimCustomer[CustomerID]
  ☐ Create relationship: FactSales[ProductID] → DimProduct[ProductID]
  ☐ Create relationship: FactSales[SalespersonID] → DimSalesperson[SalespersonID]
  ☐ Create relationship: FactSales[RegionID] → DimRegion[RegionID]

### Mark Date Table (3 min)
  ☐ Right-click DimDate → Mark as date table
  ☐ Confirm date column: DimDate[Date]
  ☐ Click OK

### Verify Model
  ☐ All 5 relationships created
  ☐ All relationships are Many-to-One
  ☐ All relationships are Single direction
  ☐ No circular relationships
  ☐ DimDate marked as date table


## PHASE 3: CREATE DAX MEASURES (45 minutes)
─────────────────────────────────────────────

### Create Measures Table
  ☐ Data view → Right-click → New Table
  ☐ Enter: Measures = BLANK()
  ☐ Create Measures table

### Core Metrics (8 measures)
  ☐ Total Sales
  ☐ Total Cost
  ☐ Gross Profit
  ☐ Gross Margin %
  ☐ Total Orders
  ☐ Total Quantity
  ☐ Total Customers
  ☐ Average Order Value

### Time Intelligence (8 measures)
  ☐ Sales YTD
  ☐ Sales MTD
  ☐ Sales QTD
  ☐ Sales PY
  ☐ YoY Sales %
  ☐ Sales L12M
  ☐ Sales L3M
  ☐ Profit Growth %

### Target & KPIs (4 measures)
  ☐ Target Sales
  ☐ Target Achievement %
  ☐ Variance to Target
  ☐ Annual Forecast

### Organize Measures
  ☐ Assign all measures to Display Folders
  ☐ Core Metrics folder created
  ☐ Time Intelligence folder created
  ☐ Target & KPIs folder created


## PHASE 4: BUILD DASHBOARD PAGES (90 minutes)
───────────────────────────────────────────────

### Page 1: Executive Overview (30 min)
  ☐ Create new page
  ☐ Rename to "Executive Overview"
  ☐ Add title text box

  ☐ Add slicers:
    ☐ Date slicer (Between range)
    ☐ Region slicer (Buttons style)

  ☐ Add KPI cards (row 1):
    ☐ Total Sales
    ☐ Gross Profit
    ☐ Gross Margin %
    ☐ YoY Growth %
    ☐ Target Achievement %
    ☐ Total Customers

  ☐ Add charts (row 2):
    ☐ Monthly Sales Trend (Line chart)
    ☐ Sales by Region (Donut chart)

  ☐ Add charts (row 3):
    ☐ Sales by Category (Bar chart)
    ☐ Monthly Profit Trend (Column chart)

  ☐ Add table:
    ☐ Top Customers table

### Page 2: Sales Analysis (20 min)
  ☐ Create new page
  ☐ Rename to "Sales Analysis"
  ☐ Add slicers: Month, Region, Category, Salesperson, Segment
  ☐ Add charts: Sales by Month, Sales by Region, Top Salespeople, Category Performance
  ☐ Add table: Sales Performance by Salesperson
  ☐ Add stat cards

### Page 3: Customer Analysis (20 min)
  ☐ Create new page
  ☐ Rename to "Customer Analysis"
  ☐ Add KPI cards
  ☐ Add charts: Growth Trend, Segment Distribution, City Distribution
  ☐ Add table: Top 15 Customers

### Page 4: Profitability (20 min)
  ☐ Create new page
  ☐ Rename to "Profitability"
  ☐ Add KPI cards: Sales, Cost, Profit, Margin %
  ☐ Add charts: Margin by Region, Margin by Product, Profit Trend, Margin by Segment
  ☐ Add table: Profitability by Product

### Page 5: Forecast & Targets (20 min)
  ☐ Create new page
  ☐ Rename to "Forecast & Targets"
  ☐ Add region filter
  ☐ Add KPI cards: YTD Sales, YTD Target, Achievement %, Annual Forecast
  ☐ Add charts: Actual vs Target vs Forecast, Achievement by Region, Cumulative Sales
  ☐ Add table: Monthly Performance vs Target

### Page 6: Transaction Details (15 min)
  ☐ Create new page
  ☐ Rename to "Transaction Details"
  ☐ Check: "Is drill-through page"
  ☐ Add slicers: Region, Category, Customer, Salesperson
  ☐ Add transaction detail table with all columns
  ☐ Configure scroll and sorting


## PHASE 5: SETUP DRILL-THROUGH & INTERACTIVITY (15 minutes)
─────────────────────────────────────────────────────────

### Configure Drill-Through Actions
  ☐ Page 1 - Region Donut chart:
    ☐ Format → Drill through
    ☐ Enable "Allow drill-through"
    ☐ Add field: DimRegion[Region]

  ☐ Page 1 - Customer table:
    ☐ Enable drill-through for DimCustomer[CustomerName]

  ☐ Page 2 - Salesperson chart:
    ☐ Enable drill-through for DimSalesperson[SalespersonName]

  ☐ Repeat for other dimension charts

### Test Interactivity
  ☐ All slicers filter data
  ☐ Drill-through actions work
  ☐ KPIs update correctly
  ☐ Charts respond to filters


## PHASE 6: FORMATTING & FINALIZATION (15 minutes)
──────────────────────────────────────────────────

### Apply Formatting
  ☐ File → Options → Global → Colors
  ☐ Set color theme:
    ☐ Primary: #0078D4 (Blue)
    ☐ Secondary: #107C10 (Green)
    ☐ Accent: #FFB900 (Gold)

  ☐ Each page:
    ☐ Set background: #F3F2F1 (Light Gray)
    ☐ Configure text colors
    ☐ Apply consistent formatting

### Mobile Layout
  ☐ View → Mobile layout
  ☐ Resize all visuals for mobile
  ☐ Test responsiveness

### Final Save
  ☐ File → Save As
  ☐ Filename: Power BI Sales Dashboard.pbix
  ☐ Location: Project root
  ☐ Format: Power BI Workbook (.pbix)
  ☐ Click Save


## PHASE 7: QUALITY ASSURANCE & TESTING
───────────────────────────────────────

### Data Validation
  ☐ Total Sales value is positive
  ☐ YTD values are cumulative from Jan 1
  ☐ YoY growth % calculated correctly
  ☐ No division by zero errors
  ☐ All dates in range 2023-2024

### Model Validation
  ☐ 5 relationships created
  ☐ No circular relationships
  ☐ DimDate marked as date table
  ☐ Data types match (Int64 for IDs)
  ☐ No nulls in foreign key columns

### Dashboard Validation
  ☐ Page 1: All 6 KPIs show data
  ☐ Page 1: 4 charts render correctly
  ☐ Page 1: Table shows data
  ☐ Pages 2-5: All pages have data
  ☐ Page 6: Drill-through page works
  ☐ All slicers filter correctly
  ☐ No blank or error values
  ☐ Mobile layout responsive

### Performance Check
  ☐ Dashboard loads in <3 seconds
  ☐ No lag when using slicers
  ☐ Drill-through is responsive
  ☐ All charts render smoothly


## 🎉 COMPLETION
─────────────

  ☐ All phases completed
  ☐ .pbix file saved
  ☐ All tests passed
  ☐ Dashboard ready for presentation!

**Total Time: ~3 hours**

─────────────────────────────────────────────────────────────────────────────
Pro Tips:
  • Copy/paste DAX from dax_measures_reference.txt (in this repo)
  • Follow dashboard-design/ specs for exact visual layouts
  • Test each page after creation before moving to next
  • Save your work every 15 minutes
  • Take screenshots of each completed page for documentation
─────────────────────────────────────────────────────────────────────────────
"""

    return output


def generate_project_json():
    """Generate a project metadata JSON file."""

    metadata = {
        "project": {
            "name": "Power BI Sales & Business Performance Dashboard",
            "version": "1.0",
            "description": "Professional BI dashboard for interview portfolio",
            "language": "DAX, M",
            "platforms": ["Power BI Desktop (Windows)"],
            "estimated_build_time_minutes": 180
        },
        "data": {
            "fact_tables": [
                {
                    "name": "FactSales",
                    "rows": 2500,
                    "columns": 12,
                    "file": "data/raw/FactSales.csv"
                }
            ],
            "dimension_tables": [
                {"name": "DimDate", "rows": 731, "file": "data/raw/DimDate.csv"},
                {"name": "DimCustomer", "rows": 100, "file": "data/raw/DimCustomer.csv"},
                {"name": "DimProduct", "rows": 50, "file": "data/raw/DimProduct.csv"},
                {"name": "DimSalesperson", "rows": 25, "file": "data/raw/DimSalesperson.csv"},
                {"name": "DimRegion", "rows": 5, "file": "data/raw/DimRegion.csv"},
                {"name": "DimTarget", "rows": 120, "file": "data/raw/DimTarget.csv"}
            ]
        },
        "model": {
            "relationships": 5,
            "measures": 20,
            "pages": 6
        },
        "measures_by_category": {
            "Core Metrics": 8,
            "Time Intelligence": 8,
            "Target & KPIs": 4
        },
        "pages": {
            "1": "Executive Overview",
            "2": "Sales Analysis",
            "3": "Customer Analysis",
            "4": "Profitability",
            "5": "Forecast & Targets",
            "6": "Transaction Details"
        }
    }

    return json.dumps(metadata, indent=2)


def main():
    """Generate all helper files."""

    print("🔨 Power BI Dashboard Build Automation Helper")
    print("=" * 70)

    # Generate DAX reference
    print("\n📝 Generating DAX measures reference...")
    dax_content = generate_dax_reference()
    with open('dax_measures_reference.txt', 'w') as f:
        f.write(dax_content)
    print("   ✅ dax_measures_reference.txt created")

    # Generate Power Query reference
    print("📝 Generating Power Query reference...")
    pq_content = generate_power_query_reference()
    with open('power_query_reference.txt', 'w') as f:
        f.write(pq_content)
    print("   ✅ power_query_reference.txt created")

    # Generate build checklist
    print("📝 Generating build checklist...")
    checklist = generate_build_checklist()
    with open('BUILD_CHECKLIST.txt', 'w') as f:
        f.write(checklist)
    print("   ✅ BUILD_CHECKLIST.txt created")

    # Generate project metadata
    print("📝 Generating project metadata...")
    metadata = generate_project_json()
    with open('project_metadata.json', 'w') as f:
        f.write(metadata)
    print("   ✅ project_metadata.json created")

    print("\n" + "=" * 70)
    print("✅ All helper files generated successfully!")
    print("\n📋 Generated Files:")
    print("   1. dax_measures_reference.txt   - All DAX measures (copy-paste ready)")
    print("   2. power_query_reference.txt    - Power Query M code snippets")
    print("   3. BUILD_CHECKLIST.txt          - Complete build checklist")
    print("   4. project_metadata.json        - Project configuration")
    print("\n🚀 Next Steps:")
    print("   1. Download Power BI Desktop (free)")
    print("   2. Read BUILD_PBIX_GUIDE.md")
    print("   3. Use dax_measures_reference.txt while building")
    print("   4. Follow BUILD_CHECKLIST.txt to track progress")
    print("\n⏱️  Estimated build time: 2-3 hours")
    print("=" * 70)


if __name__ == "__main__":
    main()
