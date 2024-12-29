import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import ta
import logging

# Load environment variables and set up logging
# load_dotenv()
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Database connection
def get_database_connection():
    return psycopg2.connect(
        dbname="msa_data",
        user="postgres",
        password="anaiman",
        host="localhost",
        port=5432
    )


# Get all stock tickers
def get_all_tickers():
    query = "SELECT id FROM tickers"
    try:
        with get_database_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return [row[0] for row in cursor.fetchall()]
    except psycopg2.Error as e:
        logging.error(f"Error fetching tickers: {e}")
        return []


# Fetch stock data for a given ticker
def get_ticker_data(stock_id):
    query = """
    SELECT date, last_transaction, max, min, 
           avg, prom, amount, total
    FROM ticker_data WHERE id = %s ORDER BY date DESC
    """
    try:
        with get_database_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (stock_id,))
                df = pd.DataFrame(cursor.fetchall())
                if not df.empty:
                    df['date'] = pd.to_datetime(df['date'])
                return df.set_index('date')
    except psycopg2.Error as e:
        logging.error(f"Error fetching data for stock {stock_id}: {e}")
        return pd.DataFrame()


# Calculate technical indicators
def calculate_indicators(df):
    if df.empty:
        logging.warning("No data to calculate indicators.")
        return pd.DataFrame()

    # Fill missing values
    df.fillna(0, inplace=True)

    # 5 Moving Averages
    df['SMA_50'] = df['last_transaction'].rolling(window=50).mean()
    df['SMA_200'] = df['last_transaction'].rolling(window=200).mean()
    df['EMA_50'] = df['last_transaction'].ewm(span=50, adjust=False).mean()
    df['EMA_200'] = df['last_transaction'].ewm(span=200, adjust=False).mean()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['last_transaction'])
    df['BollingerHigh'] = bb.bollinger_hband()
    df['BollingerLow'] = bb.bollinger_lband()

    # 5 Oscillators
    df['RSI'] = ta.momentum.RSIIndicator(df['last_transaction'], window=14).rsi()
    df['MACD'] = ta.trend.MACD(df['last_transaction']).macd()
    df['Stochastic'] = ta.momentum.StochasticOscillator(
        df['max'], df['min'], df['last_transaction'], window=14
    ).stoch()
    df['CCI'] = ta.trend.CCIIndicator(df['max'], df['min'], df['last_transaction'], window=20).cci()
    df['Williams_R'] = ta.momentum.WilliamsRIndicator(
        df['max'], df['min'], df['last_transaction'], lbp=14
    ).williams_r()

    return df


# Generate buy/sell/hold signals
def generate_signals(df):
    if df.empty:
        logging.warning("No data available to generate signals.")
        return df

    df['signal'] = 'Hold'

    # RSI-based signals
    df.loc[df['RSI'] < 30, 'signal'] = 'Buy'
    df.loc[df['RSI'] > 70, 'signal'] = 'Sell'

    # MACD-based signals
    df.loc[df['MACD'] > 0, 'signal'] = 'Buy'
    df.loc[df['MACD'] < 0, 'signal'] = 'Sell'

    # CCI-based signals
    df.loc[df['CCI'] < -100, 'signal'] = 'Buy'
    df.loc[df['CCI'] > 100, 'signal'] = 'Sell'

    return df


# Store processed data back into the database
def store_predictions_to_db(df, stock_id, timeframe):
    if df.empty:
        logging.warning("No data to store.")
        return

    try:
        with get_database_connection() as conn:
            with conn.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS stocks_indicators (
                    id SERIAL PRIMARY KEY,
                    stock_id INT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    timeframe VARCHAR(10),
                    sma_50 FLOAT, sma_200 FLOAT, ema_50 FLOAT, ema_200 FLOAT,
                    bollinger_high FLOAT, bollinger_low FLOAT, rsi FLOAT, macd FLOAT, 
                    stochastic FLOAT, cci FLOAT, williams_r FLOAT, signal VARCHAR(10)
                );
                """
                cursor.execute(create_table_query)

                insert_query = """
                INSERT INTO stocks_indicators (
                    stock_id, date, timeframe, sma_50, sma_200, ema_50, ema_200,
                    bollinger_high, bollinger_low, rsi, macd, stochastic, 
                    cci, williams_r, signal
                ) VALUES %s
                """
                records = [
                    (
                        stock_id, row.Index, timeframe,
                        row.SMA_50, row.SMA_200, row.EMA_50, row.EMA_200,
                        row.BollingerHigh, row.BollingerLow, row.RSI, row.MACD,
                        row.Stochastic, row.CCI, row.Williams_R, row.signal
                    )
                    for row in df.itertuples()
                ]
                psycopg2.extras.execute_values(cursor, insert_query, records)
                conn.commit()
    except psycopg2.Error as e:
        logging.error(f"Error storing predictions: {e}")


# Main function to process data for all tickers and timeframes
def process_all_tickers():
    ticker_ids = get_all_tickers()
    timeframes = ['D', 'W', 'M']

    for ticker_id in ticker_ids:
        data = get_ticker_data(ticker_id)
        if not data.empty:
            for timeframe in timeframes:
                resampled_data = data.resample(timeframe).mean()
                indicators_df = calculate_indicators(resampled_data)
                signals_df = generate_signals(indicators_df)
                store_predictions_to_db(signals_df, ticker_id, timeframe)
                logging.info(f"Processed data for stock {ticker_id} ({timeframe}).")


if __name__ == "__main__":
    process_all_tickers()
