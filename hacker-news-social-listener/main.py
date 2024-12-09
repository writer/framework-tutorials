import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

import aiohttp
import pandas as pd
import requests
import writer as wf
from aiohttp import ClientSession
from dotenv import load_dotenv
from prompts import report_prompt
from writer import WriterState
from writer.ai import (
    Conversation,
    File,
    list_files,
    retrieve_file,
    retrieve_graph,
    upload_file,
)

load_dotenv()

GRAPH_ID = os.getenv("GRAPH_ID", "")
HACKERNEWS_API_URL = os.getenv("HACKERNEWS_API_URL", "")
WRITER_API_KEY = os.getenv("WRITER_API_KEY", "")

wf.Config.feature_flags = ["dataframeEditor"]


def main(state: WriterState) -> None:
    _delete_files_from_graph(GRAPH_ID)
    state["message_setup"] = "%Scraping data"

    posts, comments = _scrape_hackernews(state)
    state["message_setup"] = "%Data was scraped"
    posts_columns = ["title", "created_utc", "score", "num_comments", "url"]
    state["posts"] = (
        posts[posts_columns]
        if _verify_df(posts, posts_columns)
        else pd.DataFrame(data={"Info": ["Invalid data was scrapped"]})
    )
    if state["allow_comments"]:
        comments_columns = ["body", "author", "created_utc"]
        state["comments"] = (
            comments[comments_columns]
            if _verify_df(comments, comments_columns)
            else pd.DataFrame(data={"Info": ["Invalid data was scrapped"]})
        )
    state["message_setup"] = "%Scraped data, now saving to csv"

    _save_results_to_csv(state)
    state["message_setup"] = "%Saved data, now uploading to KG"

    files_path = "static/hackernews_posts.csv"
    _upload_file_and_add_to_graph(state, files_path, GRAPH_ID)
    state["message_setup"] = "%Uploaded file and added to graph"

    if state["allow_comments"]:
        file_path = "static/hackernews_comments.csv"
        _upload_file_and_add_to_graph(state, file_path, GRAPH_ID)

    state["message_setup"] = ""


def _verify_df(df: pd.DataFrame, columns: List) -> bool:
    if df is None:
        return False
    elif not all(column in df.columns for column in columns):
        return False
    else:
        return True


def _delete_files_from_graph(graph_id: str) -> None:
    try:
        graph = retrieve_graph(graph_id=graph_id)
        graph_files = list_files(config={"extra_query": {"graph_id": graph_id}})

        if not graph_files:
            print("No files found in the specified graph.")

        for file_id in graph_files:
            graph.remove_file(file_id.id)

    except Exception as e:
        print(f"An error while file deletion occurred: {str(e)}")


def _get_file_from_graph(file_id: str) -> Optional[File]:
    try:
        return retrieve_file(file_id=file_id)
    except Exception as e:
        print(f"An error while file obtainment occurred: {str(e)}")
        return None


def _scrape_hackernews(state: WriterState) -> tuple[Any, Any]:
    stories_ids = _get_stories_ids(state)
    posts, comments_ids = _get_posts(state, stories_ids)
    comments = _get_comments(state, comments_ids)

    if len(posts) > 0:
        state["posts"] = pd.DataFrame(posts).sort_values(
            by=["score", "num_comments"], ascending=False
        )

    if len(comments) > 0:
        state["comments"] = pd.DataFrame(comments)

    return state["posts"], state["comments"]


def _get_stories_ids(state: WriterState) -> List[str]:
    top_stories_url = f"{HACKERNEWS_API_URL}/topstories.json"
    try:
        response = requests.get(url=top_stories_url, timeout=5)

        if response.status_code != 200:
            print("Failed to fetch data from Hacker News")
            return []

        return response.json()[: int(state["fetch_limit"])]
    except Exception as e:
        print(f"Failed to fetch story ids from Hacker News: {str(e)}")
        state["message_setup"] = ""
        return []


def _get_posts(state: WriterState, stories_ids: List[str]) -> (List, List):
    try:
        stories_urls = [
            f"{HACKERNEWS_API_URL}/item/{story_id}.json" for story_id in stories_ids
        ]
        stories = asyncio.run(_perform_calls(stories_urls))

        comments_ids = []
        posts_data = []

        for story in stories:
            posts_data.append(
                {
                    "post_id": str(story.get("id", "")),
                    "title": story.get("title", ""),
                    "author": story.get("by", ""),
                    "score": int(story.get("score", 0)),
                    "created_utc": datetime.fromtimestamp(story.get("time")).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "num_comments": int(story.get("descendants", 0)),
                    "url": story.get("url", ""),
                }
            )

            kids = story.get("kids", [])
            if kids:
                comments_ids += kids

        return posts_data, comments_ids
    except Exception as e:
        print(f"Failed to fetch stories from Hacker News: {str(e)}")
        state["message_setup"] = ""
        return [], []


