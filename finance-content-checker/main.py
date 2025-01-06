import asyncio

import writer as wf
from writerai import AsyncWriter
from dotenv import load_dotenv
import utils as ut
from prompts import _hyperbole_prompt, _outcome_language_prompt, _we_pronoun_prompt, input_text, initial_output

load_dotenv()

class Rule:
    def __init__(self, name, prompt_function, state):
        self.name = name
        self.prompt_function = prompt_function
        self.state = state

    async def fetch_data(self):
        formatted_content = self.state["content"].replace('\n\n', ' ')
        prompt = self.prompt_function(formatted_content)
        output = await AsyncWriter().completions.create(
            model="palmyra-x-004", prompt=prompt
        )
        data = ut.convert_string_to_dict_list(output.choices[0].text)
        if data:
            first_entry = data[0]
            ut.set_page_output(first_entry, self.state, self.name)
        self.state[self.name] = data
        self.state["pagination"][self.name]["data_size"] = len(data)

async def process_rules(state):
    """Process all rules and update the state accordingly."""

    # Define rules
    rules = [
        Rule("hyperbole", _hyperbole_prompt, state),
        Rule("outcome_language", _outcome_language_prompt, state),
        Rule("we_pronoun", _we_pronoun_prompt, state)
    ]

    tasks = []

    state["message"] = "Performing analysis..."

    # Fetch data for each rule
    for rule in rules:
        if(rule.name in state["suggestion_flags_selected"]):
            formatted_name = rule.name.replace("_", " ")
            tasks.append(rule.fetch_data())

    await asyncio.gather(*tasks)



# Event handlers
# Handler to add/remove tabs from being displayed when suggestion flags are selected. Called by change event on multiselect suggestion flags UI component.
def enable_suggestion_tabs(state,context):
    """
    Handler to add/remove tabs from being displayed when suggestion
    flags are selected. Called by change event on multiselect suggestion
     flags UI component.
    """
    all_options = list(flags.values())
    
    for selection in all_options:
        if selection in state["suggestion_flags_selected"]:
            state["tab_enabled"][selection] = True
        else: state["tab_enabled"][selection] = False


def set_page(state,payload):
    """This is a handler called by the pagination component when
    a page is clicked ("wf-change-page event). The payload returns
    the number of the current page "
    """
    index = payload - 1
    curr_tab = state["current_tab"]
    state["pagination"][curr_tab]["current_page"] = payload
    
    """The tab name of the current tab is used to determine which suggestion rule is in focus. 
    This means that the tab names need to line up with the rules. The logic here is that based 
    on the page clicked on in the active tab, we index that data dictionary and set the page 
    output accordingly, as well as highlight the text in the html output.
    """
    rule = state["current_tab"]
    data = state[rule]
    ut.set_page_output(data=data[index],state=state,rule=rule)
    ut.highlight_string(state,rule)
    return


def content_to_HMTL(state):
    """handler to set up the input text as html for the html element.
    Called whenever there is a change in the input text."""
    formatted_content = state["content"].replace('\n\n', '<br/><br/>')
    print(formatted_content)
    html = """ <p class="description">{content}</p>""".format(content=formatted_content)
    state["html_content"] = html
    return html

# Generate button click handler
async def handle_generate_button_click(state):
    # Disable button when clicked to prevent double clicking
    state["generate_btn_disabled"] = "yes"
    
    # Get function runs the llm call and returns a list of dictionaries of the results 
    # e.g. [{text:"",description: "" etc},{}]
    # This collection is stored in the state[rule] field and the 
    # number of pages is set based on the number of items in the collection.

    await process_rules(state)

    # Re-enable button once processing is completed.
    state["message"] = ""
    state["generate_btn_disabled"] = "no"
    ut.highlight_string(state,state["current_tab"])

def get_current_tab(state,context :dict):
    """This is a handler that is tied to the tab click event.
     Return the current tab: this uses an approach that will
    eventually be deprecated where we look at the context and
    grab the target from it which gives the component id of
    the UI component"""

    # mapping of component ids to tab names.
    tabs = {"y2co003xc2z7ckld": "outcome_language", "kdx0s5tf0t6t272y": "hyperbole", "1ntjnjorgokmrksh": "we_pronoun"}

    # The context["target"] gives the component id for the tab that has been clicked on.
    state["current_tab"] = tabs[context["target"]]
    curr_tab = state["current_tab"]

    # when a tab is clicked on, highlight the text for page 1 of that tab.
    ut.highlight_string(state,curr_tab)
    return tabs[context["target"]]


# State setup
content = input_text()
rule_keys = ["outcome_language", "we_pronoun", "hyperbole"]
initial_output_structure = {"text": "", "description": "", "guidelines": "", "suggestion": ""}
flags = {
        "Outcome language": "outcome_language",
        "Hyperbole": "hyperbole",
        "We pronoun": "we_pronoun"
    }

initial_state = wf.init_state({
    "my_app": {
        "title": "FINANCE COPY COMPLIANCE CHECK"
    },
    "message": "",
    "content": input_text(),
    "html_content":'<p class="description">{text}</p>'.format(text=input_text().replace("\n\n", "<br/><br/>")),
    "outcome_language": "",
    "we_pronoun":"",
    "hyperbole":"",
    "output": {
        "outcome_language": initial_output(),
        "we_pronoun": {"text": "","description":"","guidelines":"","suggestion":""},
        "hyperbole": {"text": "","description":"","guidelines":"","suggestion":""}
    },
    "suggestion_flags": {
                        "outcome_language": "Outcome language",
                        "hyperbole": "Hyperbole",
                        "we_pronoun": "We pronoun"
                        },
    "suggestion_flags_selected": ["outcome_language","hyperbole","we_pronoun"],
    "tab_enabled": {
        "outcome_language": True,
        "we_pronoun": True,
        "hyperbole": True
    },
    "pagination":{
        "outcome_language":{
            "data_size": 1,
            "current_page": 1

        },
        "hyperbole":{
            "data_size": 1,
            "current_page": 1

        },
        "we_pronoun":{
            "data_size": 1,
            "current_page": 1

        }
    },
    "current_tab": "outcome_language",
    "generate_btn_disabled": "no",
    "img_path": "static/Writer_Logo_black.svg",

})

initial_state.import_stylesheet(".description", "/static/custom.css")
