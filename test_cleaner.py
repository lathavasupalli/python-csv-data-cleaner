"""
Unit tests for CSVDataCleaner
"""

import os
import unittest
import tempfile
import pandas as pd
from cleaner import CSVDataCleaner


class TestCSVDataCleaner(unittest.TestCase):

    def setUp(self):
        # Create a temporary messy CSV
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8")
        csv_content = (
            " ID , Name , Email , Total Cost , Join Date \n"
            "1, Alice , ALICE@Test.com , $50.00 , 2024-01-10 \n"
            "2, Bob , bob@test.com , $100.50 , 10/01/2024 \n"
            "1, Alice , ALICE@Test.com , $50.00 , 2024-01-10 \n"
            "3, Charlie ,  , $25.00 , 2024/02/01 \n"
        )
        self.temp_file.write(csv_content)
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_standardize_column_names(self):
        cleaner = CSVDataCleaner(self.temp_file.name)
        cleaner.standardize_column_names()
        expected_cols = ["id", "name", "email", "total_cost", "join_date"]
        self.assertEqual(list(cleaner.df_clean.columns), expected_cols)

    def test_remove_duplicates(self):
        cleaner = CSVDataCleaner(self.temp_file.name)
        cleaner.standardize_column_names()
        cleaner.remove_duplicates()
        self.assertEqual(cleaner.duplicates_removed, 1)
        self.assertEqual(len(cleaner.df_clean), 3)

    def test_clean_text_fields(self):
        cleaner = CSVDataCleaner(self.temp_file.name)
        cleaner.standardize_column_names()
        cleaner.clean_text_fields()
        # Ensure email is lowercased and stripped
        alice_email = cleaner.df_clean.loc[cleaner.df_clean["id"] == 1, "email"].iloc[0]
        self.assertEqual(alice_email, "alice@test.com")

    def test_clean_currency(self):
        cleaner = CSVDataCleaner(self.temp_file.name)
        cleaner.standardize_column_names()
        cleaner.clean_currency_and_numbers()
        cost_val = cleaner.df_clean.loc[cleaner.df_clean["id"] == 1, "total_cost"].iloc[0]
        self.assertEqual(cost_val, 50.0)

    def test_clean_dates(self):
        cleaner = CSVDataCleaner(self.temp_file.name)
        cleaner.standardize_column_names()
        cleaner.clean_dates()
        bob_date = cleaner.df_clean.loc[cleaner.df_clean["id"] == 2, "join_date"].iloc[0]
        self.assertEqual(bob_date, "2024-10-01")

    def test_export_and_report(self):
        cleaner = CSVDataCleaner(self.temp_file.name)
        cleaner.clean_all()

        output_path = tempfile.mktemp(suffix=".csv")
        report_path = tempfile.mktemp(suffix=".md")

        cleaner.export(output_path)
        report = cleaner.generate_report(report_path)

        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(os.path.exists(report_path))
        self.assertIn("CSV Data Cleaning Audit Report", report)

        # Cleanup
        os.remove(output_path)
        os.remove(report_path)


if __name__ == "__main__":
    unittest.main()
