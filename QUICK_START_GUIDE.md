# ⚡ Quick Start: Build Your Power BI Dashboard in 3 Hours

**Status**: All data prepared ✅ | All specifications ready ✅ | Ready to build 🚀

---

## 🎯 What You'll Build

A professional Power BI dashboard with:
- ✅ **7 data tables** (2,500+ transactions)
- ✅ **Star schema** data model
- ✅ **20+ DAX measures** (pre-written, ready to copy)
- ✅ **6 interactive pages**
- ✅ **Advanced features**: drill-through, slicers, KPIs

**Result**: Production-ready `.pbix` file for your portfolio

---

## ⚙️ Prerequisites

### Software (Free)
- **Power BI Desktop** (Windows only) - Download from https://powerbi.microsoft.com/desktop
- That's it! Everything else is included in this repository

### Time
- **Total: ~3 hours** (can be done in one afternoon)
- Breakdown: Data (15min) + Model (10min) + Measures (45min) + Pages (90min) + Finish (15min)

### Computer
- Windows (Power BI Desktop requirement)
- ~500MB disk space
- Standard performance OK (no special hardware needed)

---

## 📋 Files You'll Use (All Included)

| File | Purpose | Status |
|------|---------|--------|
| `BUILD_PBIX_GUIDE.md` | Step-by-step instructions | ✅ Ready |
| `BUILD_CHECKLIST.txt` | Progress tracker | ✅ Ready |
| `dax_measures_reference.txt` | All DAX measures (copy-paste) | ✅ Ready |
| `power_query_reference.txt` | Power Query code snippets | ✅ Ready |
| `data/raw/*.csv` | 7 data files | ✅ Ready |
| `dax-measures/` | DAX documentation | ✅ Ready |
| `dashboard-design/` | Visual specifications | ✅ Ready |

---

## 🚀 3-Hour Timeline

### Hour 1: Foundation (60 min)

```
00:00-00:15  Open Power BI → Import 7 CSV files        [15 min]
00:15-00:35  Power Query → Transform data              [20 min]
00:35-00:45  Model view → Create 5 relationships       [10 min]
00:45-01:00  Mark DimDate as date table + verify       [15 min]
```

**Checkpoint**: All data loaded, relationships created ✅

---

### Hour 2: Measures (60 min)

```
01:00-01:45  Create 20 DAX measures (copy-paste)       [45 min]
             • Use dax_measures_reference.txt!
             • Organize into 3 folders
01:45-02:00  Verify measures + test values             [15 min]
```

**Checkpoint**: All measures working, showing correct values ✅

---

### Hour 3: Dashboard (60 min)

```
02:00-02:30  Build Page 1 (Executive Overview)         [30 min]
             • 6 KPIs + 4 charts
             • 2 slicers
             
02:30-03:15  Build Pages 2-5 (Analysis pages)          [45 min]
             • ~10 min per page
             
03:15-03:30  Build Page 6 (Drill-through) + Format     [15 min]
```

**Checkpoint**: All 6 pages complete ✅

---

## 📖 Step-by-Step Instructions

### STEP 1: Download & Open Power BI (5 min)

1. Go to https://powerbi.microsoft.com/desktop
2. Click **"Download Power BI Desktop"**
3. Install (standard defaults OK)
4. Open Power BI Desktop
5. **File** → **New**

### STEP 2: Import Data (15 min)

**Open BUILD_PBIX_GUIDE.md Section: STEP 1**

1. Home → **Get Data** → **Text/CSV**
2. Navigate to: `data/raw/FactSales.csv`
3. Click **Load**
4. **Wait for import** (takes 10 seconds)
5. **Repeat for each file**:
   ```
   ☐ FactSales.csv      (2,500 rows)
   ☐ DimDate.csv        (731 rows)
   ☐ DimCustomer.csv    (100 rows)
   ☐ DimProduct.csv     (50 rows)
   ☐ DimSalesperson.csv (25 rows)
   ☐ DimRegion.csv      (5 rows)
   ☐ DimTarget.csv      (120 rows)
   ```

**You should see 7 tables in the Fields pane on the right**

---

### STEP 3: Power Query Transformations (20 min)

**Open BUILD_PBIX_GUIDE.md Section: STEP 2**

1. Home → **Transform Data** (Power Query Editor opens)
2. **For FactSales**:
   - Home → **Remove Duplicates** (select OrderID)
   - Add Column → **Custom Column** → Name: `Year`
   - Add Column → **Custom Column** → Name: `Month`
   - Add Column → **Custom Column** → Name: `Quarter`
   - Add Column → **Custom Column** → Name: `YearMonth`
   - Home → **Close & Apply**

