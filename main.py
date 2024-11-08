import os
from filter_one import extract_tickers, save_tickers_to_csv
from filter_three import process_tickers
from filter_three import format_data, update_data
import time

def run_pipeline():
    start_time = time.time()
    # Run Filter 1: Extract and save tickers
    tickers = extract_tickers()
    save_tickers_to_csv(tickers)
    print("Tickers have been saved to 'tickers.csv'.")

    # Run Filter 2: Process tickers and update the historical data
    process_tickers(tickers)
    print("Historical data has been updated.")

    end_time = time.time()
    #Calculate the total time taken for pipline to run an
    total_time = end_time - start_time
    print(f"Data pipeline completed in {total_time:.2f} seconds.")

if __name__ == "__main__":
    run_pipeline()