# Power Query: FactSales Transformation

## Overview
Load raw FactSales data and apply data quality, validation, and enrichment transformations.

## Power Query M Code

```powerquery
let
    // Step 1: Load from CSV
    Source = Csv.Document(File.Contents("FactSales.csv")),
    
    // Step 2: Promote headers
    PromotedHeaders = Table.PromoteHeaders(Source),
    
    // Step 3: Change data types
    ChangeTypes = Table.TransformColumnTypes(PromotedHeaders,{
        {"OrderID", Int64.Type},
        {"OrderDate", type date},
        {"CustomerID", Int64.Type},
        {"ProductID", Int64.Type},
        {"SalespersonID", Int64.Type},
        {"RegionID", Int64.Type},
        {"Quantity", Int64.Type},
        {"UnitPrice", type number},
        {"Discount", type number},
        {"Cost", type number},
        {"Sales", type number},
        {"Profit", type number}
    }),
    
    // Step 4: Data validation - remove duplicates
    RemovedDuplicates = Table.Distinct(ChangeTypes, {"OrderID"}),
    
    // Step 5: Filter invalid records
    FilteredRecords = Table.SelectRows(RemovedDuplicates, each 
        [OrderDate] <> null and 
        [CustomerID] <> null and 
        [ProductID] <> null and 
        [Quantity] > 0 and 
        [UnitPrice] > 0 and
        [Sales] > 0),
    
    // Step 6: Add Year and Month columns for easy filtering
    AddYear = Table.AddColumn(FilteredRecords, "Year", each Date.Year([OrderDate])),
    AddMonth = Table.AddColumn(AddYear, "Month", each Date.Month([OrderDate])),
    AddQuarter = Table.AddColumn(AddMonth, "Quarter", each Date.Quarter([OrderDate])),
    AddYearMonth = Table.AddColumn(AddQuarter, "YearMonth", each 
        Date.Year([OrderDate]) & "-" & Text.PadStart(Text.From(Date.Month([OrderDate])), 2, "0")),
    
    // Step 7: Calculate margin percentage
    AddMarginPct = Table.AddColumn(AddYearMonth, "MarginPct", each 
        if [Sales] <> 0 then ([Profit] / [Sales]) else 0),
    
    // Step 8: Remove helper columns (keep only necessary fact table columns)
    FinalColumns = Table.SelectColumns(AddMarginPct, {
        "OrderID",
        "OrderDate",
        "CustomerID",
        "ProductID",
        "SalespersonID",
        "RegionID",
        "Quantity",
        "UnitPrice",
        "Discount",
        "Cost",
        "Sales",
        "Profit",
        "MarginPct",
        "Year",
        "Month",
        "Quarter",
        "YearMonth"
    })

in
    FinalColumns
```

## Data Quality Checks
- ✓ Remove duplicate OrderIDs
- ✓ Validate mandatory fields (OrderDate, CustomerID, ProductID)
- ✓ Remove records with negative/zero Quantity or UnitPrice
- ✓ Validate Sales > 0
- ✓ Detect and flag outliers (optional: add Profit flag column)

## Transformations Applied
1. **Type Conversion**: Ensure correct data types
2. **Data Validation**: Remove invalid records
3. **Calculated Columns**: Add derived fields (Year, Month, Quarter, MarginPct)
4. **Denormalization**: Add temporal attributes for easier DAX calculations

## Notes for Interview
- This query demonstrates understanding of data quality processes
- Removing duplicates ensures fact table integrity
- Adding Year/Month columns is optional but improves query performance
- MarginPct is calculated here (not in DAX) for performance reasons
