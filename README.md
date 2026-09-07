# Power BI Sales & Business Performance Dashboard
## Portfolio Project for BI/Data Analyst Interviews

![Status](https://img.shields.io/badge/Status-Complete-brightgreen) ![Version](https://img.shields.io/badge/Version-1.0-blue) ![Power%20BI](https://img.shields.io/badge/Power%20BI-2024-yellow)

---

## 📋 Project Overview

A professional, interview-ready Power BI dashboard demonstrating enterprise BI best practices. Designed to showcase skills in:

- ✅ Data modeling (star schema)
- ✅ Power Query data transformation
- ✅ DAX time intelligence & calculations
- ✅ KPI design & business metrics
- ✅ Interactive dashboard design
- ✅ Performance optimization

**Scenario:** Multi-regional sales company analyzing revenue, profitability, and performance against targets.

---

## 🎯 Key Features

### Data Model (Star Schema)
- **1 Fact Table** (FactSales): 2,500 transactions
- **5 Dimensions**: Date, Customer, Product, Salesperson, Region
- **Proper relationships**: All one-to-many, no circular dependencies
- **Clean data**: Validated, deduplicated, normalized

### 20+ DAX Measures
- Core: Total Sales, Profit, Margin %
- Time Intelligence: YTD, YoY Growth, L12M, Prior Month
- KPIs: Target Achievement %, Variance to Target, Forecast
- All measures follow best practices (DIVIDE with defaults, TOTALYTD, etc.)

### 6 Interactive Dashboard Pages
1. **Executive Overview**: KPIs, regional mix, profit trends
2. **Sales Analysis**: Performance by region, salesperson, product
3. **Customer Analysis**: Segmentation, lifetime value, concentration
4. **Profitability**: Margin analysis, waterfall, cost drivers
5. **Forecast & Targets**: Actual vs target vs forecast
6. **Drill-Through**: Transaction-level detail accessible from any page

### User Experience
- Global date/region/product slicers
- Multi-level drill-through
- Conditional formatting for status
- Mobile-responsive design
- Reset filters button

---

## 📁 Project Structure

```
power-bi-sales-dashboard/
├── data/
│   ├── raw/                          # CSV source files
│   │   ├── FactSales.csv            # 2,500 transactions
│   │   ├── DimDate.csv              # 731 daily records
│   │   ├── DimCustomer.csv          # 100 customers
│   │   ├── DimProduct.csv           # 50 products
│   │   ├── DimSalesperson.csv       # 25 salespeople
│   │   ├── DimRegion.csv            # 5 regions
│   │   └── DimTarget.csv            # Monthly targets
│   └── processed/                    # (For Power Query output, if needed)
│
├── power-query/                      # Power Query M scripts
│   ├── 01_FactSales_Query.md         # Fact table transformation
│   ├── 02_DimDate_Query.md           # Date dimension with time intelligence prep
│   └── 03_Dimensions_Queries.md      # Customer, Product, Salesperson, Region
│
├── dax-measures/                     # DAX measure definitions
│   ├── 001_Core_Measures.md          # Sales, Cost, Profit
│   ├── 002_Time_Intelligence_Measures.md  # YTD, YoY, L12M
│   └── 003_Target_KPI_Measures.md    # Achievement %, Variance, Forecast
│
├── dashboard-design/                 # Visual specifications
│   ├── PAGE_1_EXECUTIVE_OVERVIEW.md  # Detailed design for Page 1
│   ├── PAGE_2_SALES_ANALYSIS.md      # Detailed design for Page 2
│   └── PAGES_3_4_5_6_SUMMARY.md      # Summary design for Pages 3-6
│
├── docs/                             # Documentation
│   └── INTERVIEW_GUIDE.md            # Complete interview prep (THIS IS KEY!)
│
├── generate_sample_data.py           # Python script to create sample CSVs
├── README.md                         # This file
└── LICENSE                           # Project license
```

---

## 🚀 Getting Started

### Prerequisites
- Power BI Desktop (latest version)
- Python 3.7+ (for data generation)
- ~100MB disk space

### Setup Instructions

#### 1. Generate Sample Data
```bash
# Install dependencies
pip install pandas numpy

# Generate CSV files
python generate_sample_data.py
```
Output: CSV files in `data/raw/` folder

#### 2. Create Power BI Model

**Step A: Import Data**
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Load each file from `data/raw/`:
   - FactSales.csv
   - DimDate.csv
   - DimCustomer.csv
   - DimProduct.csv
   - DimSalesperson.csv
   - DimRegion.csv
   - DimTarget.csv

**Step B: Apply Power Query Transformations**
- Refer to `power-query/` folder for each transformation
- Copy/paste M code from markdown files into Power Query editor
- Test each query before loading

**Step C: Create Relationships**
| From | To | Relationship |
|------|----|----|
| FactSales[OrderDate] | DimDate[Date] | Many-to-One |
| FactSales[CustomerID] | DimCustomer[CustomerID] | Many-to-One |
| FactSales[ProductID] | DimProduct[ProductID] | Many-to-One |
| FactSales[SalespersonID] | DimSalesperson[SalespersonID] | Many-to-One |
| FactSales[RegionID] | DimRegion[RegionID] | Many-to-One |

**Step D: Create DAX Measures**
- Create new table: "Measures"
- Add all measures from `dax-measures/` folder
- Organize in display folders:
  - Core Metrics
  - Time Intelligence
  - Target & KPIs

**Step E: Build Dashboard Pages**
- Refer to `dashboard-design/` folder for each page
- Recreate visuals per specifications
- Set up drill-through actions
- Configure slicers

#### 3. Interview Preparation
Read `docs/INTERVIEW_GUIDE.md` thoroughly:
- Understand business logic behind each measure
- Practice explaining dashboard purpose
- Prepare answers to common scenarios

---

## 📊 Data Model Diagram

```
                    DimDate
                      │
                      │ (OrderDate)
                      │
FactSales ────────────┼──────── DimCustomer
│           │         │              │
│           │         │         (CustomerID)
│      (ProductID)    │
│           │         │
│      DimProduct     │
│                     │
│          (SalespersonID)
│                     │
│             DimSalesperson
│
└─ (RegionID)
       │
    DimRegion

All relationships: Many-to-One (fact to dimensions)
Direction: Single (from fact to dimension)
```

---

## 🎨 Dashboard Pages at a Glance

| Page | Purpose | Key Visuals | Audience |
|------|---------|-----------|----------|
| 1 - Executive | Overall health check | 6 KPIs, 5 charts | C-Suite, Executives |
| 2 - Sales | Deep-dive by dimension | 4 charts, tables | Sales Manager |
| 3 - Customer | Customer segmentation | Pareto, growth trend | Customer Success |
| 4 - Profit | Margin analysis | Waterfall, scatter | Finance, Product |
| 5 - Forecast | Annual planning | Actual vs Target vs Forecast | CFO, Planning |
| 6 - Drill | Transaction detail | Full transaction table | All stakeholders |

---

## 💡 Key DAX Patterns Demonstrated

### 1. Time Intelligence (TOTALYTD)
```dax
Sales YTD = TOTALYTD([Total Sales], DimDate[Date])
```

### 2. Year-over-Year Comparison (SAMEPERIODLASTYEAR)
```dax
Sales PY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))
```

### 3. Safe Division (IFERROR + DIVIDE)
```dax
Gross Margin % = IFERROR(DIVIDE([Gross Profit], [Total Sales], 0), 0)
```

### 4. Conditional Logic
```dax
Target Achievement Status = 
IF([Target Achievement %] >= 1, "Achieved",
   IF([Target Achievement %] >= 0.9, "At Risk", "Below Target"))
```

### 5. CALCULATE with DATESBETWEEN
```dax
Sales L12M = CALCULATE(
    [Total Sales],
    FILTER(DimDate, DimDate[Date] >= MAX(DimDate[Date]) - 365)
)
```

---

## 📈 What This Project Demonstrates

### Technical Skills
- ✅ **SQL**: Data extraction & transformation concepts
- ✅ **Power Query**: Data cleaning, merging, denormalization
- ✅ **DAX**: Advanced calculations, time intelligence, error handling
- ✅ **Data Modeling**: Star schema design, relationship management
- ✅ **Power BI**: Visuals, drill-through, bookmarks, formatting
- ✅ **Python**: Automated data generation

### Business Skills
- ✅ **KPI Definition**: How to measure business performance
- ✅ **Stakeholder Communication**: Dashboard for different audiences
- ✅ **Root Cause Analysis**: Multi-level drill-through for investigation
- ✅ **Decision Support**: How reports enable action

### Best Practices
- ✅ Clean code (descriptive names, documentation)
- ✅ Performance optimization (no unnecessary aggregations)
- ✅ Error handling (IFERROR, DIVIDE with defaults)
- ✅ Professional design (minimal clutter, clear hierarchy)
- ✅ Scalability (works with 10x data size)

---

## 🎓 Interview Talking Points

### "Walk me through your data model"
*See: INTERVIEW_GUIDE.md → PART 1, Question 1*

Key points:
- Star schema: 1 fact, 5 dimensions
- All one-to-many relationships
- FactSales (2,500 transactions) links to DimDate for time analysis

### "Tell me about your DAX measures"
*See: INTERVIEW_GUIDE.md → PART 3, Question 5*

Key points:
- 20+ measures organized in 3 groups
- Time intelligence (TOTALYTD, SAMEPERIODLASTYEAR)
- Proper error handling (IFERROR + DIVIDE)

### "How did you approach the dashboard?"
*See: INTERVIEW_GUIDE.md → PART 4, Question 7*

Key points:
- Design driven by business questions
- Minimal clutter (4-5 visuals per page)
- Clear drill-through path for investigation

### "How would you troubleshoot a sales drop?"
*See: INTERVIEW_GUIDE.md → PART 5, Scenario 1*

Key points:
- Systematic approach: facts → dimensions → detail
- Use drill-through to find root cause
- Propose data-driven solutions

---

## 📚 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `power-query/01_FactSales_Query.md` | Data transformation details | Technical |
| `power-query/02_DimDate_Query.md` | Date dimension setup | Technical |
| `dax-measures/001_Core_Measures.md` | Sales/Profit calculations | Technical |
| `dax-measures/002_Time_Intelligence_Measures.md` | YTD/YoY/L12M patterns | Technical |
| `dax-measures/003_Target_KPI_Measures.md` | Target & forecast measures | Technical |
| `dashboard-design/PAGE_1_EXECUTIVE_OVERVIEW.md` | Page 1 detailed design | Designer |
| `dashboard-design/PAGE_2_SALES_ANALYSIS.md` | Page 2 detailed design | Designer |
| `docs/INTERVIEW_GUIDE.md` | **Interview preparation** | **You!** |

---

## 🔍 Quality Assurance

### Data Validation Checklist
- [ ] All CSV files generate without errors
- [ ] No null values in foreign key columns
- [ ] All OrderDates within 2023-2024 range
- [ ] All Sales > 0, Quantity > 0
- [ ] Total Sales = Sum of individual transactions

### Model Validation
- [ ] All relationships created (5 total)
- [ ] No circular relationships
- [ ] DimDate marked as date table
- [ ] All foreign key data types match (Int64)

### Measure Validation
- [ ] Total Sales matches sum of CSV
- [ ] YTD values logical (cumulative from Jan 1)
- [ ] YoY % calculated correctly (Div by zero handled)
- [ ] Target Achievement % between 0-200% range

### Dashboard Validation
- [ ] KPI cards show expected values
- [ ] Charts render without errors
- [ ] Slicers filter correctly
- [ ] Drill-through actions work
- [ ] Mobile responsive layout confirmed

---

## 🚨 Common Issues & Solutions

### Issue: "Measure returns blank or error"
**Solution:** 
- Check for circular relationships
- Verify DimDate is marked as date table
- Use IFERROR wrapper to catch division errors
- Ensure dimension tables have no blanks in key columns

### Issue: "Dashboard is slow"
**Solution:**
- Reduce number of visuals per page
- Use aggregated tables for large fact tables
- Avoid custom visuals (slower than native)
- Verify all relationships are correct

### Issue: "YoY numbers don't match"
**Solution:**
- Confirm DimDate has every single day (no gaps)
- Check SAMEPERIODLASTYEAR is using correct date column
- Verify data exists for same dates in prior year
- Use IFERROR to handle missing prior year data

### Issue: "Can't find data in drill-through"
**Solution:**
- Confirm cross-filter direction is "Single"
- Verify drill-through field matches filter value
- Check that source page filters are applied
- Ensure target page has data matching filter criteria

---

## 📞 Support & Questions

### For Technical Questions
Refer to the relevant markdown file in `power-query/` or `dax-measures/`

### For Design Questions
Refer to `dashboard-design/` folder

### For Interview Prep
Read `docs/INTERVIEW_GUIDE.md` (comprehensive!)

### For Data Issues
Check sample data generation: `python generate_sample_data.py`

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-15 | Initial release |
| | | - 6 dashboard pages |
| | | - 20+ DAX measures |
| | | - Complete documentation |
| | | - Interview guide |

---

## 📄 License

This project is provided as-is for educational and interview preparation purposes.

---

## 🎯 Next Steps After Building

1. **Customize for Your Story**
   - Adjust sample data to match your industry
   - Change KPIs to reflect your experience
   - Use company names/products if presenting to specific company

2. **Add Your Own Data**
   - Replace sample CSVs with real data (anonymized)
   - Show actual performance scenarios
   - Demonstrate business impact

3. **Extend the Project**
   - Add forecasting model (if you have ML skills)
   - Add customer segmentation (K-means clustering)
   - Add financial analysis (cohort, retention)

4. **Prepare Presentation**
   - Practice explaining each page (2 min per page = 12 min total)
   - Prepare answers to scenario questions
   - Have drill-through ready to show interactivity

---

## ✨ Final Tips for Interview Success

### Before the Interview
- ✅ Build the dashboard end-to-end (don't just read about it)
- ✅ Practice explaining each page in 1-2 minutes
- ✅ Know every DAX measure (be ready to write it on whiteboard)
- ✅ Prepare 2-3 scenarios: "Sales dropped", "Margin compressed", etc.
- ✅ Read the INTERVIEW_GUIDE.md 3+ times until confident

### During the Interview
- ✅ Start with business context ("This is a sales company...")
- ✅ Show the dashboard (let visuals tell the story)
- ✅ Explain design decisions (not just "I made 5 charts")
- ✅ Demonstrate interactivity (use slicers, drill-through)
- ✅ Link to business impact ("This saves 40 hours/month of reporting")

### After Showing Dashboard
- ✅ Ask "What questions would you like me to answer with this data?"
- ✅ Use the scenario questions to demonstrate analytical thinking
- ✅ Show you can explain trade-offs (performance vs. detail)
- ✅ Discuss how you'd evolve it for production

---

## 🎉 You've Got This!

This portfolio project demonstrates everything an enterprise BI team looks for:
- Technical depth (DAX, Power Query, data modeling)
- Business acumen (KPIs, storytelling, analysis)
- Professional presentation (design, documentation, communication)

Walk into that interview confident that you have a production-quality example to discuss.

**Good luck! 🚀**

---

*Created for Power BI portfolio development and interview preparation. Use as a template for your own projects.*

