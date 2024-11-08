import os
from filter_one import extract_tickers, save_tickers_to_csv
from filter_three import process_tickers
from filter_three import format_data, update_data

def run_pipeline():
    # Run Filter 1: Extract and save tickers
    tickers = extract_tickers()
    save_tickers_to_csv(tickers)
    print("Tickers have been saved to 'tickers.csv'.")

    # Run Filter 2: Process tickers and update the historical data
    process_tickers(tickers)
    print("Historical data has been updated.")

if __name__ == "__main__":
    run_pipeline()
