# Power Query: Dimension Queries (Customer, Product, Salesperson, Region)

## DimCustomer Query

```powerquery
let
    // Load source
    Source = Csv.Document(File.Contents("DimCustomer.csv")),
    PromotedHeaders = Table.PromoteHeaders(Source),
    
    // Type conversion
    ChangeTypes = Table.TransformColumnTypes(PromotedHeaders,{
        {"CustomerID", Int64.Type},
        {"CustomerName", type text},
        {"Segment", type text},
        {"City", type text},
        {"State", type text},
        {"Country", type text}
    }),
    
    // Data quality
    RemovedDuplicates = Table.Distinct(ChangeTypes, {"CustomerID"}),
    FilterValid = Table.SelectRows(RemovedDuplicates, each [CustomerID] <> null),
    
    // Trim whitespace from text fields
    TrimmedFields = Table.TransformColumns(FilterValid,{
        {"CustomerName", Text.Trim},
        {"Segment", Text.Trim},
        {"City", Text.Trim}
    }),
    
    // Add full location
    AddFullLocation = Table.AddColumn(TrimmedFields, "Location", each 
        [City] & ", " & [State]),
    
    // Sort
    Sorted = Table.Sort(AddFullLocation, {{"CustomerID", Order.Ascending}})
in
    Sorted
```

## DimProduct Query

```powerquery
let
    // Load source
    Source = Csv.Document(File.Contents("DimProduct.csv")),
    PromotedHeaders = Table.PromoteHeaders(Source),
    
    // Type conversion
    ChangeTypes = Table.TransformColumnTypes(PromotedHeaders,{
        {"ProductID", Int64.Type},
        {"ProductName", type text},
        {"Category", type text},
        {"SubCategory", type text}
    }),
    
    // Data quality
    RemovedDuplicates = Table.Distinct(ChangeTypes, {"ProductID"}),
    FilterValid = Table.SelectRows(RemovedDuplicates, each [ProductID] <> null),
    
    // Standardize category names
    StandardizeCategory = Table.ReplaceValue(FilterValid,
        each [Category],
        each Text.Proper([Category]),
        Replacer.ReplaceValue,{"Category"}),
    
    // Trim whitespace
    TrimmedFields = Table.TransformColumns(StandardizeCategory,{
        {"ProductName", Text.Trim},
        {"Category", Text.Trim},
        {"SubCategory", Text.Trim}
    }),
    
    // Add product hierarchy level for drill-through
    AddLevel = Table.AddColumn(TrimmedFields, "HierarchyLevel", each "Product"),
    
    // Sort
    Sorted = Table.Sort(AddLevel, {{"ProductID", Order.Ascending}})
in
    Sorted
```

## DimSalesperson Query

```powerquery
let
    // Load source
    Source = Csv.Document(File.Contents("DimSalesperson.csv")),
    PromotedHeaders = Table.PromoteHeaders(Source),
    
    // Type conversion
    ChangeTypes = Table.TransformColumnTypes(PromotedHeaders,{
        {"SalespersonID", Int64.Type},
        {"SalespersonName", type text},
        {"Team", type text}
    }),
    
    // Data quality
    RemovedDuplicates = Table.Distinct(ChangeTypes, {"SalespersonID"}),
    FilterValid = Table.SelectRows(RemovedDuplicates, each 
        [SalespersonID] <> null and [Team] <> null),
    
    // Trim whitespace
    TrimmedFields = Table.TransformColumns(FilterValid,{
        {"SalespersonName", Text.Trim},
        {"Team", Text.Trim}
    }),
    
    // Standardize team names
    StandardizeTeam = Table.ReplaceValue(TrimmedFields,
        each [Team],
        each Text.Proper([Team]),
        Replacer.ReplaceValue,{"Team"}),
    
    // Sort
    Sorted = Table.Sort(StandardizeTeam, {{"SalespersonID", Order.Ascending}})
in
    Sorted
```

## DimRegion Query

```powerquery
let
    // Load source
    Source = Csv.Document(File.Contents("DimRegion.csv")),
    PromotedHeaders = Table.PromoteHeaders(Source),
    
    // Type conversion
    ChangeTypes = Table.TransformColumnTypes(PromotedHeaders,{
        {"RegionID", Int64.Type},
        {"Region", type text},
        {"Country", type text}
    }),
    
    // Data quality
    RemovedDuplicates = Table.Distinct(ChangeTypes, {"RegionID"}),
    FilterValid = Table.SelectRows(RemovedDuplicates, each [RegionID] <> null),
    
    // Trim whitespace
    TrimmedFields = Table.TransformColumns(FilterValid,{
        {"Region", Text.Trim},
        {"Country", Text.Trim}
    }),
    
    // Standardize region names
    StandardizeRegion = Table.ReplaceValue(TrimmedFields,
        each [Region],
        each Text.Proper([Region]),
        Replacer.ReplaceValue,{"Region"}),
    
    // Sort
    Sorted = Table.Sort(StandardizeRegion, {{"RegionID", Order.Ascending}})
in
    Sorted
```

## Common Transformations Applied
- ✓ **Type Safety**: Ensure all columns have correct data types
- ✓ **Duplicate Removal**: Remove any duplicate dimension keys
- ✓ **Text Cleaning**: Trim whitespace, standardize casing
- ✓ **Null Validation**: Remove records with null keys
- ✓ **Concatenation**: Create human-readable attributes (Location, etc.)

## Notes for Interview
- Dimension tables are typically small and fully loaded into memory
- Text standardization (trimming, proper case) ensures clean reports
- Removing duplicates at source prevents incorrect fact relationships
- Simple, performant dimension queries allow complex fact queries
