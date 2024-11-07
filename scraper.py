import requests
from bs4 import BeautifulSoup
import os
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

tickers = extract_tickers()
df = pd.DataFrame(tickers)
df.to_csv('tickers.csv')