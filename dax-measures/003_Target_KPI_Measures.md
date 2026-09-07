# DAX Measures: Target & KPI Calculations

## Overview
Measures for comparing actual sales against targets, tracking performance, and identifying variances.

---

## 1. Target Sales (Monthly)

### Definition
Retrieve sales target for current month-region combination from DimTarget table.

### DAX Code
```dax
Target Sales = 
SUMX(
    VALUES(DimDate[Year], DimDate[Month]),
    CALCULATE(
        SUM(DimTarget[TargetSales]),
        MATCHALL(
            DimDate[Year], DimTarget[Year],
            DimDate[Month], DimTarget[Month],
            DimRegion[RegionID], DimTarget[RegionID]
        )
    )
)
```

### Simplified Version
```dax
Target Sales = 
CALCULATE(
    SUM(DimTarget[TargetSales]),
    MATCHALL(
        DimDate[Year], DimTarget[Year],
        DimDate[Month], DimTarget[Month],
        DimRegion[RegionID], DimTarget[RegionID]
    )
)
```

### Interview Notes
- Assumes DimTarget table with Year, Month, RegionID, TargetSales columns
- MATCHALL ensures correct matching on multiple fields
- Targets are typically set monthly by region
- Can be extended to include product-level targets
- Alternative: Use LOOKUP function if simpler structure

---

## 2. Target Achievement %

### Definition
Percentage of sales target achieved in current period.

### DAX Code
```dax
Target Achievement % = 
IFERROR(
    DIVIDE([Total Sales], [Target Sales], 0),
    0
)
```

### Formatted Version (as percentage)
```dax
Target Achievement % = 
IFERROR(
    DIVIDE(
        [Total Sales], 
        [Target Sales], 
        0
    ),
    0
)
// Format as: 0.0% in Power BI
```

### Interview Notes
- Shows % of target achieved (100% = target met)
- >100% indicates over-achievement (bonus territory)
- <100% indicates shortfall
- Critical KPI for sales management
- Used in incentive calculations

---

## 3. Variance to Target

### Definition
Dollar amount by which actual sales differ from target.

### DAX Code
```dax
Variance to Target = [Total Sales] - [Target Sales]
```

### Absolute Variance (always positive)
```dax
Variance to Target (Abs) = ABS([Total Sales] - [Target Sales])
```

### Interview Notes
- Positive variance = over-achievement (good)
- Negative variance = shortfall (bad)
- Directly actionable: tells sales team exact dollar gap
- Used in waterfall charts to show contribution to variance
- Can be broken down by region/product for root cause analysis

---

## 4. Target Achievement Status (Conditional)

### Definition
Status indicator showing whether target is achieved, at-risk, or exceeded.

### DAX Code
```dax
Target Achievement Status = 
VAR CurrentAchievement = [Target Achievement %]
RETURN
    IF(
        CurrentAchievement >= 1,
        "Achieved",
        IF(CurrentAchievement >= 0.9, "At Risk", "Below Target")
    )
```

### Interview Notes
- Creates business logic for status indicators
- At-Risk threshold typically 90% (3 weeks remaining = 3/4 of month)
- Used in conditional formatting for red/yellow/green visualization
- Helps identify early warning signals
- Common in Balanced Scorecard approaches

---

## 5. Sales Quota (Alternative approach without lookup)

### Definition
Simplified annual quota divided by number of days in year.

### DAX Code
```dax
Sales Daily Quota = 
VAR AnnualQuota = 250000
VAR DaysInYear = 365
RETURN
    AnnualQuota / DaysInYear
```

### Interview Notes
- Use when targets not stored in separate table
- Less flexible than target table approach
- Useful for quick dashboards
- Should be replaced with proper target management system

---

## 6. Profit Growth %

### Definition
Percentage change in gross profit vs. same period prior year.

### DAX Code
```dax
Profit Growth % = 
IFERROR(
    DIVIDE(
        [Gross Profit] - [Profit PY],
        [Profit PY],
        0
    ),
    0
)
```

### Where Profit PY is defined as
```dax
Profit PY = 
CALCULATE(
    [Gross Profit],
    SAMEPERIODLASTYEAR(DimDate[Date])
)
```

### Interview Notes
- Profit growth differs from sales growth (driven by margins)
- Can be negative if margins compress
- Key indicator of operational efficiency
- Identifies when revenue growth doesn't translate to profit growth

---

## 7. Days to Target Achievement

### Definition
Estimated days needed to achieve annual target based on current run rate.

### DAX Code
```dax
Days to Target = 
VAR YTDSales = [Sales YTD]
VAR DailyRunRate = YTDSales / WEEKDAY(MAX(DimDate[Date]))
VAR RemainingTarget = [Target Sales] * 12 - YTDSales
VAR DaysNeeded = 
    IF(
        DailyRunRate > 0,
        ROUND(RemainingTarget / DailyRunRate, 0),
        0
    )
RETURN
    DaysNeeded
```

### Interview Notes
- Forward-looking metric showing time to goal
- Assumes constant run rate (not realistic but useful signal)
- Values > 365 indicate target won't be met
- Used for early forecasting
- More accurate after first quarter when patterns emerge

---

## 8. Annual Target Forecast

### Definition
Projected annual sales based on YTD performance.

### DAX Code
```dax
Annual Forecast = 
VAR YTDSales = [Sales YTD]
VAR MonthsElapsed = MONTH(MAX(DimDate[Date]))
VAR ProjectedAnnual = 
    IF(
        MonthsElapsed > 0,
        (YTDSales / MonthsElapsed) * 12,
        0
    )
RETURN
    ProjectedAnnual
```

### Interview Notes
- Based on actual YTD performance
- Self-corrects monthly as new data comes in
- Compared against annual target to show forecast gap/surplus
- Used in financial forecasting
- More reliable after Q2/Q3

---

## 9. Target Variance %

### Definition
Percentage variance from target.

### DAX Code
```dax
Target Variance % = 
IFERROR(
    DIVIDE(
        [Total Sales] - [Target Sales],
        [Target Sales],
        0
    ),
    0
)
```

### Interview Notes
- Positive % = over-target
- Negative % = under-target
- -10% = 10% below target
- Used for performance rankings
- Can be sorted to identify best/worst performers

---

## Segment Analysis: Target by Customer Segment

### Pattern for Segment-Specific Targets
```dax
Target Sales - Enterprise = 
CALCULATE(
    [Target Sales],
    DimCustomer[Segment] = "Enterprise"
)

Target Achievement % - Enterprise = 
DIVIDE(
    CALCULATE([Total Sales], DimCustomer[Segment] = "Enterprise"),
    [Target Sales - Enterprise],
    0
)
```

### Interview Notes
- Apply same measure pattern to Region, Product, Salesperson
- Creates mini-dashboards for each segment
- Enables drill-through to detail level

---

## Visualization Recommendations

### KPI Cards
```
┌─────────────────────┐
│  Target Achievement │
│        112%         │ ✓ Over-achieving
│  $1.2M of $1.1M     │
└─────────────────────┘
```

### Status Indicators
- ✓ Green: >100% achievement
- 🟡 Yellow: 90-100% (at-risk)
- ❌ Red: <90% (below target)

### Trend Indicators
- ↑ Green: Growing toward target
- → Gray: Flat trend
- ↓ Red: Declining from target