3. **For DimDate**:
   - Add Column → **Custom Column** → Name: `DayOfWeek`
   - Add Column → **Custom Column** → Name: `IsCurrentYear`
   - Close & Apply

4. **For DimCustomer, DimProduct, etc**:
   - Trim text columns
   - Remove duplicates
   - Close & Apply

**Reference**: Copy formulas from `power_query_reference.txt`

---

### STEP 4: Create Relationships (10 min)

**Open BUILD_PBIX_GUIDE.md Section: STEP 3**

1. Click **Model** tab (left sidebar)
2. **Drag to create relationships**:

   ```
   From                           To
   ─────────────────────────────────────────
   FactSales[OrderDate]      →  DimDate[Date]
   FactSales[CustomerID]     →  DimCustomer[CustomerID]
   FactSales[ProductID]      →  DimProduct[ProductID]
   FactSales[SalespersonID]  →  DimSalesperson[SalespersonID]
   FactSales[RegionID]       →  DimRegion[RegionID]
   ```

3. **Mark Date Table**:
   - Right-click **DimDate** → **Mark as date table**
   - Select column: `DimDate[Date]`
   - Click **OK**

---

### STEP 5: Create DAX Measures (45 min)

**Open `dax_measures_reference.txt` (generated file)**

1. Click **Data** tab (left sidebar)
2. Right-click → **New Table**
   ```
   Measures = BLANK()
   ```
3. Click **Modeling** tab
4. **New Measure** (repeat 20 times)

   For each measure:
   - Copy DAX code from `dax_measures_reference.txt`
   - Paste into formula bar
   - Set Display Folder (Core Metrics / Time Intelligence / Target & KPIs)
   - Set Format (e.g., "$#,##0.00" or "0.0%")
   - Press ✓

**Pro Tip**: Open `dax_measures_reference.txt` in Notepad while building

Example:
```
Name: Total Sales
DAX: SUM(FactSales[Sales])
Display Folder: Core Metrics
Format: $#,##0.00
```

---

### STEP 6: Build Dashboard Pages (90 min)

**Open BUILD_PBIX_GUIDE.md Sections: STEPS 5-7**

#### Page 1: Executive Overview (30 min)

1. Right-click page tab → **New page**
2. Rename to: **Executive Overview**

**Add Slicers** (top of page):
   - Insert → Slicer → Select `DimDate[Date]` → Change to "Between" range
   - Insert → Slicer → Select `DimRegion[Region]` → Change to "Buttons"

**Add KPI Cards** (row 1: 6 cards):
   - Insert → KPI Card
   - Value: `[Total Sales]` → Format: $M
   - *Repeat for*: Gross Profit, Gross Margin %, YoY Growth %, Achievement %, Customers

**Add Charts** (row 2):
   - Insert → Line Chart
     - Axis: `DimDate[Date]` (Month level)
     - Values: `[Total Sales]`
   - Insert → Donut Chart
     - Legend: `DimRegion[Region]`
     - Values: `[Total Sales]`

**Add More Charts** (row 3):
   - Insert → Horizontal Bar Chart (Sales by Category)
   - Insert → Column Chart (Monthly Profit)

**Add Table**:
   - Insert → Table
   - Columns: Customer Name, Segment, Total Sales, Total Orders

#### Pages 2-5: Analysis Pages (45 min total)

**Reference**: `BUILD_PBIX_GUIDE.md` Sections for each page

Each page takes ~12 minutes:

**Page 2 - Sales Analysis**:
- Slicers: Month, Region, Category, Salesperson
- Charts: Sales by Month, Region, Salesperson, Category
- Table: Sales Performance

**Page 3 - Customer Analysis**:
- KPI Cards: Total Customers, Avg Revenue, Repeat Rate
- Charts: Growth Trend, Segment Pie, City Bar, Revenue Distribution
- Table: Top 15 Customers

**Page 4 - Profitability**:
- KPI Cards: Sales, Cost, Profit, Margin %
- Charts: Margin by Region, Product, Profit Trend, Segment
- Table: Profitability by Product

**Page 5 - Forecast & Targets**:
- KPI Cards: YTD Sales, YTD Target, Achievement %, Forecast
- Charts: Actual vs Target, Achievement by Region, Cumulative Sales
- Table: Monthly Performance

#### Page 6: Drill-Through (15 min)

1. Create new page → Rename to **Transaction Details**
2. Right-click page tab → **Edit**
3. Check: **"Is drill-through page"** → OK
4. Insert → Table with all transaction columns:
   ```
   OrderID, OrderDate, CustomerName, ProductName, 
   Quantity, UnitPrice, Discount, Sales, Cost, Profit
   ```
