# Data Quality Framework

A modular data quality pipeline designed to validate, clean, and enforce data integrity using Python and Great Expectations.

---

## Overview

This project simulates a real-world data engineering workflow where raw data is ingested, validated, cleaned, and verified before being made available for downstream use.

The pipeline ensures that only high-quality, consistent, and reliable data moves forward.

---

## Pipeline Flow

1. **Data Ingestion**
   - Raw dataset is loaded from the `data/raw/` directory

2. **Initial Validation**
   - Checks for:
     - Null values
     - Duplicate records
     - Invalid formats

3. **Data Cleaning**
   - Removes:
     - Null records in critical columns
     - Duplicate entries
   - Standardizes:
     - Data types (e.g., ZIP codes as strings)
     - Field formats

4. **Re-validation**
   - Ensures cleaned data meets all quality rules

5. **Storage**
   - Clean data is saved to `data/validated/`
   - Invalid data is moved to `data/quarantine/`

6. **Expectation Validation (Great Expectations)**
   - Enforces schema and business rules:
     - Non-null constraints
     - Uniqueness
     - Regex validation
     - Field length checks

---

## Project Structure

```
data-quality-framework/
│
├── data/
│   ├── raw/
│   ├── validated/
│   └── quarantine/
│
├── logs/
│
├── scripts/
│   ├── validate.py
│   ├── ge_setup.py
│   ├── logger.py
│   └── alert.py
│
├── gx/
│
└── README.md
```
---

## Key Features

- Data validation using **Pandas**
- Automated data cleaning pipeline
- Rule-based validation using **Great Expectations**
- Logging for traceability and debugging
- Alert system for data quality failures
- Clear separation between raw, validated, and quarantined data

---

## Technologies Used

- Python
- Pandas
- Great Expectations

---

## How to Run

### 1. Validate and Clean Data

python scripts/validate.py


### 2. Run Data Quality Checks (Great Expectations)

python scripts/ge_setup.py

---

## Example Validation Rules

- `customer_id` must not be null
- `customer_id` must be unique
- `customer_zip_code_prefix` must contain only digits
- `customer_state` must be exactly 2 characters


---

## Purpose

This project demonstrates how to design a reliable data validation pipeline that ensures data consistency before it is consumed by analytics or downstream systems.
