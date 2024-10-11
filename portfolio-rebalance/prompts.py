def generate_positive_stock_selection_prompt(past_quarter_results):
    prompt = f"""
    For the ClearBridge Large Cap Growth Fund, when compared to the benchmark of Russell 1000 Growth, which stock sectors had the highest Selection + Interaction? Do not provide more than two sectors.

    Please only list the names of the sectors. Do not list more than two and do not put them in an ordered list.

    Use this document to help answer your question: {past_quarter_results}
    """
    return prompt


def generate_positive_sector_weighting_prompt(past_quarter_results):
    prompt = f"""
    For the ClearBridge Large Cap Growth Fund, which two sectors had the highest Total Effect?

    Please only list the names of the sectors. Do not provide more than two.

    Use this document to help answer your question: {past_quarter_results}
    """
    return prompt


def generate_positive_concatenation_prompt(past_quarter_results):
    prompt = f"""
    Stock sectors: {past_quarter_results}

    For the two stock sectors mentioned above, format a response as: "stock selection in the X sector and Y sector contributed to the performance", where X is the first sector mentioned above and Y is the second sector mentioned above. Do not capitalize the first word of the sentence.
    """
    return prompt


def generate_negative_stock_selection_prompt(past_quarter_results):
    prompt = f"""
    For the ClearBridge Large Cap Growth Fund, when compared to the benchmark of Russell 1000 Growth, which stock sectors had the lowest Selection + Interaction? Do not provide more than two sectors.

    Please only list the names of the sectors. Do not list more than two.

    Use this document to help answer your question: {past_quarter_results}
    """
    return prompt


def generate_negative_concatenation_prompt(negative_stock_selection):
    prompt = f"""
    Stock sectors: {negative_stock_selection}

    For the two stock sectors mentioned above, format a response as: "stock selection in the X sector and Y sector detracted from performance", where X is the first sector mentioned above and Y is the second sector mentioned above. Do not capitalize the first word of the sentence.
    """
    return prompt


def generate_positive_impacts_prompt(past_quarter_results):
    prompt = f"""
    Give an answer to the question: What individual stocks contributed the most to positive returns? Your answer should be in the format: "In terms of individual stocks, the greatest contributors to returns included the Portfolios' positions in [Company A], [Company B], [Company C], [Company D], and [Company E]."

    Here's the data sheet that can be used to answer that question: {past_quarter_results}

    Three things to keep in mind:

    1. The data sheet has the full names of companies, but you only need to report on its short name. For example, instead of reporting as London Stock Exchange Group plc, you should just say London Stock Exchange Group.
    2. You should only list a maximum of five individual stocks.
    3. The examples above should strictly be used for format advice. Only use stocks mentioned in the data sheet in your response.

    Please provide your answer in this format.
    """
    return prompt


def generate_negative_impacts_prompt(past_quarter_results):
    prompt = f"""
    Give an answer to the question: What individual stocks detracted the most from returns? Your answer should be in the format: "In terms of individual stocks, the greatest detractors from returns included the Portfolios' positions in [Company A], [Company B], [Company C], [Company D], and [Company E]."

    Here's the data sheet that can be used to answer that question: {past_quarter_results}

    Three things to keep in mind:

    1. The data sheet has the full names of companies, but you only need to report its short name. For example, instead of reporting as London Stock Exchange Group plc, you should just say London Stock Exchange Group.
    2. You should only list a maximum of five individual stocks.
    3. The examples above should strictly be used for format advice. Only use stocks mentioned in the data sheet in your response.

    Please provide your answer in this format.
    """
    return prompt


def generate_rebalance_recommendation_prompt(
    positive_stock_selection,
    positive_sector_weighting,
    positive_concatenation,
    positive_impacts,
    negative_stock_selection,
    negative_concatenation,
    negative_impacts,
):

    prompt = f"""
    Based on the past results from last quarter, please write a step-by-step analysis of how to rebalance the portfolio.

    Here are the results:

    <i>Positive Stock Selection:</i>
    For the last quarter relative to the benchmark, the highest positive stock selection was in the following sectors: {positive_stock_selection}.

    <i>Positive Sector Weighting:</i>
    The sectors with the highest total effect were: {positive_sector_weighting}.

    <i>Positive Impacts:</i>
    Stock selection in {positive_concatenation} contributed to the performance.
    In terms of individual stocks, the greatest contributors to returns included: {positive_impacts}.

    <i>Negative Stock Selection:</i>
    The sectors with the lowest stock selection and interaction were: {negative_stock_selection}.

    <i>Negative Impacts:</i>
    Stock selection in {negative_concatenation} detracted from the performance.
    In terms of individual stocks, the greatest detractors from returns included: {negative_impacts}.

    Based on this analysis, please provide your positive impacts, negative impacts and recommendations for rebalancing the portfolio. In your recommendation, be sure to name specific stocks as well as industries.Do not include any extraneous information around general portfolio rebalancing process or additional general resources. 
    """

    return prompt
