# Data Profiling Report

## Dataset

Online Retail II

## Dataset Statistics

- Total Records: 1,067,371
- Total Columns: 8
- Unique Customers: 5,942
- Unique Products: 5,305

## Data Quality Findings

- Missing Product Descriptions: 4,382
- Missing Customer IDs: 243,007
- Duplicate Records: 34,335
- Negative Quantity Records: 22,950
- Negative Price Records: 5
- Cancelled Orders: 19,494

## Initial Engineering Decisions

- Bronze layer will preserve all source records.
- Silver layer will remove duplicate records.
- Customer ID null values will be handled as guest customers.
- Negative quantities will be treated as product returns.
- Negative prices will be flagged for data quality review.
- Product descriptions with null values will be handled during Silver transformations.