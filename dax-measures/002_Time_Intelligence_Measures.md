# DAX Measures: Time Intelligence Calculations

## Overview
Advanced time-intelligence measures using DAX date functions. This demonstrates mastery of complex DAX patterns.

---

## 1. Sales YTD (Year-To-Date)

### Definition
Cumulative sales from the start of the fiscal year to the current date.

### DAX Code
```dax
Sales YTD = 
CALCULATE(
    [Total Sales],
    DATESBETWEEN(
        DimDate[Date],
        DATE(YEAR(MAX(DimDate[Date])), 1, 1),
        MAX(DimDate[Date])
    )
)
```

### Advanced Version (Intelligent Time Intelligence)
```dax
Sales YTD = 
TOTALYTD([Total Sales], DimDate[Date])
```

### Interview Notes
- TOTALYTD is a convenience function - equivalent to CALCULATE + DATESBETWEEN
- YTD restarts each January (or fiscal year start)
- Essential for budget tracking
- Shows progress toward annual goals
- Respects all other filter context (region, product, etc.)

---

## 2. Sales MTD (Month-To-Date)

### Definition
Cumulative sales from the start of the current month to current date.

### DAX Code
```dax
Sales MTD = 
CALCULATE(
    [Total Sales],
    DATESBETWEEN(
        DimDate[Date],
        DATE(YEAR(MAX(DimDate[Date])), MONTH(MAX(DimDate[Date])), 1),
        MAX(DimDate[Date])
    )
)
```

### Interview Notes
- Used for short-term performance tracking
- Highly sensitive to current date in data
- Updated daily for real-time dashboards
- Shows current month trajectory vs monthly target

---

## 3. Sales Previous Year (PY)

### Definition
Sales for the same period in the prior year.

### DAX Code
```dax
Sales PY = 
CALCULATE(
    [Total Sales],
    DATESBETWEEN(
        DimDate[Date],
        DATE(YEAR(MAX(DimDate[Date])) - 1, MONTH(MIN(DimDate[Date])), DAY(MIN(DimDate[Date]))),
        DATE(YEAR(MAX(DimDate[Date])) - 1, MONTH(MAX(DimDate[Date])), DAY(MAX(DimDate[Date])))
    )
)
```

### Simplified (Using SAMEPERIODLASTYEAR)
```dax
Sales PY = 
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[Date])
)
```

### Interview Notes
- SAMEPERIODLASTYEAR is the easiest to understand
- Requires continuous date dimension (every date present)
- Essential for YoY comparisons
- Works correctly across leap years

---

## 4. YoY Sales Growth %

### Definition
Percentage change in sales compared to same period previous year.

### DAX Code
```dax
YoY Sales % = 
IFERROR(
    DIVIDE(
        [Total Sales] - [Sales PY],
        [Sales PY],
        0
    ),
    0
)
```

### Interview Notes
- Fundamental growth metric
- Can be negative (indicating decline)
- When PY sales are zero, result shows as 0 (not infinity)
- Used to identify accelerating/decelerating trends
- Critical for strategic decision-making

---

## 5. Sales QTD (Quarter-To-Date)

### Definition
Cumulative sales from quarter start to current date.

### DAX Code
```dax
Sales QTD = 
TOTALQTD([Total Sales], DimDate[Date])
```

### Manual Version
```dax
Sales QTD = 
CALCULATE(
    [Total Sales],
    DATESBETWEEN(
        DimDate[Date],
        DATE(YEAR(MAX(DimDate[Date])), (QUARTER(MAX(DimDate[Date])) - 1) * 3 + 1, 1),
        MAX(DimDate[Date])
    )
)
```

### Interview Notes
- TOTALQTD handles quarter boundaries automatically
- Quarter quarters: Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Oct-Dec)
- Less common than YTD but useful for quarterly reviews
- Used for board presentations and quarterly reporting

---

## 6. Sales Last 12 Months (Rolling)

### Definition
Sales for the trailing 12-month period.

