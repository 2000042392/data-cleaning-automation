"""
data_pipeline.py — Main entry point.
Run from project root: python scripts/data_pipeline.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
import subprocess

BASE = Path(__file__).parent.parent

print("\n🔧 STEP 1 — Generating raw dataset …")
subprocess.run([sys.executable, str(BASE/"scripts/generate_data.py")], check=True)
df_raw = pd.read_csv(BASE/"data/raw_sales_data.csv")
print(f"   Loaded: {df_raw.shape[0]} rows × {df_raw.shape[1]} cols")

print("\n🧹 STEP 2 — Cleaning data …")
from data_cleaner import DataCleaner
cleaner = (
    DataCleaner(df_raw)
    .remove_duplicates(subset="order_id")
    .standardise_text(["region","product","status","sales_rep"])
    .parse_dates("date")
    .handle_missing({
        "date":"drop","revenue":"median","quantity":"median",
        "sales_rep":"mode","status":"mode","customer_rating":"mean"})
    .remove_outliers("revenue", method="iqr")
    .enforce_types({"quantity":"int64"})
    .add_derived_columns()
)
df_clean = cleaner.df
summary  = cleaner.summary()
audit_df = cleaner.get_audit_df()
df_clean.to_csv(BASE/"data/clean_sales_data.csv", index=False)
print(f"   Clean: {summary['clean_rows']} rows | Removed: {summary['rows_removed']} | Nulls left: {summary['clean_nulls']}")

print("\n📊 STEP 3 — Generating reports …")
from report_generator import ReportGenerator
reporter = ReportGenerator(df_clean, out_dir=str(BASE/"output"))
reporter.generate_all_charts()
excel_path = reporter.generate_excel()
html_path  = reporter.generate_html(summary, audit_df)

print(f"""
✅ Pipeline complete!
   📁 Raw CSV      → data/raw_sales_data.csv
   📁 Clean CSV    → data/clean_sales_data.csv
   📊 Excel Report → {excel_path}
   🌐 HTML Report  → {html_path}
   🖼️  Charts      → output/charts/ ({len(reporter.chart_paths)} files)
""")
