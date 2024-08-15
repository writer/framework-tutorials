import re

import pandas as pd
import writer as wf
import writer.ai

from html_template import _format_output
from prompts import (
    _get_description_prompt,
    _get_features_prompt,
    _get_specifications_prompt,
    _get_translation_prompt,
)

pd.options.mode.chained_assignment = None


def handle_file_on_change(state, payload):
    if not state["processing-message"]:
        process_file(state, payload)


def process_file(state, payload):
    _clean_steps_results(state)
    _save_file(state, payload[0])
    df = _raw_excel_to_df(state)
    state["step1"]["cleaned_excel"] = _clean_excel(df)
    state["step1"]["generate-button-state"] = "no"


def _clean_steps_results(state):
    state["step2"]["product-descriptions"] = None
    state["step2"]["formatted-product-descriptions"] = "Products should go here"

    state["step3"]["spanish-translation"] = initial_df
    state["step3"]["french-translation"] = initial_df
    state["step3"]["hindi-translation"] = initial_df


def _save_file(state, file):
    name = file.get("name")
    state["file"]["name"] = name
    state["file"]["file_path"] = f"data/{name}"
    file_data = file.get("data")
    with open(f"data/{name}", "wb") as file_handle:
        file_handle.write(file_data)


def _raw_excel_to_df(state):
    data = pd.read_excel(state["file"]["file_path"])
    df = pd.DataFrame(data)
    return df


def _clean_excel(df):
    df = df[
        [
            "Name",
            "Long Description",
            "Manufacturer part number",
            "Feature 1",
            "Feature 2",
            "Feature 3",
            "Feature 4",
            "Generic Spec 1 Label",
            "Generic Spec 1 Value",
            "Generic Spec 2 Label",
            "Generic Spec 2 Value",
        ]
    ]
    df["Combined Features"] = df.apply(
        lambda row: f"{row['Feature 1']}\n{row['Feature 2']}\n{row['Feature 3']}\n{row['Feature 4']}",
        axis=1,
    )
    df["Combined Specifications"] = df.apply(_format_specs, axis=1)
    return df


def _format_specs(row):
    return (
        f"{row['Generic Spec 1 Label']} : {row['Generic Spec 1 Value']}",
        f"{row['Generic Spec 2 Label']} : {row['Generic Spec 2 Value']}",
    )


def handle_generate_button_click(state):
    if state["step2"]["product-descriptions"] is None:
        state["step1"]["generate-button-state"] = "yes"

        state["processing-message"] = "%Hang tight, we're generating your Product Descriptions!"

        formatted_product_descriptions = ""
        df = state["step1"]["cleaned_excel"]

        for index, row in df.iterrows():
            features_html = _get_features(row["Combined Features"])
            specifications_html = _get_specifications(row["Combined Specifications"])

            df.at[index, "o_Features"] = _strip_html_and_format_bullets(features_html)
            df.at[index, "o_Specifications"] = _strip_html_and_format_bullets(
                specifications_html
            )
            df.at[index, "o_Description"] = _get_description(
                desc=row["Long Description"]
            )

            state["processing-message"] = f"%Processing {index + 1} of {df.shape[0]} Product Descriptions"

            formatted_product_descriptions += _format_output(
                name=df.at[index, "Name"],
                desc=df.at[index, "o_Description"],
                product_num=df.at[index, "Manufacturer part number"],
                features=features_html,
                specifications=specifications_html,
            )
            state["step2"]["formatted-product-descriptions"] = (
                    "<div>" + formatted_product_descriptions + "</div>"
            )

            df.at[index, "html"] = formatted_product_descriptions

        _write_html_to_file(state["step2"]["formatted-product-descriptions"])

        df_temp = df[
            [
                "Name",
                "o_Description",
                "Manufacturer part number",
                "o_Features",
                "o_Specifications",
            ]
        ]
        df_sorted = df_temp.sort_values(by="Name")

        state["step2"]["product-descriptions"] = df_sorted

        state["step1"]["completed"] = "yes"
        state["processing-message"] = ""

        state["metrics"]["products"] = df_sorted.shape[0]
        state["step1"]["generate-button-state"] = "no"
    else:
        state["step1"]["completed"] = "yes"


