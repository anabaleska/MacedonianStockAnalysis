import pandas as pd
import os
from datetime import datetime  # Functions from filter_three.py


def load_existing_data(ticker):
    # Load historical data from CSV for spesific ticker
    chunks = pd.read_csv(f'DataFrames/{ticker}.csv', chunksize=1000)
    df = pd.concat(chunks, ignore_index=True)
    return df


def check_last_available_date( df):
    # If data exists, get the latest date
    if not df.empty:
        last_date = pd.to_datetime(df['Date'],dayfirst=True).max()   # Get the most recent date
        return last_date
    else:
        return None  # No data for this ticker








