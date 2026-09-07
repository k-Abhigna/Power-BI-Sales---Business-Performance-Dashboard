# Power Query: DimDate Dimension

## Overview
Load and enrich date dimension with complete calendar attributes for time intelligence calculations.

## Power Query M Code

```powerquery
let
    // Step 1: Load from CSV
    Source = Csv.Document(File.Contents("DimDate.csv")),
    
    // Step 2: Promote headers
    PromotedHeaders = Table.PromoteHeaders(Source),
    
    // Step 3: Change data types
    ChangeTypes = Table.TransformColumnTypes(PromotedHeaders,{
        {"Date", type date},
        {"Day", Int64.Type},
        {"Month", Int64.Type},
        {"MonthName", type text},
        {"Quarter", Int64.Type},
        {"Year", Int64.Type},
        {"YearMonth", type text}
    }),
    
    // Step 4: Add additional time intelligence columns
    AddYearQuarter = Table.AddColumn(ChangeTypes, "YearQuarter", each 
        [Year] & "-Q" & Text.From([Quarter])),
    
    AddDayOfWeek = Table.AddColumn(AddYearQuarter, "DayOfWeek", each 
        Date.DayOfWeekName([Date])),
    
    AddWeekOfYear = Table.AddColumn(AddDayOfWeek, "WeekOfYear", each 
        Date.WeekOfYear([Date])),
    
    AddMonthFullName = Table.AddColumn(AddWeekOfYear, "MonthNameFull", each 
        Date.MonthName([Date])),
    
    // Step 5: Add fiscal period (if needed - adjust based on company fiscal year)
    // Assuming calendar fiscal year (can be changed)
    AddFiscalYear = Table.AddColumn(AddMonthFullName, "FiscalYear", each 
        [Year]),
    
    AddFiscalQuarter = Table.AddColumn(AddFiscalYear, "FiscalQuarter", each 
        [Quarter]),
    
    // Step 6: Add prior year date for YoY comparisons
    AddPriorYearDate = Table.AddColumn(AddFiscalQuarter, "PriorYearDate", each 
        Date.AddYears([Date], -1)),
    
    // Step 7: Mark current year and current month
    CurrentDate = DateTime.LocalNow(),
    AddIsCurrentYear = Table.AddColumn(AddPriorYearDate, "IsCurrentYear", each 
        [Year] = Date.Year(CurrentDate)),
    
    AddIsCurrentMonth = Table.AddColumn(AddIsCurrentYear, "IsCurrentMonth", each 
        [Year] = Date.Year(CurrentDate) and [Month] = Date.Month(CurrentDate)),
    
    // Step 8: Add sorting helpers
    AddMonthSort = Table.AddColumn(AddIsCurrentMonth, "MonthSort", each 
        [Month]),
    
    // Step 9: Remove any null dates
    FilteredDates = Table.SelectRows(AddMonthSort, each 
        [Date] <> null),
    
    // Step 10: Set primary key and sort
    SortedByDate = Table.Sort(FilteredDates, {{"Date", Order.Ascending}})

in
    SortedByDate
```

## Key Features
- ✓ Complete fiscal and calendar periods
- ✓ Day of week and week of year
- ✓ Prior year date for YoY calculations
- ✓ Current year/month flags for highlighting
- ✓ Sorting helpers for proper calendar display

## Date Dimension Best Practices
1. **No blanks**: Every date should be present
2. **Consistent format**: All dates in standard format
3. **Time intelligence ready**: Include PriorYearDate for advanced DAX
4. **Fiscal calendar support**: Add FiscalYear columns if needed

## Notes for Interview
- This dimension enables powerful time-intelligence DAX calculations
- PriorYearDate column simplifies YoY comparisons in DAX
- IsCurrentYear/IsCurrentMonth used for highlighting current period
- Properly designed date dimensions are critical for BI performance
