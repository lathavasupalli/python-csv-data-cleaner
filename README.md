# 🧹 Python CSV Data Cleaner

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pandas](https://img.shields.io/badge/pandas-data%20wrangling-150458.svg)](https://pandas.pydata.org/)
[![Tests](https://img.shields.io/badge/tests-6%20passed-brightgreen.svg)]()

A modular, production-ready Python data preprocessing tool built for real-world **freelance data cleaning and ETL tasks**. It cleans messy spreadsheets and CSV exports by removing duplicates, imputing missing values, standardizing headers, formatting currency and dates, and exporting an automated markdown audit report.

---

## 💼 Why This Matters for Freelancing & Internships

Clients on platforms like **Upwork, Fiverr, and Freelancer** frequently export messy CSV/Excel files from CRMs (HubSpot, Salesforce), e-commerce platforms (Shopify, WooCommerce), and web scrapers. These datasets typically suffer from:
- Inconsistent headers with spaces and special symbols
- Duplicate transaction and contact records
- Mixed date formats (`MM/DD/YYYY`, `DD-MM-YYYY`, `YYYY/MM/DD`)
- Currency strings containing symbols and commas (`$1,250.00`)
- Missing email addresses, names, and phone numbers

This tool automates the entire cleaning workflow in seconds and generates a client-ready **Audit Report** proving the transformations applied.

---

## ✨ Features

- **Header Standardization:** Converts inconsistent column names into database-ready `snake_case` (strips whitespace, replaces punctuation and spaces with underscores).
- **Duplicate Removal:** Identifies and eliminates redundant rows while maintaining record order.
- **Missing Value Handling:**
  - *Numerical columns:* Imputes with median (resilient to outliers) or mean.
  - *Categorical columns:* Fills with customizable placeholders (e.g., `'Unknown'`) or drops missing rows.
- **Text & Email Sanitization:** Trims leading/trailing whitespace across all text columns and lowercases email addresses.
- **Currency & Number Parsing:** Strips currency symbols (`$`, `€`, `£`) and commas, converting numeric fields to proper float values.
- **Date Normalization:** Parses varied date representations and normalizes them into standard ISO `YYYY-MM-DD`.
- **Audit Reporting:** Automatically writes a Markdown summary (`cleaning_report.md`) logging every change, duplicate count, and column mapping.

---

## 📂 Project Structure

```text
python-csv-data-cleaner/
├── cleaner.py                 # Core cleaner class and CLI entry point
├── test_cleaner.py            # Automated unit test suite (6 tests)
├── requirements.txt           # Project dependencies
├── cleaning_report.md         # Generated audit report sample
├── data/
│   ├── sample_dirty_data.csv  # Messy sample dataset
│   └── cleaned_data.csv       # Preprocessed, cleaned dataset
└── README.md                  # Documentation and usage guide
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/lathavasupalli/python-csv-data-cleaner.git
cd python-csv-data-cleaner
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Cleaner
Run on the included sample dataset with default settings:
```bash
python cleaner.py
```

Or specify custom inputs and outputs:
```bash
python cleaner.py -i data/my_dirty_file.csv -o data/cleaned_output.csv -r audit_report.md --strategy auto
```

---

## ⚙️ CLI Options

| Option | Short | Default | Description |
| :--- | :--- | :--- | :--- |
| `--input` | `-i` | `data/sample_dirty_data.csv` | Path to the source raw CSV file |
| `--output` | `-o` | `data/cleaned_data.csv` | Destination path for the cleaned CSV file |
| `--report` | `-r` | `cleaning_report.md` | Destination path for the Markdown audit report |
| `--strategy` | `-s` | `auto` | Missing values strategy: `auto`, `drop`, or `fill` |

---

## 📊 Before & After Comparison

### 🔴 Before Cleaning (`sample_dirty_data.csv`)
```csv
  Customer ID  , Full Name , Email Address ,Phone Number,Order Date, Product Name ,Price (USD), Status , Notes 
CUST001,John Doe,John.Doe@Gmail.com,+1 (555) 019-2834,2024/01/15,Wireless Mouse,$120.50,Delivered,First order
CUST002, Jane Smith ,jane_smith@yahoo.com,555-019-2835,15-01-2024, Gaming Laptop ,"$1,250.00",Delivered,Expedited
CUST001,John Doe,John.Doe@Gmail.com,+1 (555) 019-2834,2024/01/15,Wireless Mouse,$120.50,Delivered,First order
CUST003, Robert Johnson ,,555-019-2836,2024-02-01,USB-C Cable,$45.00,,Needs invoice
```

### 🟢 After Cleaning (`cleaned_data.csv`)
```csv
customer_id,full_name,email_address,phone_number,order_date,product_name,price_usd,status,notes
CUST001,John Doe,john.doe@gmail.com,+1 (555) 019-2834,2024-01-15,Wireless Mouse,120.5,Delivered,First order
CUST002,Jane Smith,jane_smith@yahoo.com,555-019-2835,2024-01-15,Gaming Laptop,1250.0,Delivered,Expedited
CUST003,Robert Johnson,Unknown,555-019-2836,2024-02-01,USB-C Cable,45.0,Unknown,Needs invoice
```

---

## 🧪 Running Tests

Verify all unit tests pass:
```bash
python -m unittest test_cleaner.py
```

Output:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.092s

OK
```

---

## 👩‍💻 Author

**Latha Vasupalli**
- **Portfolio:** [lathavasupalli.github.io/latha-portfolio](https://lathavasupalli.github.io/latha-portfolio/)
- **GitHub:** [@lathavasupalli](https://github.com/lathavasupalli)
- **Email:** [lathavasupalli14@gmail.com](mailto:lathavasupalli14@gmail.com)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
