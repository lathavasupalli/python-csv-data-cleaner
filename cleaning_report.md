# 📊 CSV Data Cleaning Audit Report
**Source File:** `sample_dirty_data.csv`  
**Total Records (Before):** 10 rows | 9 columns  
**Total Records (After):** 8 rows | 9 columns  
**Duplicates Removed:** 2  

## 🔄 Column Renaming Mapping
| Original Column | Standardized Header (snake_case) |
| :--- | :--- |
| `  Customer ID  ` | `customer_id` |
| ` Full Name ` | `full_name` |
| ` Email Address ` | `email_address` |
| `Phone Number` | `phone_number` |
| `Order Date` | `order_date` |
| ` Product Name ` | `product_name` |
| `Price (USD)` | `price_usd` |
| ` Status ` | `status` |
| ` Notes ` | `notes` |

## 🩹 Missing Values Addressed
| Column | Missing Count | Action Taken |
| :--- | :--- | :--- |
| `full_name` | 1 | Imputed 1 missing values with 'Unknown' |
| `email_address` | 1 | Imputed 1 missing values with 'Unknown' |
| `phone_number` | 1 | Imputed 1 missing values with 'Unknown' |
| `product_name` | 1 | Imputed 1 missing values with 'Unknown' |
| `status` | 1 | Imputed 1 missing values with 'Unknown' |
| `notes` | 2 | Imputed 2 missing values with 'Unknown' |

## ⚡ Applied Transformations
1. Standardized 9 column headers to snake_case.
2. Removed 2 duplicate rows.
3. Normalized email addresses in 'email_address' to lowercase.
4. Trimmed leading/trailing whitespace across all text columns.
5. Converted 'price_usd' to numeric float format.
6. Standardized date column 'order_date' to YYYY-MM-DD.
7. Handled missing values using strategy 'auto'.