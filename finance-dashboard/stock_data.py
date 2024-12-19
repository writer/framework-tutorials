import json
from datetime import datetime

import pandas as pd
import yfinance as yf
from charts import update_bar_graph
from dotenv import load_dotenv

load_dotenv()


# Download stock data and format into a DataFrame
def download_data(state):
    df = yf.download(state["symbol"], period="max", interval="1d")
    df = df.reset_index()
    if type(df.columns) is pd.MultiIndex:
        df.columns = df.columns.droplevel(1)
    df = df.sort_values(by="Date", ascending=False)
    df = df.round({"Open": 2, "High": 2, "Low": 2, "Close": 2, "Adj Close": 2})
    df["Date"] = pd.to_datetime(df["Date"])
    state["main_df_subset"] = df
    state["main_df"] = state["main_df_subset"]


# Download S&P 500 data and format into a DataFrame
def download_sp500(state):
    df = yf.download(tickers="^GSPC", period="max", interval="1d")
    df = df.reset_index()
    if type(df.columns) is pd.MultiIndex:
        df.columns = df.columns.droplevel(1)
    df = df.sort_values(by="Date", ascending=False)
    df = df.round({"Open": 2, "High": 2, "Low": 2, "Close": 2, "Adj Close": 2})
    df["Date"] = pd.to_datetime(df["Date"])
    state["another_df"] = df


# Retrieve latest stock news
def stock_news(state):
    msft = yf.Ticker(state["symbol"])
    articles = {}
    data = msft.news
    latest_articles = sorted(
        data, key=lambda x: x["providerPublishTime"], reverse=True
    )[:4]

    for item in latest_articles:
        provider_publish_time = item.get("providerPublishTime", "")
        if provider_publish_time:
            # Convert the timestamp to a readable date
            formatted_date = datetime.fromtimestamp(provider_publish_time)
            readable_date = formatted_date.strftime("%B %d, %Y at %H:%M")
        else:
            readable_date = "Date not available"

        title = item.get("title", "No Title")
        articles[title] = {
            "source": item.get("publisher", ""),
            "published_at": readable_date,
            "url": item.get("link", ""),
        }
    state["articles"] = articles


# Retrieve income statement data
def income_statement(state):
    quarterly_income_stmt = yf.Ticker(state["symbol"]).quarterly_income_stmt
    df = pd.DataFrame(quarterly_income_stmt)
    df.columns = pd.to_datetime(df.columns).strftime("%Y-%m-%d")
    state["income_statement_df"] = df
    update_bar_graph(state)
    show_fin_metrics(state)


# Show financial metrics
def show_fin_metrics(state):
    stock = yf.Ticker(state["symbol"])
    operating_margins = stock.info["operatingMargins"]
    gross_margin = stock.info["grossMargins"]
    ebitda_margin = stock.info["ebitdaMargins"]

    state["operating_margin"] = f"{operating_margins * 100:.2f}%"
    state["gross_margin"] = f"{gross_margin * 100:.2f}%"
    state["ebitda_margin"] = f"{ebitda_margin * 100:.2f}%"


def _one_day_data(state):
    state["last_24_hours_open"] = round(state["main_df"]["Open"].iloc[0], 2)
    state["last_24_hours_high"] = round(state["main_df"]["High"].iloc[0], 2)
    state["last_24_hours_low"] = round(state["main_df"]["Low"].iloc[0], 2)


# Retrieve earnings call transcript from JSON file
# You could replace this with a call to an API like Financial Modeling Prep
def earnings_calls(state):
    ticker = state["symbol"]
    with open("earnings-data.json", "r") as file:
        earnings_transcript = json.load(file)
    if earnings_transcript:
        for item in earnings_transcript:
            if item["symbol"] == ticker:
                state["earnings_transcript"] = item["content"]
    else:
        print("No earnings transcript found.")
