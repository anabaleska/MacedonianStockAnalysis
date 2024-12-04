import requests
from bs4 import BeautifulSoup
from sqlalchemy import Table, Column, String, Date, Float, MetaData, Integer, Sequence, ForeignKey,PrimaryKeyConstraint
from db_config import get_database_connection
from sqlalchemy.dialects.postgresql import insert

ticker_dates={}
def extract_tickers():
    tickers_codes = []
    url = 'https://www.mse.mk/mk/stats/symbolhistory/kmb'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dropdown = soup.select_one('#Code').select('option')
    for code in dropdown:
        ticker = code.__getitem__('value').strip()
        if not any(char.isdigit() for char in ticker):
            tickers_codes.append(ticker)

    return tickers_codes

def save_tickers_to_db(tickers):
    engine = get_database_connection()
    metadata = MetaData()
    print("Database connected!")
    # Define the table
    tickers_table = Table(
        'tickers', metadata,
        Column('id', Integer, Sequence('tickers_id_seq'), primary_key=True),
        Column('ticker', String, unique=True)
    )
    metadata.create_all(engine)

    with engine.connect() as conn:
        with conn.begin():
         for ticker in tickers:
             # ticker_dates[ticker]=None
             stmt = insert(tickers_table).values(ticker=ticker)
             stmt = stmt.on_conflict_do_nothing(index_elements=['ticker'])
             try:
                 conn.execute(stmt)
                 print(f"Saving ticker: {ticker}")
             except Exception as e:
                 print(f"Error saving ticker {ticker}: {str(e)}")


def create_ticker_table():
    engine = get_database_connection()
    metadata = MetaData()
    tickers_table = Table('tickers', metadata, schema='public', autoload_with=engine)
    f=tickers_table.c.id
    # Define the table schema for each ticker
    ticker_table = Table(
        'ticker_data', metadata,
        Column('id', Integer, ForeignKey(f), nullable=False),
        Column('date', Date, nullable=False),
        Column('last_transaction', Float),
        Column('max', Float),
        Column('min', Float),
        Column('avg', Float),
        Column('prom', Float),
        Column('amount', Integer),
        Column('best', Float),
        Column('total', Float),
        PrimaryKeyConstraint('id', 'date')
    )

    metadata.create_all(engine)
    print(f"Created table for ticker_details")


# def create_tables_for_all_tickers():
#     # Fetch tickers from the 'tickers' table
#     engine = get_database_connection()
#     tickers_table = Table('tickers', MetaData(), autoload_with=engine)
#
#     with engine.connect() as conn:
#         result = conn.execute(tickers_table.select())
#         tickers = [row[1] for row in result]
#
#     # Create a table for each ticker
#     for ticker in tickers:
#         create_ticker_table()