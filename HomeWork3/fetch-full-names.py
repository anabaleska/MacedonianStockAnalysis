import requests
import os
import psycopg2
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Database connection details
DB_CONFIG = {
    'dbname': "msa_data",
    'user': "postgres",
    'password': "anaiman",
    'host': "localhost",
    'port': 5432
}

def add_column_if_not_exists():
    """Add a column 'full_name' to the stocks table if it doesn't exist."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'tickers' AND column_name = 'full_name') THEN
                            ALTER TABLE tickers ADD COLUMN full_name VARCHAR;
                        END IF; 
                    END; 
                    $$;
                """)
            conn.commit()
        print("Checked and added 'full_name' column if needed.")
    except psycopg2.Error as e:
        print(f"Error adding column 'full_name': {e}")

def get_company_name(ticker_name):
    """Fetch the company name from the MSE site based on ticker."""
    url = f"http://www.mse.mk/mk/symbol/{ticker_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        company_name_tag = soup.select_one("#izdavach .col-md-8.title")
        if company_name_tag:
            return company_name_tag.text.strip()

        alternative_name_tag = soup.select_one("#titleKonf2011.panel-heading")
        if alternative_name_tag:
            text = alternative_name_tag.text.strip()
            if " - " in text:
                return text.split(" - ", maxsplit=2)[-1]

        print(f"Company name not found for {ticker_name}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {ticker_name}: {e}")
        return None

def update_company_name_in_db(stock_id, company_name):
    """Update the company name in the database."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE tickers SET full_name = %s WHERE id = %s;",
                    (company_name, stock_id)
                )
            conn.commit()
        print(f"Updated stock_id {stock_id} with company name: {company_name}")
    except psycopg2.Error as e:
        print(f"Error updating stock_id {stock_id}: {e}")

def main():
    """Main function to fetch company names for tickers and update database."""
    add_column_if_not_exists()

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, ticker FROM tickers WHERE full_name IS NULL;")
                stocks = cursor.fetchall()

        for stock_id, stock_name in stocks:
            company_name = get_company_name(stock_name)
            if company_name:
                update_company_name_in_db(stock_id, company_name)
    except Exception as e:
        print(f"Error in main process: {e}")

if __name__ == "__main__":
    main()
