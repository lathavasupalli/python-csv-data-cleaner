"""
Python CSV Data Cleaner
=======================
A professional data cleaning utility designed for real-world freelance data cleaning tasks.
Features:
- Standardizes column headers (lowercase, snake_case, cleans special characters)
- Removes duplicate rows with detailed tracking
- Handles missing values via customizable strategies (median, mean, mode, placeholder, or drop)
- Trims whitespace and normalizes text fields (including email sanitization)
- Cleans and converts currency/numeric fields (removes $, €, commas)
- Standardizes dates into ISO 8601 (YYYY-MM-DD)
- Exports cleaned CSV and comprehensive Markdown cleaning audit report

Author: Latha Vasupalli
GitHub: https://github.com/lathavasupalli/python-csv-data-cleaner
"""

import os
import sys
import re
import argparse
from typing import Dict, Any, Optional, List

# Ensure utf-8 output encoding for console compatibility
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd


class CSVDataCleaner:
    """Core class for cleaning and transforming messy CSV datasets."""

    def __init__(self, filepath: str):
        """Initialize cleaner with path to a CSV file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Input file not found: {filepath}")

        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.df_raw: pd.DataFrame = pd.read_csv(filepath)
        self.df_clean: pd.DataFrame = self.df_raw.copy()

        # Audit tracking metrics
        self.initial_rows = len(self.df_raw)
        self.initial_cols = len(self.df_raw.columns)
        self.duplicates_removed = 0
        self.missing_handled: Dict[str, Dict[str, Any]] = {}
        self.renamed_columns: Dict[str, str] = {}
        self.transformations: List[str] = []

    def standardize_column_names(self) -> "CSVDataCleaner":
        """
        Convert column names to clean snake_case:
        - Strip leading/trailing whitespaces
        - Lowercase
        - Replace spaces, hyphens, and punctuation with underscores
        - Remove duplicate underscores
        """
        new_columns = {}
        for col in self.df_clean.columns:
            cleaned = str(col).strip().lower()
            # Replace special characters and spaces with underscore
            cleaned = re.sub(r'[\s\-+()/\\]+', '_', cleaned)
            # Remove any characters that are not alphanumeric or underscore
            cleaned = re.sub(r'[^a-z0-9_]', '', cleaned)
            # Collapse multiple underscores
            cleaned = re.sub(r'_+', '_', cleaned).strip('_')
            new_columns[col] = cleaned

        self.renamed_columns = new_columns
        self.df_clean = self.df_clean.rename(columns=new_columns)
        self.transformations.append(f"Standardized {len(new_columns)} column headers to snake_case.")
        return self

    def remove_duplicates(self, subset: Optional[List[str]] = None, keep: str = 'first') -> "CSVDataCleaner":
        """Identify and remove duplicate rows."""
        initial_count = len(self.df_clean)
        self.df_clean = self.df_clean.drop_duplicates(subset=subset, keep=keep)
        self.duplicates_removed = initial_count - len(self.df_clean)
        self.transformations.append(f"Removed {self.duplicates_removed} duplicate rows.")
        return self

    def clean_text_fields(self) -> "CSVDataCleaner":
        """Trim whitespace and sanitize string columns."""
        for col in self.df_clean.select_dtypes(include=['object', 'string']).columns:
            # Strip whitespace
            self.df_clean[col] = self.df_clean[col].astype(str).str.strip()
            # Replace 'nan' strings that resulted from NaN conversion back to actual NA
            self.df_clean[col] = self.df_clean[col].replace({'nan': None, '': None, 'None': None})

            # Check if column is email-related
            if 'email' in col.lower():
                self.df_clean[col] = self.df_clean[col].str.lower()
                self.transformations.append(f"Normalized email addresses in '{col}' to lowercase.")

        self.transformations.append("Trimmed leading/trailing whitespace across all text columns.")
        return self

    def clean_currency_and_numbers(self) -> "CSVDataCleaner":
        """Detect and clean price/currency strings ($1,250.00 -> 1250.00)."""
        for col in self.df_clean.columns:
            # Check if column name suggests currency or numeric value
            if any(term in col for term in ['price', 'cost', 'amount', 'salary', 'fee', 'total', 'usd']):
                try:
                    cleaned_series = (
                        self.df_clean[col]
                        .astype(str)
                        .str.replace(r'[\$,€£\s]', '', regex=True)
                        .replace({'nan': None, 'None': None, '': None})
                    )
                    self.df_clean[col] = pd.to_numeric(cleaned_series, errors='coerce')
                    self.transformations.append(f"Converted '{col}' to numeric float format.")
                except Exception:
                    pass
        return self

    def clean_dates(self) -> "CSVDataCleaner":
        """Attempt to standardize date columns to YYYY-MM-DD format."""
        for col in self.df_clean.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    parsed_dates = pd.to_datetime(self.df_clean[col], errors='coerce', format='mixed')
                    if parsed_dates.notna().sum() > 0:
                        self.df_clean[col] = parsed_dates.dt.strftime('%Y-%m-%d')
                        self.transformations.append(f"Standardized date column '{col}' to YYYY-MM-DD.")
                except Exception:
                    pass
        return self

    def handle_missing_values(
        self,
        strategy: str = 'auto',
        numeric_fill: str = 'median',
        categorical_fill: str = 'Unknown',
        drop_threshold: Optional[float] = None
    ) -> "CSVDataCleaner":
        """
        Handle missing/null values based on strategy.
        Strategies:
        - 'auto': Fills numeric with median, categorical with placeholder
        - 'drop': Drops rows with missing values
        - 'fill': Explicitly fills using numeric_fill & categorical_fill
        """
        for col in self.df_clean.columns:
            missing_count = int(self.df_clean[col].isna().sum())
            if missing_count > 0:
                is_numeric = pd.api.types.is_numeric_dtype(self.df_clean[col])
                action_taken = ""

                if strategy == 'drop':
                    self.df_clean.dropna(subset=[col], inplace=True)
                    action_taken = f"Dropped {missing_count} rows with missing values"
                elif strategy in ['auto', 'fill']:
                    if is_numeric:
                        if numeric_fill == 'median':
                            fill_val = self.df_clean[col].median()
                        elif numeric_fill == 'mean':
                            fill_val = round(self.df_clean[col].mean(), 2)
                        else:
                            fill_val = 0
                        self.df_clean[col] = self.df_clean[col].fillna(fill_val)
                        action_taken = f"Imputed {missing_count} missing values with {numeric_fill} ({fill_val})"
                    else:
                        fill_val = categorical_fill
                        self.df_clean[col] = self.df_clean[col].fillna(fill_val)
                        action_taken = f"Imputed {missing_count} missing values with '{fill_val}'"

                self.missing_handled[col] = {
                    "count": missing_count,
                    "action": action_taken
                }

        self.transformations.append(f"Handled missing values using strategy '{strategy}'.")
        return self

    def clean_all(self, strategy: str = 'auto') -> "CSVDataCleaner":
        """Execute the full data cleaning pipeline."""
        return (
            self.standardize_column_names()
            .remove_duplicates()
            .clean_text_fields()
            .clean_currency_and_numbers()
            .clean_dates()
            .handle_missing_values(strategy=strategy)
        )

    def export(self, output_path: str) -> str:
        """Export cleaned dataset to CSV."""
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        self.df_clean.to_csv(output_path, index=False)
        return output_path

    def generate_report(self, report_path: Optional[str] = None) -> str:
        """Generate a formatted markdown cleaning summary audit."""
        final_rows = len(self.df_clean)
        final_cols = len(self.df_clean.columns)

        report_lines = [
            "# 📊 CSV Data Cleaning Audit Report",
            f"**Source File:** `{self.filename}`  ",
            f"**Total Records (Before):** {self.initial_rows} rows | {self.initial_cols} columns  ",
            f"**Total Records (After):** {final_rows} rows | {final_cols} columns  ",
            f"**Duplicates Removed:** {self.duplicates_removed}  ",
            "",
            "## 🔄 Column Renaming Mapping",
            "| Original Column | Standardized Header (snake_case) |",
            "| :--- | :--- |"
        ]

        for orig, new in self.renamed_columns.items():
            report_lines.append(f"| `{orig}` | `{new}` |")

        report_lines.append("")
        report_lines.append("## 🩹 Missing Values Addressed")
        if self.missing_handled:
            report_lines.append("| Column | Missing Count | Action Taken |")
            report_lines.append("| :--- | :--- | :--- |")
            for col, details in self.missing_handled.items():
                report_lines.append(f"| `{col}` | {details['count']} | {details['action']} |")
        else:
            report_lines.append("No missing values were detected.")

        report_lines.append("")
        report_lines.append("## ⚡ Applied Transformations")
        for idx, trans in enumerate(self.transformations, 1):
            report_lines.append(f"{idx}. {trans}")

        report_text = "\n".join(report_lines)

        if report_path:
            os.makedirs(os.path.dirname(report_path) or '.', exist_ok=True)
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_text)

        return report_text


def main():
    parser = argparse.ArgumentParser(
        description="Python CSV Data Cleaner - Standardize headers, remove duplicates, handle missing values, and export clean data."
    )
    parser.add_argument(
        "-i", "--input",
        default="data/sample_dirty_data.csv",
        help="Path to input raw CSV file (default: data/sample_dirty_data.csv)"
    )
    parser.add_argument(
        "-o", "--output",
        default="data/cleaned_data.csv",
        help="Path to output cleaned CSV file (default: data/cleaned_data.csv)"
    )
    parser.add_argument(
        "-r", "--report",
        default="cleaning_report.md",
        help="Path to export Markdown audit report (default: cleaning_report.md)"
    )
    parser.add_argument(
        "-s", "--strategy",
        choices=["auto", "drop", "fill"],
        default="auto",
        help="Missing values strategy: auto (impute), drop (drop rows), or fill (default: auto)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("CSV Data Cleaner - Data Preprocessing Utility")
    print("=" * 60)
    print(f"Reading:  {args.input}")

    cleaner = CSVDataCleaner(args.input)
    cleaner.clean_all(strategy=args.strategy)

    out_file = cleaner.export(args.output)
    cleaner.generate_report(args.report)

    print(f"Cleaned data saved to: {out_file}")
    print(f"Audit report saved to: {args.report}")
    print("=" * 60)
    print("Summary:")
    print(f"- Rows before: {cleaner.initial_rows} | Rows after: {len(cleaner.df_clean)}")
    print(f"- Duplicates removed: {cleaner.duplicates_removed}")
    print(f"- Columns renamed: {len(cleaner.renamed_columns)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