def _get_comments(state: WriterState, comments_ids: List[str]) -> List[dict]:
    try:
        comments_urls = [
            f"{HACKERNEWS_API_URL}/item/{comment_id}.json"
            for comment_id in comments_ids
        ]
        comments_data = []

        comments = asyncio.run(_perform_calls(comments_urls))

        for comment in comments:
            comments_data.append(
                {
                    "comment_id": str(comment.get("id", "")),
                    "post_id": str(comment.get("parent", "")),
                    "author": comment.get("by", "anonymous"),
                    "created_utc": datetime.fromtimestamp(comment.get("time")).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "body": comment.get("text", ""),
                }
            )

        return comments_data
    except Exception as e:
        print(f"Failed to fetch comments from Hacker News: {str(e)}")
        state["message_setup"] = ""
        return []


async def _fetch_data(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.json()


async def _perform_calls(urls: List[str]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return results


def _save_results_to_csv(state: WriterState) -> None:
    state["posts"].to_csv("static/hackernews_posts.csv", index=False)
    if state["allow_comments"]:
        state["comments"].to_csv("static/hackernews_comments.csv", index=False)


def _upload_file_and_add_to_graph(
    state: WriterState, file_path: str, graph_id: str
) -> dict:
    try:
        file_id = _upload_file(file_path)
        _add_file_to_graph(graph_id, file_id)

        return {"file_id": file_id, "graph_id": graph_id}
    except Exception as e:
        print(f"An error while file uploading occurred: {str(e)}")
        state["message_setup"] = ""
        return {}


def _upload_file(file_path: str) -> str:
    with open(file_path, "rb") as file:
        uploaded_file = upload_file(
            data=file.read(), name=Path(file.name).stem, type="text/csv"
        )
        return uploaded_file.id


def _add_file_to_graph(graph_id: str, file_id: str) -> None:
    graph = retrieve_graph(graph_id)
    graph.add_file(file_id)


def _handle_contributing_sources(state: WriterState, graph_data: dict) -> None:
    sources = graph_data.get("sources")
    contributing_sources = {}
    if sources:
        for index, source in enumerate(sources):
            source_file = _get_file_from_graph(source["file_id"])
            source_snippet = source["snippet"]

            contributing_sources.update(
                {
                    str(index): {
                        "name": f"📄 {source_file.name}",
                        "file_css": "file",
                        "content": source_snippet,
                        "content_css": "file-text",
                    }
                }
            )

        state["contributing_sources"] = contributing_sources
        state["contributing_sources_vis"] = True
        state["contributing_sources_button_text"] = "View contributing sources ▸"


def run_report(state: WriterState) -> None:
    try:
        state["message_report"] = "%Creating report"

        prompt = report_prompt(state["posts"], state["comments"])
        report_convo = Conversation()
        report_convo += {"role": "user", "content": prompt}
        response = report_convo.stream_complete()

        state["prepared_report"] = ""

        for chunk in response:
            state["prepared_report"] += chunk["content"]

        state["message_report"] = ""
    except Exception as e:
        state["prepared_report"] = "Something went wrong. Please try again!"
        state["message_report"] = ""
        raise e


def fetch_posts(state: WriterState) -> None:
    main(state)


def message_handler(payload: dict, state: WriterState) -> None:
    try:
        state.call_frontend_function("scripts", "enableDisableTextarea", ["true"])
        state["conversation"] += payload

        graph = retrieve_graph(GRAPH_ID)

        response = state["conversation"].stream_complete(tools=graph)

        for chunk in response:
            state["conversation"] += chunk

        graph_data = state["conversation"].messages[-1].get("graph_data")
        if graph_data:
            _handle_contributing_sources(state, graph_data)

        state.call_frontend_function("scripts", "enableDisableTextarea", ["false"])
    except Exception as e:
        state["conversation"] += {
            "role": "assistant",
            "content": "Something went wrong. Please try again!",
        }
        state.call_frontend_function("scripts", "enableDisableTextarea", ["false"])
        raise e


def contributing_sources_change_vis(state: WriterState) -> None:
    state["contributing_sources_vis"] = not state["contributing_sources_vis"]
    if state["contributing_sources_vis"]:
        state["contributing_sources_button_text"] = "View contributing sources ▸"
    else:
        state["contributing_sources_button_text"] = "View contributing sources ◂"


initial_state = wf.init_state(
    {
        "conversation": Conversation(
            [
                {
                    "role": "assistant",
                    "content": "Ask me anything about the scraped Hacker News data.",
                },
            ],
        ),
        "contributing_sources": {},
        "response": None,
        "file_path": "",
        "graph_name": "",
        "uploaded_file": None,
        "graph_id": None,
        "prepared_report": "# **Trend report**",
        "contributing_sources_button_text": "View contributing sources ◂",
        "message_setup": "",
        "message_report": "",
        "contributing_sources_vis": False,
        "fetch_limit": 100,
        "allow_comments": True,
    }
)

initial_state.import_stylesheet("style", "/static/custom.css")
