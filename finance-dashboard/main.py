import writer as wf
import writer.ai
import pandas as pd
from prompts import stock_prompts, income_prompts, earnings_prompt
from stock_data import download_data, download_sp500, stock_news, _one_day_data, income_statement, earnings_calls
from charts import update_scatter_chart
from dotenv import load_dotenv
import os

load_dotenv() 

writer.ai.init(os.getenv("WRITER_API_KEY"))

# Update all data
def updates(state):
    state["message"] = "% Refreshing stock data..."
    earnings_calls(state)
    download_sp500(state)
    stock_news(state)
    download_data(state)
    income_statement(state)
    update_scatter_chart(state)
    _one_day_data(state)
    _refresh_window(state)

# Refresh the window
def _refresh_window(state):
    state["show_income_metrics"]["visible"] = False
    state["show_bar_graph"]["visible"] = False
    state["show_analysis_text"]["visible"] = False
    state["show_analysis_text"]["language"] = False
    state["message"] = "Writer AI insights will be generated here"

# Summarize earnings call using Palmyra-Fin model
def summarize_earnings(state):
    _refresh_window(state)  
    state["message"] = f"% {state["symbol"]} earnings call will be summarized here"
    
    earnings_transcript = state["earnings_transcript"]
    prompt = earnings_prompt.format(earnings_transcript=earnings_transcript)
    submission = writer.ai.complete(prompt, config={"model": "palmyra-fin-32k", "temperature": 0.7, "max_tokens": 8192})
    state["message"] = f"+ {state["symbol"]} earnings call summary"
    state["analysis"] = submission.strip()
    state["show_analysis_text"]["visible"] = True
    
def prompt_parameters_words(state,payload):
    state["prompt_parameters_words"] = payload
    _refresh_window(state)
    
def prompt_parameters_lang(state,payload):
    state["prompt_parameters_lang"] = payload
    generate_stock_analysis(state)
    
def generate_stock_analysis(state):
    _refresh_window(state)  
    if(state["prompt_parameters_lang"] == ""):
        state["prompt_parameters_lang"] == "English"

    state["message"] = f"% {state["symbol"]} trends will be analyzed here in {state['prompt_parameters_lang']}"
    stock_name = state["symbol"]
    stock_data = state["main_df"][:365]
        
    rounded_value = round(state["prompt_parameters_words"], 0)
    language = state["prompt_parameters_lang"]
    # Convert the rounded value to an integer
    integer_value = int(rounded_value)

    prompt = stock_prompts.format(language=language, stock_name=stock_name,words=integer_value,stock_data=stock_data)
    submission = writer.ai.complete(prompt, config={"model": "palmyra-fin-32k", "temperature": 0.7, "max_tokens": 8192})
    state["analysis"] = submission.strip()
    state["message"] = f"+ {state["symbol"]} trends analyzed"
    state["show_analysis_text"]["visible"] = True
    state["show_analysis_text"]["language"] = True
        
    return submission


def generate_income_analysis(state):
    _refresh_window(state)
    state["message"] = f"% {state["symbol"]} income statement will be visualized here"
    stock_name = state["symbol"]
    stock_data = state["main_df"][:365]
    income_statement_data = state["income_statement_df"][:365]
    prompt = income_prompts.format(
        income_statement_data=income_statement_data,
        stock_data=stock_data,
        stock_name=stock_name,
    )
    submission = writer.ai.complete(prompt, config={"model": "palmyra-fin-32k", "temperature": 0.7, "max_tokens": 8192})
    state["analysis"] = submission.strip()
    state["message"] = f"+ {state["symbol"]} income statement visualized"
    state["show_income_metrics"]["visible"] = True
    state["show_analysis_text"]["visible"] = True
    state["show_bar_graph"]["visible"] = True
    return submission

def stock_tags(state, payload):
    state["symbol"] = payload
    updates(state)

def _get_main_df(filename):
    main_df = pd.read_csv(filename)
    return main_df 

initial_state = wf.init_state(
    {
        "last_24_hours_open": "168.76",
        "last_24_hours_high": "169.72",
        "last_24_hours_low": "167.50",
        "message": None,
        "main_df": _get_main_df("daily_IBM.csv"),
        "main_df_subset": _get_main_df("daily_IBM.csv"),
        "symbol": "AAPL",
        "articles": {
            "EU seeks views on Microsoft, OpenAI, Google and Samsung deals, EU's Vestager says": {
                "source": "Reuters",
                "published_at": "June 28, 2024 at 15:40",
                "url": "https://finance.yahoo.com/news/eu-seeks-views-microsoft-openai-144044802.html",
            },
            "Forget the S&P 500 -- Buy This Magnificent ETF Instead": {
                "source": "Motley Fool",
                "published_at": "June 28, 2024 at 15:00",
                "url": "https://finance.yahoo.com/m/662fcc10-7b6c-3bd1-8b7f-6cc25e8a1e61/forget-the-s%26p-500-buy.html",
            },
            "Microsoft Corporation (MSFT) is Attracting Investor Attention: Here is What You Should Know": {
                "source": "Zacks",
                "published_at": "June 28, 2024 at 14:00",
                "url": "https://finance.yahoo.com/news/microsoft-corporation-msft-attracting-investor-130015018.html",
            },
        },
        "show_analysis_text": {
            "visible": False,
            "language": False
        },
        "show_income_metrics": {
            "visible": False,
        },
        "tab_message": "- **Performance** tab highlights stock trends using an interactive graph where time filters can be selected.<br><li>**Stock data** tab shows the stock data from Yahoo Finance. <br><li>**Income data** tab shows the income statement from Yahoo Finance. <br><li>**View 10-K** tab shows the selected stock 10-K in a PDF viewer shown via an _API integration_.",
        "prompt_parameters_lang": "English",
        "prompt_parameters_words": 100,
        "message": "Writer AI insights will be generated here",
        "show_bar_graph": {"visible": False},
        "output_language": {
            "English": "English",
            "Arabic": "Arabic",
            "Bengali": "Bengali",
            "Bulgarian": "Bulgarian",
            "Chinese simplified": "Chinese simplified",
            "Chinese traditional": "Chinese traditional",
            "Croatian": "Croatian",
            "Czech": "Czech",
            "Danish": "Danish",
            "Dutch": "Dutch",
            "Finnish": "Finnish",
            "French": "French",
            "German": "German",
            "Greek": "Greek",
            "Hebrew": "Hebrew",
            "Hindi": "Hindi",
            "Hungarian": "Hungarian",
            "Indonesian": "Indonesian",
            "Italian": "Italian",
            "Japanese": "Japanese",
            "Korean": "Korean",
            "Lithuanian": "Lithuanian",
            "Polish": "Polish",
            "Portuguese": "Portuguese",
            "Romanian": "Romanian",
            "Russian": "Russian",
            "Spanish": "Spanish",
            "Swahili": "Swahili",
            "Swedish": "Swedish",
            "Thai": "Thai",
            "Turkish": "Turkish",
            "Ukrainian": "Ukrainian",
            "Vietnamese": "Vietnamese",
        },
    }
)

updates(initial_state)

initial_state.import_stylesheet("theme", "/static/custom.css?18")
