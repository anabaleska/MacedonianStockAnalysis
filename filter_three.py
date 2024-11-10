import os
import pandas as pd
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from sympy.physics.units import years

from filter_one import extract_tickers
from filter_two import load_existing_data, check_last_available_date
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup


# def format_data(data):
#     # Ensure dates are in a consistent format
#     data['Date'] = pd.to_datetime(data['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
#     return data

def fetch_data_for_ticker(ticker, start_date):
    print(f"Fetching data for {ticker} starting from {start_date}")
    url = f"https://www.mse.mk/mk/stats/symbolhistory/{ticker}"
    data_rows = []
    date_to = datetime.today().date() - timedelta(days=1)

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    while date_to >= start_date:
            date_from = max(start_date, date_to - timedelta(days=365))

            params = {
                "FromDate": date_from.strftime("%d.%m.%Y"),
                "ToDate": date_to.strftime("%d.%m.%Y"),
            }

            response = requests.get(url, params=params)
            bs = BeautifulSoup(response.text, 'html.parser')

            table = bs.select_one('#resultsTable > tbody')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    data_row = [cell.text.strip() for cell in row.find_all('td')]
                    data_rows.append(data_row)

            date_to = date_from - timedelta(days=1)

    return data_rows


def update_data(df_existing, new_data):
    # Combine the new data with existing data
    df_combined = pd.concat([pd.DataFrame(new_data,columns=["Date", "LastTransaction", "Max", "Min", "Avg", "%Prom", "Amount", "BEST", "Total"]), df_existing], ignore_index=True)

    # Ensure no duplicate entries (based on 'Ticker' and 'Date')
    df_combined = df_combined.drop_duplicates(subset=['Date'], keep='last')

    return df_combined.dropna(axis=1, how='all')

def process_single_ticker(ticker):
    print(f"Processing ticker: {ticker}")
    df_existing = load_existing_data(ticker)
    last_date = check_last_available_date(df_existing)

    if last_date is None:
        # No data for this ticker, fetch data for the last 10 years
        last_date = datetime.today() - relativedelta(years=10)
    today=datetime.now().date() - timedelta(days=1)
    if datetime.today().weekday()==6:
        today=today-timedelta(days=1)



    if last_date.date() == today:
        print(f"Data already up to date for {ticker}, skipping.")
        return
    last_date = last_date.date()
    new_data = fetch_data_for_ticker(ticker, last_date)
    df_existing = update_data(df_existing, new_data)
    df_existing.to_csv(f'DataFrames/{ticker}.csv', index=False)
    print(f"Done for ticker {ticker}")

def process_tickers(tickers):
    # Create the directory if it doesn't exist
    if not os.path.exists('DataFrames'):
        os.makedirs('DataFrames')

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_single_ticker, tickers)





