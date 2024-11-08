
import pandas as pd
from datetime import date,datetime, timedelta
from filter_one import extract_tickers
import requests
from bs4 import BeautifulSoup
from filter_two import load_existing_data, check_last_available_date
import re


def format_data(data):
    # Ensure dates are in a consistent format
    data[1] = pd.to_datetime(data['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Ensure prices are formatted correctly (using commas for thousands, dot for decimal)
    #data['Open'] = data['Open'].apply(lambda x: f"{x:,.2f}")
    #data['Close'] = data['Close'].apply(lambda x: f"{x:,.2f}")

    return data


def fetch_data_for_ticker(ticker, start_date):
    print(f"Fetching data for {ticker} starting from {start_date}")
    url = f"https://www.mse.mk/mk/stats/symbolhistory/{ticker}"
    df = []
    date_to = date.today() - timedelta(days=1)
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
            #df.append(["Date", "LastTransaction", "Max", "Min", "Avg", "%Prom", "Amount", "BEST", "Total"])
            rows = table.find_all('tr')
            for row in rows:
                data_row = [cell.text.strip() for cell in row.find_all('td')]
                df.append(data_row)

        date_to = date_from - timedelta(days=1)


    return pd.DataFrame(df, columns=["Date", "LastTransaction", "Max", "Min", "Avg", "%Prom", "Amount", "BEST", "Total"])




def update_data(df_existing, new_data):
    # Combine the new data with existing data
    df_combined = pd.concat([new_data,df_existing], ignore_index=True)

    # Ensure no duplicate entries (based on 'Ticker' and 'Date')
    df_combined = df_combined.drop_duplicates(subset=['Date'], keep='last')

    return df_combined


def fetch_missing_data(ticker, last_date):
    # Define the starting point for the missing data (next day after last available date)
    start_date = (last_date + pd.DateOffset(days=1)).strftime('%Y-%m-%d')

    # Fetch data from the stock exchange
    new_data = fetch_data_for_ticker(ticker, start_date)  # Fetch data from the ticker API

    # Format the new data (apply date and price formatting)
    new_data = format_data(new_data)

    return new_data



def process_tickers(tickers):
    for ticker in tickers:
        df_existing = load_existing_data(ticker)
        # Check the last available date for each ticker
        last_date = check_last_available_date( df_existing)
        print(f"Proccessing for ticker {ticker}")
        if last_date.date()== datetime.now().date()-timedelta(days=1):
            continue
        if last_date is None:
            # No data for this ticker, fetch data for the last 10 years
            start_date = (datetime.now() - pd.DateOffset(years=10)).strftime('%Y-%m-%d')
            new_data = fetch_data_for_ticker(ticker, start_date)
            # new_data = format_data(new_data)## TODO
            df_existing = update_data(df_existing, new_data) ## TODO
        else:
            # Data exists for this ticker, fetch missing data starting from the last available date
            new_data = fetch_missing_data(ticker, last_date)
            df_existing = update_data(df_existing, new_data)

        df_existing.to_csv(f'DataFrames/{ticker}.csv', index=False)
        print(f'Done for ticker {ticker}')


