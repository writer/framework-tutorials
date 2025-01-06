import json
import re
from prompts import _we_pronoun_prompt, _outcome_language_prompt, _hyperbole_prompt

# Map data dictionary into output boxes 
def set_page_output(data,state,rule):
    state["output"][rule]["text"]= data["text"]
    state["output"][rule]["description"] = data["description"]
    state["output"][rule]["guideline"] = data["guideline"]
    state["output"][rule]["suggestion"] = data["suggestion"]


def highlight_string(state,rule):
    state["html_content"] = state["content"].replace('\n\n', '<br/><br/>')
    html_paragraph = state["html_content"]
    search_string =  state["output"][rule]["text"]
    highlighted_html = highlight_string_in_html(html_paragraph, search_string)
    state["html_content"] = highlighted_html


def convert_string_to_dict_list(input_string):
    try:
        # # Properly format the string to make it a valid JSON array
        input_string = input_string.replace("```json", "").replace("```", "")
        # Convert the formatted string into a list of dictionaries
        data_list = json.loads(input_string)
        return data_list
    except json.JSONDecodeError as e:
        print(e)
        return []


def highlight_string_in_html(html_paragraph, search_string):
    # Escape special characters in the search string to safely use it in a regular expression
    escaped_search_string = re.escape(search_string)
    
    # Define the replacement pattern, wrapping the search string in a span with a light orange background
    replacement_pattern = f'<span style="background-color: #FFA07A;">{search_string}</span>'
    
    # Use re.sub() to replace occurrences of the search string with the replacement pattern
    highlighted_html = re.sub(escaped_search_string, replacement_pattern, html_paragraph, flags=re.IGNORECASE)
    
    return highlighted_html
