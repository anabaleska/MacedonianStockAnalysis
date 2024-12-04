import pandas as pd
from sqlalchemy import Table, Column, String, Date, Float, MetaData, Integer
from db_config import get_database_connection
from datetime import datetime

def check_last_available_date():
    engine = get_database_connection()
    metadata = MetaData()
    ticker_table = Table('ticker_data', metadata, autoload_with=engine)


    with engine.connect() as conn:
        result = conn.execute(ticker_table.select().order_by(ticker_table.c.date.desc()).limit(1))
        row = result.fetchone()
        if row:
            last_date = row['date']
            return datetime.strptime(last_date, "%Y-%m-%d").date()
        else:
            return None