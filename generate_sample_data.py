#!/usr/bin/env python3
"""
Generate sample sales data for Power BI Dashboard
Creates a realistic star schema dataset with 2 years of sales data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============= Dimensions =============

# DimDate - 2 years of daily data
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='D')

dim_date = pd.DataFrame({
    'Date': date_range,
    'Day': date_range.day,
    'Month': date_range.month,
    'MonthName': date_range.strftime('%B'),
    'Quarter': date_range.quarter,
    'Year': date_range.year,
    'YearMonth': date_range.strftime('%Y-%m')
})

# DimCustomer
customers = {
    'CustomerID': range(1001, 1101),  # 100 customers
    'CustomerName': [f'Customer {i}' for i in range(1, 101)],
    'Segment': np.random.choice(['Enterprise', 'Mid-Market', 'SMB'], 100),
    'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                               'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'], 100),
    'State': np.random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'PA'], 100),
    'Country': 'USA'
}
dim_customer = pd.DataFrame(customers)

# DimProduct
dim_product = pd.DataFrame({
    'ProductID': range(2001, 2051),  # 50 products
    'ProductName': [f'Product {i}' for i in range(1, 51)],
    'Category': np.random.choice(['Electronics', 'Software', 'Services', 'Hardware'], 50),
    'SubCategory': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], 50)
})

# DimSalesperson
dim_salesperson = pd.DataFrame({
    'SalespersonID': range(3001, 3026),  # 25 salespeople
    'SalespersonName': [f'Salesperson {i}' for i in range(1, 26)],
    'Team': np.random.choice(['North', 'South', 'East', 'West'], 25)
})

# DimRegion
dim_region = pd.DataFrame({
    'RegionID': range(4001, 4006),  # 5 regions
    'Region': ['North', 'South', 'East', 'West', 'Central'],
    'Country': 'USA'
})

# ============= Fact Table =============

# Generate realistic sales transactions
n_orders = 2500

order_ids = range(5001, 5001 + n_orders)
dates = [start_date + timedelta(days=random.randint(0, 730)) for _ in range(n_orders)]

fact_sales = pd.DataFrame({
    'OrderID': order_ids,
    'OrderDate': dates,
    'CustomerID': [np.random.choice(dim_customer['CustomerID']) for _ in range(n_orders)],
    'ProductID': [np.random.choice(dim_product['ProductID']) for _ in range(n_orders)],
    'SalespersonID': [np.random.choice(dim_salesperson['SalespersonID']) for _ in range(n_orders)],
    'RegionID': [np.random.choice(dim_region['RegionID']) for _ in range(n_orders)],
    'Quantity': np.random.randint(1, 20, n_orders),
    'UnitPrice': np.random.uniform(50, 500, n_orders).round(2),
    'Discount': np.random.choice([0, 0.05, 0.1, 0.15, 0.2], n_orders),
    'Cost': np.random.uniform(20, 300, n_orders).round(2)
})

# Calculate Sales = (UnitPrice * Quantity) * (1 - Discount)
fact_sales['Sales'] = (fact_sales['UnitPrice'] * fact_sales['Quantity'] * (1 - fact_sales['Discount'])).round(2)
fact_sales['Profit'] = (fact_sales['Sales'] - (fact_sales['Cost'] * fact_sales['Quantity'])).round(2)

# Sort by date
fact_sales = fact_sales.sort_values('OrderDate').reset_index(drop=True)

# ============= Create Target Data =============

target_data = []
for year in [2023, 2024]:
    for month in range(1, 13):
        for region_id in dim_region['RegionID']:
            base_target = np.random.uniform(80000, 150000)
            target_data.append({
                'Year': year,
                'Month': month,
                'RegionID': region_id,
                'TargetSales': base_target
            })

dim_target = pd.DataFrame(target_data)

# ============= Export to CSV =============

print("Generating sample data...")
dim_date.to_csv('data/raw/DimDate.csv', index=False)
dim_customer.to_csv('data/raw/DimCustomer.csv', index=False)
dim_product.to_csv('data/raw/DimProduct.csv', index=False)
dim_salesperson.to_csv('data/raw/DimSalesperson.csv', index=False)
dim_region.to_csv('data/raw/DimRegion.csv', index=False)
fact_sales.to_csv('data/raw/FactSales.csv', index=False)
dim_target.to_csv('data/raw/DimTarget.csv', index=False)

print(f"✓ DimDate: {len(dim_date)} rows")
print(f"✓ DimCustomer: {len(dim_customer)} rows")
print(f"✓ DimProduct: {len(dim_product)} rows")
print(f"✓ DimSalesperson: {len(dim_salesperson)} rows")
print(f"✓ DimRegion: {len(dim_region)} rows")
print(f"✓ FactSales: {len(fact_sales)} rows")
print(f"✓ DimTarget: {len(dim_target)} rows")
print("\nAll data files created in data/raw/")
