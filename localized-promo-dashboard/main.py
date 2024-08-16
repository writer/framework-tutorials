import re

import pandas as pd
import plotly.express as px
import writer as wf
import writer.ai
from prompts import base_prompt


def handle_file_upload_click(payload, state):
    _save_file(state, payload[0])
    _generate_output_data(state, state["file"]["file_path"])


def _save_file(state, file):
    name = file.get("name")
    state["file"]["name"] = name
    state["file"]["file_path"] = f"data/{name}"
    file_data = file.get("data")
    with open(f"data/{name}", "wb") as file_handle:
        file_handle.write(file_data)


def _generate_output_data(state, file_path):
    state["data_frame"] = pd.read_csv(file_path)
    _set_default_input(state)
    _generate_segments_chart(state)
    _generate_promo_materials(state)


def _set_default_input(state):
    if not state["data_frame"].empty:
        state["input_data"]["location"] = state["data_frame"].at[0, "City"]
        state["input_data"]["segment"] = state["data_frame"].at[0, "Segment"]


def handle_chart_click(payload, state):
    point_number = payload[0]["pointNumber"]
    fig = state["generated_charts"]["segments"]
    point_id = fig.data[0]["ids"][point_number]
    point_segments = point_id.split("/")

    if len(point_segments) < 3:
        return
    _all, location, segment = point_segments

    if (
        state["input_data"]["location"] == location
        and state["input_data"]["segment"] == segment
    ):
        return

    state["input_data"]["location"] = location
    state["input_data"]["segment"] = segment

    _generate_promo_materials(state)


def _generate_promo_materials(state):
    state["available"] = False
    state["message"] = "% Generating promotional material..."

    social_post = _generate_post(
        state["base_prompt"].format(**state["input_data"].to_dict())
    )
    hashtags = _generate_post_hashtags(social_post)
    promo_email = _generate_promo_email(social_post)
    blog_post = _generate_blog_post(social_post)

    state["generated_data"]["social_post"] = social_post
    state["generated_data"]["hashtags"] = {
        item: item for item in re.findall(r"#\w+", hashtags)
    }
    state["generated_data"]["promo_email"] = promo_email
    state["generated_data"]["blog_post"] = blog_post

    state["message"] = ""
    state["available"] = True


def _generate_post(prompt):
    social_post = writer.ai.complete(prompt)
    return social_post


def _generate_post_hashtags(social_post):
    prompt = (
        f"Based on the following social media post, output ten hashtags in the language of the post, "
        f"for example #dogs #cats #food #pets etc:\n{social_post}"
    )
    hashtags = writer.ai.complete(prompt)
    return hashtags


def _generate_promo_email(social_post):
    prompt = f"Based on the following social media post, create a promotional email:\n{social_post}"
    promo_email = writer.ai.complete(prompt)
    return promo_email


def _generate_blog_post(social_post):
    prompt = (
        f"Based on the following social media post, create a blog post:\n{social_post}"
    )
    blog_post = writer.ai.complete(prompt)
    return blog_post


def _generate_segments_chart(state):
    colors = [
        "#FFCFC2",
        "#B5EEEE",
        "#E4E9FF",
        "#FFD0F7",
        "#CECFFF",
        "#F2FFA2",
        "#B1EFDD",
        "#E5D1FA",
        "#FFE3FA",
    ]
    fig = px.treemap(
        state["data_frame"],
        path=[px.Constant("all"), "City", "Segment"],
        values="Revenue",
        hover_data=["City", "Segment"],
        color_discrete_sequence=colors,
    )
    state["generated_charts"]["segments"] = fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#F5F5F9"
    )


def _init_default_output_fields(state):
    _generate_output_data(state, "data/default_segments.csv")
    _set_default_input(state)


initial_state = wf.init_state(
    {
        "base_prompt": base_prompt,
        "file": {"name": "", "file_path": ""},
        "input_data": {
            "location": "",
            "segment": "",
            "product_description": "Nomnom the cereal bar made in London, UK, crafted only with natural ingredients.",
        },
        "generated_data": {"social_post": "", "promo_email": "", "blog_post": ""},
        "generated_charts": {
            "segments": None,
        },
        "message": "",
        "available": False,
    }
)


_init_default_output_fields(initial_state)
