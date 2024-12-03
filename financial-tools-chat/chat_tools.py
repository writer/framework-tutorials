import json
import os
from io import StringIO

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from dotenv import load_dotenv
from plotly.subplots import make_subplots
from prompts import income_prompt, stock_prompt
from writer.ai import apps, complete

load_dotenv()


def _get_stock_analysis(symbol: str) -> str:
    config = {"model": "palmyra-fin-32k", "temperature": 0.7, "max_tokens": 8192}
    data = _get_stock_data(symbol)
    prompt = stock_prompt.format(name=symbol, data=data)
    stock_analysis = complete(prompt, config=config)
    return stock_analysis


def _get_stock_data(symbol: str) -> str:
    df = yf.download(symbol, period="5y", interval="5d")
    df = df.reset_index()
    df = df.sort_values(by="Date", ascending=True)
    df = df.round({"Open": 2, "High": 2, "Low": 2, "Close": 2, "Adj Close": 2})
    df["Date"] = pd.to_datetime(df["Date"])
    return df.to_csv(index=False)


def _get_income_analysis(symbol: str) -> str:
    config = {"model": "palmyra-fin-32k", "temperature": 0.7, "max_tokens": 8192}
    data = _get_income_data(symbol)
    prompt = income_prompt.format(name=symbol, data=data)
    income_analysis = complete(prompt, config=config)
    return income_analysis


def _get_income_data(symbol: str) -> str:
    quarterly_income_stmt = yf.Ticker(symbol).quarterly_income_stmt
    df = pd.DataFrame(quarterly_income_stmt)
    df.columns = pd.to_datetime(df.columns).strftime("%Y-%m-%d")
    return df.to_csv()


def _get_earnings_analysis(symbol: str) -> str:
    data = _get_earnings_data(symbol)
    earnings_analysis = apps.generate_content(
        application_id=os.getenv("EARNINGS_ANALYSIS_APP_ID", ""),
        input_dict={
            "name": symbol,
            "data": data,
        },
    )
    return earnings_analysis


def _get_earnings_data(symbol: str) -> str:
    with open("earnings-data.json", "r") as file:
        earnings_transcript = json.load(file)
    if earnings_transcript:
        for item in earnings_transcript:
            if item["symbol"] == symbol:
                return item["content"]
    else:
        return "No earnings transcript found."


def get_stock_chart(symbol: str) -> str:
    symbol_io = StringIO(_get_stock_data(symbol))
    sp500_io = StringIO(_get_stock_data("^GSPC"))

    symbol_df = pd.read_csv(symbol_io)
    sp500_df = pd.read_csv(sp500_io)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=symbol_df["Date"], y=symbol_df["Open"], name=symbol, mode="lines"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=sp500_df["Date"], y=sp500_df["Open"], name="S&P 500", mode="lines"
        ),
        secondary_y=True,
    )

    fig.update_yaxes(title_text=f"{symbol} Stock Price", secondary_y=False)
    fig.update_yaxes(title_text="S&P 500", secondary_y=True)

    fig.update_layout(
        height=450,
        title_text=f"{symbol} Stock vs the S&P 500",
        title_x=0.5,
        title_y=0.9,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig.to_json()


def get_income_chart(symbol: str) -> str:
    string_io = StringIO(_get_income_data(symbol))

    df = pd.read_csv(string_io, index_col=0)
    df_filtered = df.loc[["Total Revenue", "Net Income", "Operating Income"]]

    df_transposed = df_filtered.transpose().reset_index()
    df_transposed = df_transposed.melt(
        id_vars=["index"], var_name="Metric", value_name="Value"
    )

    fig = px.bar(
        df_transposed,
        x="index",
        y="Value",
        color="Metric",
        barmode="group",
        labels={"index": "", "Value": ""},
        title=f"Summary of Quarterly Income Statement for {symbol}",
    )

    fig.update_layout(
        height=400,
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
    )

    return fig.to_json()


stock_analysis_tool = {
    "type": "function",
    "name": "get_stock_analysis",
    "callable": _get_stock_analysis,
    "parameters": {
        "symbol": {
            "type": "string",
            "description": "Symbol to compose stock data analysis.",
        },
    },
}


income_analysis_tool = {
    "type": "function",
    "name": "get_income_analysis",
    "callable": _get_income_analysis,
    "parameters": {
        "symbol": {
            "type": "string",
            "description": "Symbol to compose income statement analysis.",
        },
    },
}


earnings_analysis_tool = {
    "type": "function",
    "name": "get_earnings_analysis",
    "callable": _get_earnings_analysis,
    "parameters": {
        "symbol": {
            "type": "string",
            "description": "Symbol to fetch earnings data and compose analysis.",
        },
    },
}


tools = [
    stock_analysis_tool,
    income_analysis_tool,
    earnings_analysis_tool,
]
