# Data Model Design

## Overview

This document describes the logical data model for the Enterprise Retail Lakehouse project.

The solution follows a **Star Schema** design to support analytical reporting and business intelligence. The model is optimized for querying large volumes of retail sales data while maintaining simplicity and performance.

The data warehouse follows the Medallion Architecture:

- Bronze Layer – Raw data
- Silver Layer – Cleaned and transformed data
- Gold Layer – Business-ready dimensional model

---

# Star Schema

```
                    DimDate
                       |
                       |
DimCustomer ---- FactSales ---- DimProduct
       |               |              |
       |               |              |
    DimStore      DimCurrency    DimWeather
```

The **FactSales** table is the central fact table and is surrounded by multiple dimension tables.

---

# Fact Tables

## FactSales

Stores all retail sales transactions.

### Primary Key

OrderID

### Foreign Keys

- CustomerKey
- ProductKey
- StoreKey
- DateKey
- CurrencyKey
- WeatherKey

### Measures

- Quantity
- UnitPrice
- Discount
- TotalSales

---

## FactInventory

Stores inventory information for each warehouse.

### Foreign Keys

- ProductKey
- WarehouseKey
- DateKey

### Measures

- StockQuantity
- ReorderLevel

---

# Dimension Tables

## DimCustomer

Stores customer information.

Attributes include:

- CustomerKey
- CustomerID
- FirstName
- LastName
- Gender
- Age
- City
- State
- Country
- LoyaltyTier

This dimension will implement **Slowly Changing Dimension (SCD Type 2)** to preserve historical customer information.

---

## DimProduct

Stores product details.

Attributes include:

- ProductKey
- ProductID
- ProductName
- Category
- SubCategory
- Brand
- Supplier
- CostPrice
- SellingPrice

---

## DimDate

Stores calendar information.

Attributes include:

- DateKey
- Date
- Day
- Month
- Quarter
- Year
- WeekendFlag
- HolidayFlag

---

## DimStore

Stores store information.

Attributes include:

- StoreKey
- StoreID
- StoreName
- City
- State
- Country
- Region

---

## DimCurrency

Stores exchange rate information.

Attributes include:

- CurrencyKey
- CurrencyCode
- ExchangeRate
- EffectiveDate

---

## DimWeather

Stores daily weather information.

Attributes include:

- WeatherKey
- Date
- City
- Temperature
- Humidity
- Rainfall
- WindSpeed

---

# Relationships

FactSales has many-to-one relationships with:

- DimCustomer
- DimProduct
- DimDate
- DimStore
- DimCurrency
- DimWeather

FactInventory has many-to-one relationships with:

- DimProduct
- DimDate

---

# Slowly Changing Dimension (SCD Type 2)

The Customer dimension will use SCD Type 2.

Instead of updating customer records, a new record will be inserted whenever customer information changes.

Additional columns:

- EffectiveDate
- ExpiryDate
- IsCurrent

This preserves historical customer information for reporting and auditing purposes.

---

# Design Decisions

The following design decisions were made:

- Star Schema is used for analytical reporting.
- Delta Lake tables will store all Bronze, Silver, and Gold data.
- Surrogate keys will be used in dimension tables.
- Fact tables will store only transactional measures.
- Dimension tables will store descriptive attributes.
- Gold layer tables will be optimized for Power BI reporting.

---

# Future Enhancements

Future improvements include:

- Additional fact tables
- Customer Lifetime Value model
- Product recommendation analytics
- Sales forecasting
- Real-time streaming analytics
- Data Quality Framework