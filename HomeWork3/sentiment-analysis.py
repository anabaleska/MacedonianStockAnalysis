import os
import psycopg2
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
from transformers import pipeline
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax

# Database connection configuration
DB_CONFIG = {
    'dbname': "msa_data",
    'user': "postgres",
    'password': "anaiman",
    'host': "localhost",
    'port': 5432
}

# model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)
#
# # If using GPU, move model to device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)


def get_news_pages():
    for page_num in range(1, 6):
        url = f"https://www.mse.mk/mk/news/latest/{page_num}"

        news_links = []

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch the page: {url}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        panel_body = soup.find("div", class_="panel-body")
        if panel_body:
                links = panel_body.find_all("a", href=True)
                news_links.extend([link["href"] for link in links])

        if not news_links:
            print("No news links found.")
            return None
        return news_links



# def predict_sentiment(text):
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
#     with torch.no_grad():
#         logits = model(**inputs).logits.squeeze().cpu()
#     probabilities = torch.nn.functional.softmax(logits, dim=-1)
#     sentiment = torch.argmax(probabilities).item()  # This gives the sentiment label (0 = negative, 1 = neutral, 2 = positive)
#     return sentiment, probabilities[sentiment].item()  # Return the sentiment and its confidence score

def fetch_news(news_links, ticker, ticker_id, full_name):

    if not news_links:
        print("No news links available.")
        return
    sentiment_analyzer=pipeline("sentiment-analysis", model="agentlans/multilingual-e5-small-aligned-sentiment")
    company_news_found = False


    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            pos, neg, neutral = 0, 0, 0
            for index, link in enumerate(news_links):
                print(f"Index: {index}, Link: {link}")
                if not link.startswith("http"):
                    link = f"https://www.mse.mk{link}"

                response = requests.get(link)
                if response.status_code != 200:
                    print(f"Failed to fetch news article: {link}")
                    continue

                soup = BeautifulSoup(response.content, "html.parser")
                news_text = soup.find("div", class_="panel-body")
                if news_text:
                    news_text=news_text.get_text()
                else:
                    print("No news text found.")
                    continue

                if ticker.lower() in news_text.lower() or full_name.lower() in news_text.lower() :
                    company_news_found = True
                    sentiment_result = sentiment_analyzer(news_text[:512])[0]
                    print(f"Sentiment result for link {link}: {sentiment_result}")

                    sentiment_label = sentiment_result["label"]
                    # sentiment, score = predict_sentiment(news_text[:512])
                    # print(f"Sentiment result for link {link}: {sentiment}, Score: {score}")

                    # # Map the sentiment number to string
                    # if sentiment == 0:  # Negative
                    #     sentiment_label = "Negative"
                    # elif sentiment == 1:  # Neutral
                    #     sentiment_label = "Neutral"
                    # else:  # Positive
                    #     sentiment_label = "Positive"

                    if sentiment_label=='LABEL_0':
                            sentiment = "Negative"
                            neg+=1
                    elif sentiment_label=='LABEL_1':
                            sentiment = "Neutral"
                            neutral+=1
                    else:
                            sentiment = "Positive"
                            pos+=1

            if not company_news_found:
                print("No information.")
                return
            else:
                if pos/(pos+neg+neutral) >0.7:
                        prediction="Buy"
                elif neg/(pos+neg+neutral) >0.7:
                        prediction="Sell"
                else :
                        prediction="Hold"





                    # cursor.execute("""
                    #                         INSERT INTO latest_news (date, text, sentiment)
                    #                         VALUES (CURRENT_DATE, %s, %s)
                    #                         RETURNING id;
                    #                     """, (news_text, sentiment))


                cursor.execute("""
                                               INSERT INTO tickers_news (ticker_id, news_id,date,prediction)
                                               VALUES (%s, %s, CURRENT_DATE, %s);
                                           """, (ticker_id, index+100,prediction))

                conn.commit()









def fetch_tickers(conn):
    """Fetch all stock tickers and their full names."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, ticker, full_name FROM tickers;")
        return cursor.fetchall()

def get_latest_news_date(conn):
    """Fetch the latest news date from the database."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT MAX(date) FROM latest_news;")
        return cursor.fetchone()[0]




def fetch_and_process_news(conn):
    """Fetch and process the latest news articles."""
    tickers = fetch_tickers(conn)
    latest_date = get_latest_news_date(conn)
    news_links=get_news_pages()
    for ticker_id, ticker_name, full_name in tickers:
        fetch_news(news_links,  ticker_name, ticker_id, full_name)
        print(f"done for ticker {ticker_name}")


def init_db():
    """Initialize the database and create necessary tables."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            # cursor.execute("""
            #     CREATE TABLE IF NOT EXISTS latest_news (
            #         id SERIAL PRIMARY KEY,
            #         date DATE,
            #         text TEXT,
            #         sentiment VARCHAR(255)
            #     );
            # """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickers_news (
                    id SERIAL PRIMARY KEY,
                    ticker_id INT,
                    news_id INT,
                    date DATE,
                    prediction VARCHAR(255),
                    FOREIGN KEY (ticker_id) REFERENCES tickers(id)
                    --FOREIGN KEY (news_id) REFERENCES latest_news(id)
                );
            """)
            conn.commit()
            print('Database tables created if they didn’t exist.')

def init():
    """Main entry point to fetch and store news."""
    print("Fetching latest news...")

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            init_db()  
            fetch_and_process_news(conn)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    init()

