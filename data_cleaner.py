"""data_cleaner.py — Step-by-step data cleaning with full audit trail."""
import pandas as pd
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


class DataCleaner:
    def __init__(self, df):
        self.original = df.copy()
        self.df = df.copy()
        self.audit = []
        self._record("init", f"Loaded {len(df)} rows × {len(df.columns)} columns")

    def _record(self, step, detail, rows_affected=0):
        self.audit.append({"step":step,"detail":detail,
                           "rows_affected":rows_affected,
                           "timestamp":datetime.now().strftime("%H:%M:%S")})
        log.info(f"[{step}] {detail} (rows: {rows_affected})")

    def remove_duplicates(self, subset="order_id"):
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep="first")
        n = before - len(self.df)
        self._record("duplicates", f"Removed {n} duplicate rows (key: {subset})", n)
        return self

    def standardise_text(self, columns):
        total = 0
        for col in columns:
            if col not in self.df.columns: continue
            before = self.df[col].copy()
            self.df[col] = self.df[col].astype(str).str.strip().str.title().replace("None", np.nan)
            total += (before.astype(str) != self.df[col].astype(str)).sum()
        self._record("standardise_text", f"Standardised text columns: {columns}", total)
        return self

    def parse_dates(self, col="date"):
        b = self.df[col].isnull().sum()
        self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
        coerced = self.df[col].isnull().sum() - b
        self._record("parse_dates", f"Parsed '{col}'; {coerced} unparseable → NaT", coerced)
        return self

    def handle_missing(self, strategy):
        for col, method in strategy.items():
            if col not in self.df.columns: continue
            n = self.df[col].isnull().sum()
            if n == 0: continue
            if method == "drop":
                self.df = self.df.dropna(subset=[col])
                self._record("missing", f"Dropped {n} rows where '{col}' is null", n)
            elif method in ("mean","median","mode"):
                if method == "mean":   fill = round(self.df[col].mean(),2)
                elif method == "median": fill = self.df[col].median()
                else:                  fill = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(fill)
                self._record("missing", f"Filled '{col}' nulls with {method}={fill}", n)
            else:
                self.df[col] = self.df[col].fillna(method)
                self._record("missing", f"Filled '{col}' with '{method}'", n)
        return self

    def remove_outliers(self, col, lower=None, upper=None, method="iqr"):
        before = len(self.df)
        Q1,Q3 = self.df[col].quantile([0.25,0.75])
        iqr = Q3-Q1
        lo = lower if lower is not None else Q1 - 1.5*iqr
        hi = upper if upper is not None else Q3 + 1.5*iqr
        self.df = self.df[self.df[col].between(lo,hi,inclusive="both") | self.df[col].isnull()]
        n = before - len(self.df)
        self._record("outliers", f"Removed {n} outliers from '{col}' [{lo:.1f},{hi:.1f}]", n)
        return self

    def enforce_types(self, schema):
        for col,dtype in schema.items():
            if col not in self.df.columns: continue
            try:
                self.df[col] = self.df[col].astype(dtype)
                self._record("enforce_types", f"Cast '{col}' → {dtype}", 0)
            except Exception as e:
                self._record("enforce_types", f"Could not cast '{col}': {e}", 0)
        return self

    def add_derived_columns(self):
        self.df["year"]        = self.df["date"].dt.year
        self.df["month"]       = self.df["date"].dt.month_name()
        self.df["quarter"]     = "Q" + self.df["date"].dt.quarter.astype(str)
        self.df["net_revenue"] = (self.df["revenue"]*(1-self.df["discount_%"]/100)).round(2)
        self._record("derived", "Added year, month, quarter, net_revenue", len(self.df))
        return self

    def get_audit_df(self):
        return pd.DataFrame(self.audit)

    def summary(self):
        return {
            "original_rows":       len(self.original),
            "clean_rows":          len(self.df),
            "rows_removed":        len(self.original) - len(self.df),
            "original_nulls":      int(self.original.isnull().sum().sum()),
            "clean_nulls":         int(self.df.isnull().sum().sum()),
            "original_duplicates": int(self.original.duplicated(subset="order_id").sum()),
            "steps_run":           len(self.audit),
        }
