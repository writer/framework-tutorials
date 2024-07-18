import writer as wf
import pandas as pd
import writer.ai
from  prompts import get_release_notes_summary_prompt, get_release_notes_desc_prompt, get_category_prompt
from html_template import format_output

# Welcome to Writer Framework! 
# More documentation is available at https://developer.writer.com/framework


# Initialise the state
wf.init_state({
    "my_app": {
        "title": "RELEASE NOTES GENERATOR"
    },
    "logo_image_path" : 'static/Writer_Logo_black.svg'
})