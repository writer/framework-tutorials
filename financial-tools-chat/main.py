import json
import os

import httpx
import plotly.express as px
import writer
from chat_tools import get_income_chart, get_stock_chart, tools
from dotenv import load_dotenv
from writer.ai import Conversation

load_dotenv()

writer.ai.init(os.getenv("WRITER_API_KEY", ""))


def message_handler(payload, state):
    try:
        state.call_frontend_function("scripts", "enableDisableTextarea", ["true"])
        state["conversation"] += payload

        response = state["conversation"].stream_complete(tools=tools)

        for chunk in response:
            state["conversation"] += chunk

        for tool_call in _get_tool_call_results(state).values():
            _visualize_response(state, tool_call)

        state.call_frontend_function("scripts", "enableDisableTextarea", ["false"])
    except (KeyError, ValueError, httpx.RemoteProtocolError) as e:
        state["conversation"] += {
            "role": "assistant",
            "content": "Sorry, we faced unexpected error. Please try again!",
        }
        state.call_frontend_function("scripts", "enableDisableTextarea", ["false"])
        raise e


def _get_tool_call_results(state):
    tool_calls = {}
    for message in reversed(state["conversation"].messages):
        try:
            if message["role"] == "tool":
                tool_calls.update({message["name"]: message})
            elif message["role"] == "assistant" and message["tool_calls"]:
                for tool_call in message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = tool_call["function"]["arguments"]
                    tool_calls[tool_name].update({"arguments": json.loads(tool_args)})
            elif message["role"] == "user":
                break
        except KeyError as e:
            raise KeyError("Key error during fetching tool calls") from e
    return tool_calls


def _visualize_response(state, tool_call):
    _update_text(state, tool_call["name"].split("_")[1], tool_call["content"])
    _update_graphic(
        state, tool_call["name"].split("_")[1], tool_call["arguments"]["symbol"]
    )
    state.call_frontend_function(
        "scripts", "focusOnTab", [tool_call["name"].split("_")[1]]
    )
    state["visual_block_visible"] = True


def _update_text(state, property_name, text):
    state[property_name + "_analysis"] = text


def _update_graphic(state, property_name, symbol_name):
    graphic = ""
    if property_name == "stock":
        graphic = get_stock_chart(symbol_name)
    elif property_name == "income":
        graphic = get_income_chart(symbol_name)
    state[property_name + "_chart"] = graphic


def _get_chart_placeholder():
    df = px.data.stocks()
    df.columns.values[1] = "TEST"
    fig = px.line(df, x="date", y="TEST")

    fig.update_layout(
        height=400,
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


def clear_visualization(state):
    tab_names = ["stock", "income", "earnings"]

    for tab_name in tab_names:
        state[tab_name + "_analysis"] = "Analysis will appear here."
        state[tab_name + "_chart"] = _get_chart_placeholder()

    state["visual_block_visible"] = False


def close_visualization(state):
    state["visual_block_visible"] = False


def open_visualization(state):
    state["visual_block_visible"] = True


initial_state = writer.init_state(
    {
        "conversation": Conversation(
            [
                {"role": "assistant", "content": "Hi there. I can analyze stock price data, income statements, and earnings reports. How can I help?"},
            ],
        ),
        "visual_block_visible": False,
        "stock_analysis": "Analysis will appear here.",
        "stock_chart": _get_chart_placeholder(),
        "income_analysis": "Analysis will appear here.",
        "income_chart": _get_chart_placeholder(),
        "earnings_analysis": "Analysis will appear here.",
    }
)

initial_state.import_stylesheet("style", "/static/custom.css")
initial_state.import_frontend_module("scripts", "/static/custom.js")