def _get_features(features):
    prompt = _get_features_prompt(features)
    features = writer.ai.complete(prompt)
    return features


def _get_specifications(specifications):
    prompt = _get_specifications_prompt(specifications)
    specifications = writer.ai.complete(prompt)
    return specifications


def _strip_html_and_format_bullets(html_text):
    text_without_tags = re.sub(r"<[^>]+>", "", html_text)

    lines = text_without_tags.split("\n")

    formatted_lines = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            formatted_lines.append(f"- {stripped_line}")

    formatted_text = "\n".join(formatted_lines)

    return formatted_text


def _get_description(desc):
    prompt = _get_description_prompt(desc)
    description = writer.ai.complete(prompt)
    return description


def _write_html_to_file(html):
    with open("data/output-html.html", "w") as file_handle:
        file_handle.write(html)


def handle_translate_button_click(state):
    state["step2"]["completed"] = "yes"

    _update_translation_status(state, "spanish")
    _update_translation_status(state, "hindi")
    _update_translation_status(state, "french")

    state["processing-message"] = ""


def _update_translation_status(state, language):
    if state["step3"][f"{language}-translation"].equals(initial_df):
        state["processing-message"] = f"%Hang tight, we're translating your file to {language}"
        state["step3"][f"{language}-translation"] = _translate_to(state, language)


def _translate_to(state, language):
    df = state["step2"]["product-descriptions"]
    df_foreign = pd.DataFrame()
    for index, row in df.iterrows():
        df_foreign.at[index, "Name"] = _get_translation(
            text=row["Name"], language=language
        )
        df_foreign.at[index, "Description"] = _get_translation(
            text=row["o_Description"], language=language
        )
        df_foreign.at[index, "Part number"] = row["Manufacturer part number"]
        df_foreign.at[index, "Features"] = _get_translation(
            text=row["o_Features"], language=language
        )
        df_foreign.at[index, "Specifications"] = _get_translation(
            text=row["o_Specifications"], language=language
        )
    return df_foreign


def _get_translation(text, language):
    prompt = _get_translation_prompt(text, language)
    description = writer.ai.complete(prompt)
    cleaned_text = description.replace("**", "")
    return cleaned_text


def handle_step2_back_button_click(state):
    state["step1"]["completed"] = "no"
    state["step1"]["generate-button-state"] = "no"


def handle_step3_back_button_click(state):
    state["step2"]["completed"] = "no"


def handle_file_download(state):
    html_data = wf.pack_file("data/output-html.html", "text/html")
    file_name = "output-html.html"
    state.file_download(html_data, file_name)


placeholder_data = {
    "Description": ["Description 1", "Description 2", "Description 3"],
    "Label": ["Label 1", "Label 2", "Label 3"],
}
initial_df = pd.DataFrame(placeholder_data)

initial_state = wf.init_state(
    {
        "my_app": {"title": "MY APP"},
        "image-path": "static/writer_logo.png",
        "file": {"name": "", "file_path": ""},
        "metrics": {"products": 0},
        "step1": {
            "cleaned_excel": initial_df,
            "completed": "no",
            "generate-button-state": "yes",
            "styled-table": "<h3>csv table</h3>",
        },
        "step2": {
            "product-descriptions": None,
            "completed": "no",
            "formatted-product-descriptions": "notes should go here",
        },
        "step3": {
            "spanish-translation": initial_df,
            "hindi-translation": initial_df,
            "french-translation": initial_df,
        },
        "processing-message": "",
    }
)

initial_state.import_stylesheet(
    ".description, .summary, .category, .styled-table, .scroll-container",
    "/static/custom.css",
)
