import asyncio
import os
import shutil

import pandas as pd
import writer as wf
import writer.ai
from dotenv import load_dotenv

from prompts import (generate_negative_concatenation_prompt,
                     generate_negative_impacts_prompt,
                     generate_negative_stock_selection_prompt,
                     generate_positive_concatenation_prompt,
                     generate_positive_impacts_prompt,
                     generate_positive_sector_weighting_prompt,
                     generate_positive_stock_selection_prompt,
                     generate_rebalance_recommendation_prompt)

load_dotenv()

pd.options.mode.chained_assignment = None


def handle_file_on_change(state, payload):
    clear_results(state)
    _save_file(state, payload[0])

    file_extension = state["file"]["name"].split(".")[-1].lower()

    match file_extension:
        case "xlsx" | "xls":
            df = _read_excel(state)
        case "pdf":
            text_data = _read_pdf(state)
        case _:
            state["processing-message"] = "Unsupported file type"
            return

    state["processing-message"] = "Analyzing positive and negative impacts..."
    prompt = analyze_data(
        df if file_extension in ["xlsx", "xls"] else text_data
    )

    state["processing-message"] = "Generating rebalancing recommendation..."
    state["analysis-result"] = ""
    
    # Using Palmyra-Fin model
    # for chunk in writer.ai.stream_complete(prompt, {"model": "palmyra-fin-32k", "max_tokens": 2048, "temperature": 0.7}):
    #     state["analysis-result"] += chunk

    # Using Palmyra X 004 model
    conversation = writer.ai.Conversation([{"role": "user", "content": prompt}], {"model": "palmyra-x-004", "max_tokens": 2048, "temperature": 0.7})
    for chunk in conversation.stream_complete():
        if chunk.get("content"):
            state["analysis-result"] += chunk.get("content")
    
    state["visual_block_visible"] = True
    state["processing-message"] = ""


def clear_results(state):
    state["analysis-result"] = "Your analysis will appear here."
    _delete_all_files(state)
    state["visual_block_visible"] = False


def _save_file(state, file):
    name = file.get("name")
    state["file"]["name"] = name
    state["file"]["file_path"] = f"data/{name}"
    state["processing-message"] = f"File {name} saved."
    file_data = file.get("data")
    with open(f"data/{name}", "wb") as file_handle:
        file_handle.write(file_data)


def _delete_all_files(state):
    directory = "data"

    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)

    state["file"]["name"] = ""
    state["file"]["file_path"] = ""
    state["processing-message"] = "All files have been deleted."


def _read_excel(state):
    data = pd.read_excel(state["file"]["file_path"])
    df = pd.DataFrame(data)
    return df


def _read_pdf(state):
    from PyPDF2 import PdfReader

    reader = PdfReader(state["file"]["file_path"])
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Create async tasks for each prompt and then generate the final prompt
async def gather_results_and_generate_rebalance_prompt(data: str):
    async def complete_async(prompt):
        return await asyncio.to_thread(writer.ai.complete, prompt, {"model": "palmyra-fin-32k", "max_tokens": 3048, "temperature": 0.7})

    positive_stock_selection_task = complete_async(
        generate_positive_stock_selection_prompt(data)
    )

    positive_sector_weighting_task = complete_async(
        generate_positive_sector_weighting_prompt(data)
    )

    positive_concatenation_task = complete_async(
        generate_positive_concatenation_prompt(data)
    )

    positive_impacts_task = complete_async(generate_positive_impacts_prompt(data))

    negative_stock_selection_task = complete_async(
        generate_negative_stock_selection_prompt(data)
    )

    negative_concatenation_task = complete_async(
        generate_negative_concatenation_prompt(data)
    )

    negative_impacts_task = complete_async(generate_negative_impacts_prompt(data))

    (
        positive_stock_selection,
        positive_sector_weighting,
        positive_concatenation,
        positive_impacts,
        negative_stock_selection,
        negative_concatenation,
        negative_impacts,
    ) = await asyncio.gather(
        positive_stock_selection_task,
        positive_sector_weighting_task,
        positive_concatenation_task,
        positive_impacts_task,
        negative_stock_selection_task,
        negative_concatenation_task,
        negative_impacts_task,
    )

    final_prompt = generate_rebalance_recommendation_prompt(
            positive_stock_selection,
            positive_sector_weighting,
            positive_concatenation,
            positive_impacts,
            negative_stock_selection,
            negative_concatenation,
            negative_impacts,
        )

    return final_prompt


def analyze_data(data):
    if isinstance(data, pd.DataFrame):
        data_str = data.to_string()
    else:
        data_str = data
    
    return asyncio.run(
        gather_results_and_generate_rebalance_prompt(data_str)
    )


def handle_file_download(state):
    analysis_result = state["analysis-result"]

    if analysis_result:
        with open("data/analysis_result.txt", "w") as file_handle:
            file_handle.write(analysis_result)

        file_data = wf.pack_file("data/analysis_result.txt", "text/plain")
        state.file_download(file_data, "analysis_result.txt")


initial_state = wf.init_state(
    {
        "image-path": "static/writer_logo.png",
        "app": {"title": "Recommendations for Rebalancing Portfolio"},
        "file": {"name": "", "file_path": ""},
        "analysis-result": "Your recommendations will appear here.",
        "processing-message": "",
        "visual_block_visible": False
    }
)


initial_state.import_stylesheet("style", "/static/custom.css?")
