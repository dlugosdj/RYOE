#!/usr/bin/env python3
"""
Read Plays.csv, coerce numeric columns to integers, and write a SQLite database `plays.db`
with a single table named `Plays`.

Assumptions:
- Numeric-like columns are detected by attempting to parse them with pandas.to_numeric
  (errors='coerce'). If any parseable numeric values exist in a column, the column will be
  converted to integer by filling NaNs with 0 and casting to int64.
"""
import os
import sqlite3
import sys
from typing import List

import pandas as pd


def find_csv(path: str) -> str:
    if os.path.isabs(path):
        return path
    here = os.path.abspath(os.path.dirname(__file__))
    candidate = os.path.join(here, path)
    return candidate


def load_and_convert(csv_path: str) -> (pd.DataFrame, List[str]):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    print(f"Loading CSV from: {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)
    converted = []

    # Try to detect numeric columns and convert them to integers
    for col in df.columns:
        # Try to parse column as numeric
        parsed = pd.to_numeric(df[col], errors="coerce")
        # If there is at least one parseable numeric value, treat column as numeric
        if parsed.notna().any():
            # Fill NaNs with 0 and cast to integer (int64)
            df[col] = parsed.fillna(0).round().astype("int64")
            converted.append(col)

    return df, converted


def write_sqlite(df: pd.DataFrame, db_path: str, table_name: str = "Plays") -> None:
    print(f"Writing DataFrame to SQLite DB: {db_path} (table: {table_name})")
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    finally:
        conn.close()


def verify_db(db_path: str, table_name: str = "Plays") -> None:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        # Check table exists
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)
        )
        found = cur.fetchone()
        if not found:
            print(f"ERROR: table '{table_name}' not found in {db_path}")
            return

        print(f"Table '{table_name}' exists in {db_path}.")

        # Show schema
        print("Schema (PRAGMA table_info):")
        for row in cur.execute(f"PRAGMA table_info('{table_name}')"):
            print(row)

        print("\nFirst 5 rows from table:")
        for row in cur.execute(f"SELECT * FROM '{table_name}' LIMIT 5;"):
            print(row)
    finally:
        conn.close()


def main():
    csv_name = "Plays.csv"
    csv_path = find_csv(csv_name)
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "plays.db")

    try:
        df, converted = load_and_convert(csv_path)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(2)

    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    if converted:
        print(f"Converted these columns to integers: {converted}")
    else:
        print("No columns detected as numeric to convert.")

    write_sqlite(df, db_path, table_name="Plays")
    print("Database written successfully.")

    # Verify
    verify_db(db_path, table_name="Plays")


if __name__ == "__main__":
    main()
