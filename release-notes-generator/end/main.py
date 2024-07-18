import writer as wf
import pandas as pd
import writer.ai
from  prompts import get_release_notes_summary_prompt, get_release_notes_desc_prompt, get_category_prompt
from html_template import format_output

#Functions to call the Completions end point for category, summary, and description. The prompts used are imported from the prompts file
def _get_category(desc, label):
    prompt = get_category_prompt(desc, label)
    label = writer.ai.complete(prompt)
    return label

def _get_release_notes_summary(label, desc):
    prompt = get_release_notes_summary_prompt(label, desc)
    formatted_desc =  writer.ai.complete( prompt)
    return formatted_desc

def _get_release_notes_desc(label,desc):
    prompt = get_release_notes_desc_prompt(label,desc)
    formatted_desc =  writer.ai.complete(prompt)
    return formatted_desc

# Handles when file is uploaded
def onchangefile_handler(state, payload):
    uploaded_file = payload[0]

    # Store file name and path in case we need to use it later
    name = uploaded_file.get("name")
    state["File"]["Name"] = name
    state["step1"]["processing-message"] = f'+File {name} uploaded successfully.'
    state["File"]["file_path"] = f"data/{name}"
    file_data = uploaded_file.get("data")
    # Save the file to the data folder instead of reading it in memory
    with open(f"data/{name}", "wb") as file_handle:
        file_handle.write(file_data)
        
    # Save raw csv file and mark the upload step as complete
    data = pd.read_csv(state["File"]["file_path"])
    df = pd.DataFrame(data)
    state["step1"]["raw_csv"] = df
    state["step1"]["generate-button-state"] = "no"

# Handler for generate button
def handle_generate_button_click(state):
    state["step1"]["generate-button-state"] = "yes"
    # Set Processing Message state to visible
    state["step1"]["processing-message-isVisible"] = True
    state["step1"]["processing-message"] = "%Hang tight, preparing to process your file"

    # Read in csv from state and iterate through each row to apply the completions endpoint functions
    notes_counter = 0
    df = _raw_csv_to_df(state)
    csv_row_count = df.shape[0]
    for index, row in df.iterrows():
        df.at[index,"Primary-Category"] = _get_category(label=row["Labels"], desc=row["Description"])
        df.at[index,"Release-Notes-Summary"] = _get_release_notes_summary(label=row["Labels"], desc=row["Description"])
        df.at[index,"Release-Notes-Description"] = _get_release_notes_desc(label=row["Labels"], desc=row["Description"])
        notes_counter += 1 
        state["step1"]["processing-message"] = f'%Processing {notes_counter} of {csv_row_count} Release Notes'
    df_temp = df[["Primary-Category","Release-Notes-Summary","Release-Notes-Description"]]
    df_sorted = df_temp.sort_values(by='Primary-Category')

    # Update State to populate Release Notes table in Release Notes tab
    state["step2"]["release-notes"] = df_sorted

    # Complete step 1 and automatically direct the user to step 2
    state["step1"]["completed"] = "yes"
    state["step1"]["processing-message"] = ""

    # Create the HTML element for the Formatted Release Notes Tab
    html = _create_df_for_category(df_sorted,state)
    _write_html_to_file(html)
    state["step2"]["formatted-release-notes"] = html
    state["metrics"]["Total"] = df_sorted.shape[0]

    state["step1"]["generate-button-state"] = "no"

# Back button handler
def handle_back_button_click(state):
    state["step1"]["completed"] = "no"

# Function to write the HTML to a file
def _write_html_to_file(html):
    with open("data/output-html.html", "w") as file_handle:
            file_handle.write(html)

# Handler for HTML file download button
def handle_file_download(state):
    html_data = wf.pack_file("data/output-html.html","text/html")
    file_name = "output-html.html"
    state.file_download(html_data,file_name)

# Get a list of all unique categories from the dataframe and 
# generate the HTML for each of the summaries and descriptions
# This function returns a single string with all the elements for all categories.
def _create_df_for_category(df,state):
    unique_categories = df['Primary-Category']
    formatted_output_list = list()
    for category in set(unique_categories):
        # Filter by individual category. This will produce a df for each single category.
        df_category = df[df['Primary-Category']==category]
        categories = {" New Feature": "new_features", " Caveat": "caveats", " Fixed Issue": "fixed_issues" }
        curr_category = categories[category]
        state["metrics"][curr_category]= df_category.shape[0]
        formatted_output = format_output(category,df_category)
        formatted_output_list.append(formatted_output)
    return "".join(formatted_output_list)


# Creating initial placeholder DataFrame
placeholder_data = {
    'Description': ['Description 1', 'Description 2', 'Description 3'],
    'Label': ['Label 1', 'Label 2', 'Label 3']
}
initial_df = pd.DataFrame(placeholder_data)

# Function to read in the raw CSV file and return a DataFrame
def _raw_csv_to_df(state):
    data = pd.read_csv(state["File"]["file_path"])
    df = pd.DataFrame(data)
    return df

# Initialise the state
initial_state = wf.init_state({
    "my_app": {
        "title": "Release Notes Generator"
    },
    "logo_image_path" : 'static/Writer_Logo_black.svg',
    "File": {
        "Name" : "",
        "file_path" : "" 
    },
    "metrics":{
        "new_features": 0,
        "caveats": 0,
        "fixed_issues" : 0,
        "Total": 0
    },
    "step1":{
        "raw_csv": initial_df,
        "completed": "no",
        "generate-button-state": "yes",
        "processing-message" : None,
        "processing-message-isVisible": False,
        "styled-table": "<h3>csv table</h3>" 
    },
    "step2":{
            "release-notes": None,
            "completed": "no",
            "formatted-release-notes":"notes should go here"},    
})

# Import the custom CSS file
initial_state.import_stylesheet(".description, .summary, .category, .list", "/static/custom.css")