5. Go back to Page 1 → Select Region chart
6. Format → Drill through → Enable "Allow drill-through"
7. Add drill field: `DimRegion[Region]`

---

### STEP 7: Format & Save (15 min)

1. **Apply Color Theme**:
   - File → Options → Global → Colors
   - Primary: #0078D4 (Blue)
   - Secondary: #107C10 (Green)
   - Accent: #FFB900 (Gold)

2. **Mobile Layout**:
   - View → Mobile layout
   - Resize visuals for mobile view

3. **Save as .PBIX**:
   - File → **Save As**
   - Filename: `Power BI Sales Dashboard.pbix`
   - Location: Project root folder
   - **Save!**

---

## ✅ Verification Checklist

**Use BUILD_CHECKLIST.txt to track everything**

Quick checklist:
- [ ] All 7 tables loaded (data view)
- [ ] All 5 relationships created (model view)
- [ ] DimDate marked as date table
- [ ] 20 measures created and organized
- [ ] Page 1: All 6 KPIs showing values
- [ ] Page 1: All 4 charts showing data
- [ ] Pages 2-5: All pages complete
- [ ] Page 6: Drill-through working
- [ ] All slicers filter data
- [ ] .pbix file saved

---

## 🎯 Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| "Measure shows blank/error" | Wrap in IFERROR: `= IFERROR([Your Measure], 0)` |
| "Chart shows no data" | Check slicer filters aren't hiding all data |
| "Relationship error" | Verify data types match (both should be Int64 for IDs) |
| "YoY growth shows error" | Use IFERROR with DIVIDE: `DIVIDE([Sales], [Sales PY], 0)` |
| "Date relationship not working" | Make sure DimDate is marked as date table |
| "Drill-through not working" | Verify cross-filter direction is "Single" |

**Full troubleshooting**: See BUILD_PBIX_GUIDE.md

---

## 📚 Reference Files You'll Need Open

Keep these files open while building:

1. **dax_measures_reference.txt** → Copy DAX formulas
2. **power_query_reference.txt** → Power Query code
3. **BUILD_CHECKLIST.txt** → Track your progress
4. **BUILD_PBIX_GUIDE.md** → Detailed step-by-step

---

## 🚀 After You're Done

### 1. Test Your Dashboard (15 min)
   - [ ] Click each slicer → Data updates
   - [ ] Drill-through: Right-click chart → Drill through works
   - [ ] Mobile view: Switch to mobile → Charts resize
   - [ ] All pages load without errors

### 2. Practice Your Demo (30 min)
   - [ ] 1-minute overview of each page
   - [ ] Explain a key design decision
   - [ ] Show drill-through capability
   - [ ] Discuss a DAX measure

### 3. Prepare for Interviews
   - [ ] Read INTERVIEW_GUIDE.md
   - [ ] Know 3-5 key talking points
   - [ ] Practice explaining the data model
   - [ ] Be ready to show the dashboard

---

## 💡 Pro Tips

1. **Save Often**: Save every 15 minutes (Ctrl+S)
2. **Copy from Reference Files**: Don't type DAX - copy/paste!
3. **One Page at a Time**: Don't try to build everything at once
4. **Test as You Go**: Add a measure → test it → move on
5. **Use Naming Convention**: Keep measure names exactly as documented
6. **Take Screenshots**: Screenshot each completed page
7. **Read Comments**: All documentation explains the "why"

---

## 🏆 You're Ready!

Everything you need is in this repository:
- ✅ Data files (ready to import)
- ✅ DAX measures (ready to copy)
- ✅ Visual specifications (ready to recreate)
- ✅ Power Query code (ready to paste)
- ✅ Complete checklist (ready to follow)

**Time to build: ~3 hours**
**Result: Production-ready Power BI dashboard**

---

## 📞 Still Have Questions?

1. **Data issues**: Check `data/` folder and CSV files
2. **DAX questions**: See `dax-measures/` documentation
3. **Visual design**: See `dashboard-design/` folder
4. **Interview prep**: Read `INTERVIEW_GUIDE.md`
5. **Build steps**: See `BUILD_PBIX_GUIDE.md`

---

## 🎉 Get Started Now!

1. **Download Power BI Desktop** (free)
2. **Open BUILD_PBIX_GUIDE.md**
3. **Follow Step 1: Import Data**
4. **Track progress in BUILD_CHECKLIST.txt**

You've got this! Build your dashboard and show what you can do! 🚀

---

**Questions? Everything is documented in this repository. You have everything you need to succeed!**
