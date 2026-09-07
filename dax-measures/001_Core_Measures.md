# DAX Measures: Core Sales & Profitability

## Overview
Core measures for sales, cost, and profitability calculations. These form the foundation for all other measures.

---

## 1. Total Sales

### Definition
Sum of all sales revenue across filtered context.

### DAX Code
```dax
Total Sales = SUMX(FactSales, FactSales[Sales])
```

### Alternative (more performant for large datasets)
```dax
Total Sales = SUM(FactSales[Sales])
```

### Interview Notes
- This is the most fundamental business metric
- SUMX vs SUM: SUM is more performant when column already exists
- The measure respects all filter context automatically
- Used as base for calculating margin, growth, and achievement

---

## 2. Total Cost

### Definition
Sum of all product costs (Cost × Quantity).

### DAX Code
```dax
Total Cost = SUMX(FactSales, FactSales[Cost] * FactSales[Quantity])
```

### Interview Notes
- Cost is per unit in FactSales, so multiply by Quantity
- This measure is essential for profitability analysis
- Cost should never be exposed directly to business users (security)
- Used with Sales to derive Gross Profit and Margin %

---

## 3. Gross Profit

### Definition
Difference between sales revenue and cost of goods sold.

### DAX Code
```dax
Gross Profit = [Total Sales] - [Total Cost]
```

### Interview Notes
- Simple subtraction of two measures demonstrates composition
- This is a key management KPI
- Can be negative if costs exceed sales (identifies problem areas)
- Always filtered by date to show profit trends over time

---

## 4. Gross Margin %

### Definition
Gross profit as a percentage of total sales.

### DAX Code
```dax
Gross Margin % = 
IFERROR(
    DIVIDE([Gross Profit], [Total Sales], 0),
    0
)
```

### Interview Notes
- IFERROR handles division by zero gracefully
- DIVIDE function is preferred over "/" operator in DAX
- Represents operational efficiency
- Should be between 30-70% depending on industry
- Used to identify high-margin vs low-margin products/regions

---

## 5. Total Orders

### Definition
Count of distinct orders (transactions).

### DAX Code
```dax
Total Orders = COUNTA(FactSales[OrderID])
```

### Alternative (using Distinct Count)
```dax
Total Orders = DISTINCTCOUNT(FactSales[OrderID])
```

### Interview Notes
- DISTINCTCOUNT ensures no duplicate counting
- Different from total line items (if one order has multiple rows)
- Shows transaction volume and sales velocity
- Used to calculate Average Order Value

---

## 6. Total Quantity

### Definition
Sum of all units sold.

### DAX Code
```dax
Total Quantity = SUM(FactSales[Quantity])
```

### Interview Notes
- Represents physical volume sold
- Different from Total Orders (one order can be many units)
- Used for capacity planning and inventory analysis
- Shows growth independent of price changes

---

## 7. Total Customers

### Definition
Count of unique customers in current filter context.

### DAX Code
```dax
Total Customers = DISTINCTCOUNT(FactSales[CustomerID])
```

### Interview Notes
- DISTINCTCOUNT eliminates duplicate customer counting
- Essential for customer-level analytics
- Used to calculate revenue per customer
- Changes based on date filter (shows customer acquisition)

---

## 8. Average Order Value

### Definition
Average revenue per transaction.

### DAX Code
```dax
Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)
```

### Interview Notes
- Shows sales efficiency per transaction
- Rising AOV indicates upselling success
- Declining AOV might indicate pricing pressure or discount increase
- Key metric for sales strategy evaluation

---

## Measure Organization

### Best Practices
1. **Create a dedicated "Measures" table** in Power BI data model
2. **Group related measures** in display folders:
   - Core Metrics
   - Time Intelligence
   - Growth & Targets
   - Profitability

3. **Use consistent naming**:
   - Prefix: Total, Count, Avg, etc.
   - Suffix: %, $, Dollars as needed
   
4. **Documentation in measures**:
   Add comments to complex measures
   ```dax
   // Calculate profit margin as percentage
   Gross Margin % = ...
   ```

---

## Performance Considerations

### For Large Fact Tables (>10M rows)
1. Pre-calculate known values in fact table if needed
2. Use SUM instead of SUMX when possible
3. Minimize CALCULATE usage with complex filters
4. Use semicolon (;) not comma (,) in CALCULATE filter arguments

### Optimization Example
```dax
// SLOWER - Iterates through rows
Total Sales (Slow) = SUMX(FactSales, FactSales[UnitPrice] * FactSales[Quantity])

// FASTER - Direct column sum (if pre-calculated in Power Query)
Total Sales (Fast) = SUM(FactSales[Sales])
```

---

## Testing Measures

### Validation Steps
1. **Sanity Check**: Compare with source system totals
2. **Time Aggregation**: Monthly total = sum of daily totals
3. **Dimension Check**: Sum across all categories = total
4. **Null Handling**: IFERROR prevents error values in reports

