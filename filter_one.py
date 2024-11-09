import requests
from bs4 import BeautifulSoup
import pandas as pd

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

def save_tickers_to_csv(tickers):
    df = pd.DataFrame(tickers, columns=['Ticker'])
    df.to_csv('tickers.csv', mode='w', header=True, index=False, chunksize=1000)