### DAX Code
```dax
Sales L12M = 
CALCULATE(
    [Total Sales],
    DATESBETWEEN(
        DimDate[Date],
        DATE(YEAR(MAX(DimDate[Date])) - 1, MONTH(MAX(DimDate[Date])), DAY(MAX(DimDate[Date]))) + 1,
        MAX(DimDate[Date])
    )
)
```

### Alternative (Simpler but less precise)
```dax
Sales L12M = 
CALCULATE(
    [Total Sales],
    FILTER(
        DimDate,
        DimDate[Date] >= MAX(DimDate[Date]) - 365
    )
)
```

### Interview Notes
- L12M smooths seasonal variations
- Useful for annualized performance metrics
- More stable than single-year comparisons
- Used to detect long-term trends

---

## 7. Sales Last 3 Months (Rolling)

### Definition
Sales for the trailing 3-month (quarter-like) period.

### DAX Code
```dax
Sales L3M = 
CALCULATE(
    [Total Sales],
    FILTER(
        DimDate,
        DimDate[Date] >= MAX(DimDate[Date]) - 90
        && DimDate[Date] <= MAX(DimDate[Date])
    )
)
```

### Interview Notes
- Recent performance indicator
- Smooths weekly/daily volatility
- Useful for momentum analysis
- Often used in executive dashboards

---

## 8. Sales Prior Month

### Definition
Sales for the month immediately preceding the current month.

### DAX Code
```dax
Sales Prior Month = 
CALCULATE(
    [Total Sales],
    DATESBETWEEN(
        DimDate[Date],
        DATE(YEAR(MAX(DimDate[Date])), MONTH(MAX(DimDate[Date])) - 1, 1),
        DATE(YEAR(MAX(DimDate[Date])), MONTH(MAX(DimDate[Date])), 0)
    )
)
```

### Interview Notes
- Used for month-over-month (MoM) comparisons
- Shows sequential performance changes
- Less stable than YoY but shows current momentum
- Requires careful handling of month boundaries

---

## Advanced Pattern: Month-Over-Month Change

### Definition
Percentage change from previous month to current month.

### DAX Code
```dax
Sales MoM % = 
IFERROR(
    DIVIDE(
        [Total Sales] - [Sales Prior Month],
        [Sales Prior Month],
        0
    ),
    0
)
```

---

## Common Time Intelligence Pitfalls

### ❌ AVOID
```dax
// Wrong - Date context is lost
Sales YTD (Bad) = CALCULATE([Total Sales], "Jan-Dec")

// Wrong - Doesn't respect filter context
Sales YTD (Bad) = SUMX(FactSales, IF(MONTH(FactSales[OrderDate]) <= MONTH(TODAY()), FactSales[Sales], 0))
```

### ✓ CORRECT
```dax
// Correct - Uses TOTALYTD helper function
Sales YTD = TOTALYTD([Total Sales], DimDate[Date])

// Correct - Uses DATESBETWEEN for explicit control
Sales YTD = CALCULATE([Total Sales], DATESBETWEEN(DimDate[Date], ...))
```

---

## Performance Optimization

### Date Table Requirements
1. **Continuous**: No gaps between first and last date
2. **Sorted**: Dates in ascending order for aggregation
3. **Mark as Date Table**: Set in Power BI (Data View → Mark as Date Table)
4. **Unique values**: No duplicate dates

### Measure Caching
- DAX Query Folding doesn't apply to DAX (only Power Query)
- Time intelligence measures are calculated at query time
- For large datasets, consider materializing YTD/QTD/MTD in Power Query

---

## Testing Time Intelligence Measures

### Validation Approach
```
For Month = "Jan 2024":
  YTD should = Jan sales
For Month = "Mar 2024":
  YTD should = Jan + Feb + Mar sales
For Month = "Feb 2024":
  PY should = Feb 2023 sales
For Month = "Feb 2024":
  YoY Growth % should = (Feb 2024 - Feb 2023) / Feb 2023
```

