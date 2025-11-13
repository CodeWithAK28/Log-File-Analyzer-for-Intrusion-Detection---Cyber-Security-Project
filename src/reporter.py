# src/reporter.py
from pathlib import Path
import pandas as pd


def export_incidents(df, out_path="reports/incidents.csv"):
    if df is None or df.empty:
        print("No incidents to export.")
        return
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Exported incidents to {out_path}")


def save_dataframe_preview(df, out_path="reports/preview.csv", max_rows=200):
    if df is None or df.empty:
        return
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.head(max_rows).to_csv(out_path, index=False)
