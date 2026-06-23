# 📊 Data Cleaning & Reporting Automation

> A fully automated Python pipeline that ingests raw, messy sales data, applies systematic data-quality fixes, and produces publication-ready Excel workbooks and HTML dashboards — zero manual steps required.

---

## 🚀 Features

| Feature | Details |
|---|---|
| **Data Generation** | Realistic synthetic sales dataset with controlled noise |
| **Duplicate Removal** | Key-based deduplication with row-count audit |
| **Text Standardisation** | Strip whitespace, fix casing, normalise inconsistent labels |
| **Date Parsing** | `pd.to_datetime` with coercion; invalid dates dropped |
| **Missing Values** | Per-column strategy: drop / mean / median / mode / literal |
| **Outlier Removal** | IQR fencing with configurable bounds |
| **Type Enforcement** | Schema-driven dtype casting |
| **Derived Columns** | Year, month, quarter, net revenue (after discount) |
| **Audit Trail** | Every step logged with row counts and timestamps |
| **Excel Report** | 4-sheet workbook — cleaned data + 3 summary tabs |
| **HTML Dashboard** | Standalone self-contained report with embedded charts |
| **5 Charts** | Revenue by region, monthly trend, product mix, status, top reps |

---

## 📁 Project Structure

```
data-cleaning-automation/
├── data/
│   ├── raw_sales_data.csv       # Auto-generated messy dataset
│   └── clean_sales_data.csv     # Output of the cleaning pipeline
├── scripts/
│   ├── generate_data.py         # Synthetic dataset generator
│   ├── data_cleaner.py          # DataCleaner class with audit trail
│   ├── report_generator.py      # Charts + Excel + HTML generator
│   └── data_pipeline.py         # Main orchestrator (run this)
├── output/
│   ├── charts/                  # PNG chart files
│   ├── excel/
│   │   └── sales_report.xlsx    # Multi-sheet Excel workbook
│   └── reports/
│       └── report.html          # Self-contained HTML dashboard
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/data-cleaning-automation.git
cd data-cleaning-automation
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python scripts/data_pipeline.py
```

That's it. All outputs are generated automatically.

### 3. View results

| Output | Path |
|---|---|
| HTML Dashboard | `output/reports/report.html` |
| Excel Workbook | `output/excel/sales_report.xlsx` |
| Charts | `output/charts/*.png` |
| Clean data | `data/clean_sales_data.csv` |

---

## 🧹 Cleaning Pipeline — Step by Step

```
RAW DATA (315 rows, 10 cols, 144 nulls, 15 duplicates)
    │
    ├── 1. remove_duplicates()       → -15 rows (key: order_id)
    ├── 2. standardise_text()        → region, product, status, sales_rep
    ├── 3. parse_dates()             → errors → NaT
    ├── 4. handle_missing()
    │       date           → drop rows
    │       revenue        → fill with median
    │       quantity       → fill with median
    │       sales_rep      → fill with mode
    │       status         → fill with mode
    │       customer_rating→ fill with mean
    ├── 5. remove_outliers()         → IQR method on revenue
    ├── 6. enforce_types()           → quantity → int64
    └── 7. add_derived_columns()     → year, month, quarter, net_revenue

CLEAN DATA (287 rows, 14 cols, 0 nulls)
```

---

## 📊 Excel Workbook Structure

| Sheet | Contents |
|---|---|
| **Cleaned Data** | Full clean dataset, alternating row fill, formatted columns |
| **Regional Summary** | Aggregated KPIs per region with auto-totals formula row |
| **Product Performance** | Units sold, revenue, avg discount, revenue per unit |
| **Monthly Trend** | Month-by-month order count and net revenue |

---

## 🛠 Tech Stack

- **Python 3.10+**
- **pandas** — data manipulation and cleaning
- **NumPy** — numerical operations
- **Matplotlib / Seaborn** — chart generation
- **OpenPyXL** — Excel workbook creation with formulas and formatting

---

## 📈 Sample Output

The HTML report includes:

- **6 KPI cards** — total revenue, order count, avg order value, top region, top product, avg rating
- **6 data quality cards** — before/after row counts, nulls removed, duplicates found
- **5 embedded charts** — all base64-encoded (no external dependencies)
- **Full audit table** — every cleaning step with timestamp and rows affected

---

## 🔧 Customisation

### Use your own data

Replace the CSV path in `data_pipeline.py`:

```python
df_raw = pd.read_csv("path/to/your_data.csv")
```

### Change cleaning strategy

Edit the `handle_missing` call in `data_pipeline.py`:

```python
.handle_missing({
    "your_column": "mean",     # or "median", "mode", "drop", or any literal value
})
```

### Add more charts

Subclass or extend `ReportGenerator` with new `chart_*` methods, then call them in `generate_all_charts()`.

---

## 📝 Skills Demonstrated

- **Data preprocessing** — nulls, duplicates, inconsistent formats, outliers, type coercion
- **OOP design** — chainable `DataCleaner` class with immutable audit log
- **Automation** — single command end-to-end; no manual steps
- **Reporting** — Excel with formulas + self-contained HTML dashboard
- **Data visualisation** — 5 professionally styled charts

---

## 📄 License

MIT — free to use, adapt, and share.

---

*Built as part of a data engineering internship project.*
