from datetime import datetime, timedelta
from sqlalchemy import Table, MetaData
from HomeWork1.db_config import get_database_connection
from sqlalchemy.dialects.postgresql import insert
from functools import partial
from sqlalchemy import text

from dateutil.relativedelta import relativedelta
from filter_two import check_last_available_date
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

def format_number(value):
    if value is None or value == "":
        return None
    value = value.replace(',', '.')
    if '.' in value:
        parts = value.split('.')
        if len(parts) > 2:
            value = value.replace('.', '', value.count('.') - 1)
    return value

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
                    data_dict = {
                        "Date": data_row[0],
                        "LastTransaction": format_number(data_row[1]),
                        "Max": format_number(data_row[2]),
                        "Min": format_number(data_row[3]),
                        "Avg": format_number(data_row[4]),
                        "Prom": format_number(data_row[5]),
                        "Amount": format_number(data_row[6]),
                        "BEST": format_number(data_row[7]),
                        "Total": format_number(data_row[8])
                    }
                    data_rows.append(data_dict)

            date_to = date_from - timedelta(days=1)

    return data_rows


def update_data(ticker, dictionary):
    engine = get_database_connection()
    metadata = MetaData()
    ticker_table = Table('ticker_data', metadata, autoload_with=engine)
    with engine.connect() as conn:
        conn = conn.execution_options(autocommit=True)
        ticker_id_query = text('SELECT id FROM tickers WHERE ticker = :ticker')
        result = conn.execute(ticker_id_query, {'ticker': ticker})
        ticker_id = result.scalar()

    with engine.connect() as conn:
        with conn.begin():
            for row in dictionary:
                        insert_stmt = insert(ticker_table).values(
                            id=ticker_id,
                            date=row['Date'],
                            last_transaction=float(row['LastTransaction']) if row['LastTransaction'] else None,
                            max=float(row['Max'])  if row['Max'] else None,
                            min=float(row['Min'])  if row['Min'] else None,
                            avg=float(row['Avg'])  if row['Avg'] else None,
                            prom = float(row['Prom']) if row['Prom'] else None,
                        amount = int(float(row['Amount'])) if row['Amount'] else None,
                        best = float(row['BEST']) if row['BEST'] else None,
                        total = float(row['Total']) if row['Total'] else None
                        )
                        #insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['Date','id'])
                        try:

                            conn.execute(insert_stmt)

                        except Exception as e:
                            print(f"Error saving ticker {ticker}: {str(e)}")
        print(f"Saving ticker: {ticker}")

def process_single_ticker(ticker,last_date):
    print(f"Processing ticker: {ticker}")


    new_data = fetch_data_for_ticker(ticker, last_date)
    update_data(ticker, new_data)
    # df_existing.to_csv(f'DataFrames/{ticker}.csv', index=False)
    print(f"Done for ticker {ticker}")

def process_tickers(tickers):
    last_date = check_last_available_date()

    if last_date is None:
        last_date = datetime.today() - relativedelta(years=10)
    today = datetime.now().date() - timedelta(days=1)
    if datetime.today().weekday() == 6:
        today = today - timedelta(days=1)

    if last_date.date() == today:
        print(f"Data already up to date for , skipping.")
        return
    last_date = last_date.date()
    process_with_date = partial(process_single_ticker, last_date=last_date)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_with_date, tickers)





