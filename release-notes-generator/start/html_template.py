import re

# Pass in filtered df for a category eg. New Feature
# This function loops through each row in the df and creates an element for each summary/description pair.
def format_output(category,df ):
    all_elements_list = list()
    for _,row in df.iterrows():
        all_elements_list.append(formatted_single_element(summary=row["Release-Notes-Summary"],description=row["Release-Notes-Description"]))
    all_elements = "\n".join(all_elements_list)
    

    html = f"""
<details>
    <summary class="category">{category}</summary>
    {all_elements}
</details>
"""
    return html

def formatted_single_element(summary: str, description: str ) -> str:
    formatted_description = format_to_html(description)

    html = f"""
<details>
        <summary class="summary"> {summary}</summary>
        <p class="description">{formatted_description}</p>
    </details>
"""
    return html

def format_to_html(text):
    items = re.split(r'(?<=\.)\s*-\s*', text.strip('- '))
    list_items = [f"<li>{item.strip()}</li>" for item in items if item.strip()]
    formatted_html = "\n".join(list_items)
    
    return f'<ul class="list">\n{formatted_html}\n</ul>'