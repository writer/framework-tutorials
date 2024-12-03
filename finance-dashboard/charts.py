import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def handle_click(state, context: dict, ui):
    # Resetting the classes for active button
    if state["active_button"]:
        active_button = ui.find(state["active_button"])
        active_button.content["cssClasses"] = ""

    event_target = context["target"]
    button = ui.find(event_target)

    # Storing the clicked button ID in state
    state["active_button"] = event_target

    button_text = button.content["text"]
    _handle_time_period(state, button_text)
    button.content["cssClasses"] = "button-click"
    
    button_max = ui.find("e13teponreio9yyz")
    button_max.content["cssClasses"] = ""
    
    ui.component_tree.updated = True

def _handle_time_period(state, period):
    state["main_df_subset"] = state["main_df"]
    if period == "5D":
        state["main_df_subset"] = state["main_df_subset"][:5]
    elif period == "1M":
        state["main_df_subset"] = state["main_df_subset"][:30]
    elif period == "3M":
        state["main_df_subset"] = state["main_df_subset"][:90]
    elif period == "1Y":
        state["main_df_subset"] = state["main_df_subset"][:360]
    elif period == "5Y":
        state["main_df_subset"] = state["main_df_subset"][:1800]
    elif period == "Max":
        # No need to slice, already has the full data
        pass
    update_scatter_chart(state)

def update_scatter_chart(state):
    fig = px.line(state["main_df_subset"], x="Date", y="Open", height=400)
    
    df1 = state["main_df_subset"]
    df2 = state["another_df"]
    df2 = df2.head(len(df1))

    # Add a new column to each dataframe to identify the source
    df1["Source"] = "Main_DF"
    df2["Source"] = "Another_DF"

    # Concatenate the dataframes
    combined_df = pd.concat([df1, df2])
    state["main_df_subset"] = combined_df

    # Plot the lines
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for the primary y-axis (Main_DF)
    fig.add_trace(
        go.Scatter(x=df1["Date"], y=df1["Open"], name=state["symbol"], mode='lines'),
        secondary_y=False,
    )

    # Add traces for the secondary y-axis (Another_DF)
    fig.add_trace(
        go.Scatter(x=df2["Date"], y=df2["Open"], name="S&P 500", mode='lines'),
        secondary_y=True,
    )

    # Set axis titles
    fig.update_yaxes(title_text=f"{state['symbol']} Stock Price", secondary_y=False)
    fig.update_yaxes(title_text="S&P 500", secondary_y=True)

    # Update layout
    fig.update_layout(height=550, title_text=f"{state['symbol']} Stock vs the S&P 500", title_x = 0.5, title_y = 0.9, legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.2,  # Adjust this value as needed
            xanchor='center',
            x=0.5
        ))

    state["scatter_chart"] = fig
    
def update_bar_graph(state):
    fig = px.line(state["main_df_subset"], x="Date", y="Open", height=400)

    df = state["income_statement_df"]
    selected_metrics = ["Total Revenue", "Net Income", "Operating Income"]
    df_filtered = df.loc[selected_metrics]

    # Transpose the DataFrame for easier plotting
    df_transposed = df_filtered.transpose().reset_index()
    df_transposed = df_transposed.melt(
        id_vars=["index"], var_name="Metric", value_name="Value"
    )

    # Create the bar graph using Plotly Express
    fig = px.bar(
        df_transposed,
        x="index",
        y="Value",
        color="Metric",
        barmode="group",
        labels={"index": "", "Value": ""},
        title="Summary of Quarterly Income Statement",
    )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
    )

    state["bar_graph"] = fig