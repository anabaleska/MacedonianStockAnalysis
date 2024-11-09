import pandas as pd
import os  # Ensure directory exists


def load_existing_data(ticker):
    file_path = f'DataFrames/{ticker}.csv'

    # Check if the file exists
    if os.path.exists(file_path):
        # Load historical data from CSV for specific ticker
        chunks = pd.read_csv(file_path, chunksize=1000)
        df = pd.concat(chunks, ignore_index=True)
        return df
    else:
        # If the file doesn't exist, return an empty DataFrame
        return pd.DataFrame()


def check_last_available_date(df):
    # If data exists, get the latest date
    if not df.empty:
        last_date = pd.to_datetime(df['Date'], dayfirst=True).max()  # Get the most recent date
        return last_date
    else:
        return None  # No data for this ticker
