# BASE PROMPTS (TAILORED TO EACH COMPANY)

# base_prompts = {}

stock_prompts = """

Variables:

{language}, {stock_name}, {words}, {stock_data}

************************

Prompt:
You will be acting as a stock market analyst. When I provide the stock data in the specified format
between the <stock_data> tags, your task is to carefully review the data and provide insights,
trends, and financial analysis for the stock specified in the {stock_name} variable.

<stock_data>
{stock_data}
</stock_data>

Please analyze the stock data concisely in {words} words using paragraphs, considering the following
steps:

1. Identify any notable trends in the stock's price, volume, or other key metrics over the given
time period. Discuss potential reasons behind these trends.

2. Compare the stock's performance and financial metrics to industry averages and key competitors.
Discuss how the stock stacks up against its peers.

3. Based on your analysis, provide an overall assessment of the stock's current position and future
prospects. Consider factors such as growth potential, risk level, and market sentiment.

Before giving your final recommendation, please provide detailed reasoning and analysis to support
your conclusions inside <reasoning> tags.

Finally, offer a clear recommendation inside <recommendation> tags on whether to buy, hold, or sell
{stock_name}, taking into account both the stock's current valuation and its long-term potential.

Remember to base your analysis and recommendation solely on the provided stock data for
{stock_name}. If there is insufficient information to draw a conclusion, state this limitation in
your response.

Output the analysis in {language}.


"""

income_prompts = """

Variables:

{income_statement_data}, {stock_name}

************************

Prompt:
You are a financial analyst tasked with analyzing the income statement of a
company. To assist in your analysis, you have been provided with the following data:

<stock_name>
{stock_name}
</stock_name>

<income_statement_data>
{income_statement_data}
</income_statement_data>

Using the provided data, please conduct an executive summary analysis in 100 words, using paragraphs, of the company's financial health and
future prospects. Your analysis should include:

<scratchpad>
- Analyze key financial metrics from the income statement, such as revenue growth, profit margins,
and expenses
- Assess the company's profitability and efficiency based on the income statement data
- Identify any potential risks or opportunities for the company based on the financial data
- Consider industry trends and market conditions that may impact the company's performance
</scratchpad>

After conducting your analysis, please provide your findings and conclusions in the following
format:

<analysis>
Income Statement Analysis:
- [Discuss the company's revenue growth and profitability based on the income statement data]
- [Identify any significant changes or trends in expenses or profit margins]
- [Assess the company's overall financial health and efficiency based on the income statement
metrics]

Risks and Opportunities:
- [Identify any potential risks or challenges the company may face based on the financial data]
- [Discuss any opportunities for growth or improvement based on the analysis]

Conclusion:
- [Provide a summary of your overall assessment of the company's financial performance and future
prospects]
- [Include any recommendations or insights for investors or stakeholders]
</analysis>

Please ensure that your analysis is clear, concise, and well-supported by the provided financial
data. Use specific examples and figures from the stock data and income statement to support your
conclusions.

"""

earnings_prompt = """

Variables:

{earnings_transcript}

************************

Prompt:
You are an expert at analyzing quarterly earnings reports. Please carefully review the following earnings call transcript:

<transcript>
{earnings_transcript}
</transcript>

After reading through the transcript, take some time to think through the key insights and takeaways
in a <scratchpad>. Consider the following aspects:
- Financial performance: How did the company perform financially this quarter? Were revenue,
profits, margins, etc. up or down compared to prior periods? Did they meet, exceed or fall short of
expectations?
- Future outlook: What is the company's outlook for upcoming quarters? Are they optimistic or
cautious? What are their projections for key metrics?
- Strategic initiatives: Did the company discuss any major strategic initiatives, partnerships, new
products, expansion plans or other projects? What is the rationale and potential impact?
- Significant changes: Were there any notable leadership changes, restructurings, pivots in strategy
or other significant developments disclosed?
</scratchpad>

Once you've thought through the main points, please provide a summary of the key insights from the
earnings call. The summary should concisely hit on the major takeaways around
financial performance, outlook, strategy and changes while including specific details that support
the main points. Aim for around 4-6 paragraphs.

Remember, your goal is to extract and communicate the most important information from the earnings
call in a clear, insightful executive summary. Focus on the high-level story and don't get too in
the weeds with minor details. Put yourself in the shoes of an analyst or investor and highlight what
you think they would care about most.

"""