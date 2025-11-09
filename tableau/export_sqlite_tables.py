# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd

conn = sqlite3.connect('filings_demo_step3.sqlite')

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

def report_quarter(date):
    if pd.isna(date):
        return pd.NaT
    year = date.year
    month = date.month
    day = date.day
    if month <= 3 or (month == 4 and day <= 4):
        return pd.Timestamp(year, 1, 1)   # Q1 → 1 jan
    elif month <= 6 or (month == 7 and day <= 4):
        return pd.Timestamp(year, 4, 1)   # Q2 → 1 apr
    elif month <= 9 or (month == 10 and day <= 4):
        return pd.Timestamp(year, 7, 1)   # Q3 → 1 jul
    else:
        return pd.Timestamp(year, 10, 1)  # Q4 → 1 oct

for table in tables['name']:
    df = pd.read_sql(f'SELECT * FROM {table}', conn)

    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = df[col].str.replace(' ', '').astype(float)
            except:
                pass

    if table == 'Forms':
        df['ValueDate'] = pd.to_datetime(df['ValueDate'], format='%Y-%m-%d', errors='coerce')
        df['ReportQuarter'] = df['ValueDate'].apply(report_quarter)

    df.to_csv(f'{table}.csv', index=False, encoding='utf-8')
    print(f'Table {table} has been saved to {table}.csv')

conn.close()