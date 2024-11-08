import pandas as pd
import os
from datetime import datetime  # Functions from filter_three.py


def load_existing_data(ticker):
    # Load historical data from CSV for spesific ticker
    if os.path.exists(f'DataFrames/{ticker}.csv'):
        df = pd.read_csv(f'DataFrames/{ticker}.csv')
    else:
        df = pd.DataFrame(columns=["Date", "LastTransaction", "Max", "Min", "Avg", "%Prom", "Amount", "BEST", "Total"])  # Empty dataframe if no data exists
    return df


def check_last_available_date( df):
    # Filter data for the specific ticker
    #ticker_data = df[df['Ticker'] == ticker]

    # If data exists, get the latest date
    if not df.empty:
        last_date = pd.to_datetime(df['Date'],dayfirst=True).max()   # Get the most recent date
        return last_date
    else:
        return None  # No data for this ticker








