import asyncio
import json
import os
from datetime import datetime
from typing import Optional

import writer as wf
from dotenv import load_dotenv
from prompts import prescribing_summary_prompt
from utils import (
    _get_drug_side_effects,
    _get_full_prescribing_info,
    _get_pubmed_sheets,
    _parse_prescribing_info,
    _upload_file_and_add_to_graph,
)
from writer import WriterState
from writer.ai import Conversation, File, retrieve_file, retrieve_graph, stream_complete

load_dotenv()

GRAPH_ID = os.getenv("GRAPH_ID", "")


def drug_switch(state: WriterState, payload: str) -> None:
    update_drug_data(state, payload)


def update_drug_data(state: WriterState, drug_name: str) -> None:
    prescribing_info, adverse_reactions = asyncio.run(
        _get_drug_prescribing_info(drug_name)
    )
    state["raw_prescribing_info"] = _parse_prescribing_info(prescribing_info[0])
    state["adverse_reactions"] = adverse_reactions
    state["related_pubmed_articles"] = _get_pubmed_sheets(drug_name)

    state["prescribing_info_summary"] = ""

    for chunk in stream_complete(
        prescribing_summary_prompt.format(
            prescribing_details=state["raw_prescribing_info"]
        )
    ):
        state["prescribing_info_summary"] += chunk

    asyncio.run(_upload_drug_data_into_graph(state, drug_name))


async def _get_drug_prescribing_info(drug_name: str) -> (dict, str):
    return await asyncio.gather(
        _get_full_prescribing_info(drug_name), _get_drug_side_effects(drug_name)
    )


async def _upload_drug_data_into_graph(state: WriterState, drug_name: str) -> None:
    input_params = [
        {
            "file_data": state["prescribing_info_summary"],
            "file_name": f"prescribing_info_summary_{drug_name}_{str(datetime.timestamp(datetime.now()))}",
            "graph_id": GRAPH_ID,
        },
        {
            "file_data": state["raw_prescribing_info"],
            "file_name": f"raw_prescribing_info_{drug_name}_{str(datetime.timestamp(datetime.now()))}",
            "graph_id": GRAPH_ID,
        },
        {
            "file_data": state["adverse_reactions"],
            "file_name": f"adverse_reactions_{drug_name}_{str(datetime.timestamp(datetime.now()))}",
            "graph_id": GRAPH_ID,
        },
        {
            "file_data": json.dumps(state["related_pubmed_articles"], default=str),
            "file_name": f"pubmed_articles_{drug_name}_{str(datetime.timestamp(datetime.now()))}",
            "graph_id": GRAPH_ID,
        },
    ]
    coroutines = [_upload_file_and_add_to_graph(**params) for params in input_params]
    await asyncio.gather(*coroutines)


def _handle_contributing_sources(state: WriterState, graph_data: dict) -> None:
    sources = graph_data.get("sources")
    contributing_sources = {}
    if sources:
        for index, source in enumerate(sources):
            source_file = _get_file_from_graph(source["file_id"])
            source_snippet = source["snippet"]

            raw_filename = f"📄 {source_file.name}"
            row_length = 30
            filename = " ".join(
                [
                    raw_filename[i : i + row_length]
                    for i in range(0, len(raw_filename), row_length)
                ]
            )

            contributing_sources.update(
                {
                    str(index): {
                        "name": filename,
                        "file_css": "file",
                        "content": source_snippet,
                        "content_css": "file-text",
                    }
                }
            )

        state["contributing_sources"] = contributing_sources
        state["contributing_sources_vis"] = True
        state["contributing_sources_button_text"] = "View contributing sources ▸"


def _get_file_from_graph(file_id: str) -> Optional[File]:
    try:
        return retrieve_file(file_id=file_id)
    except Exception as e:
        print(f"An error while file obtainment occurred: {str(e)}")
        return None


def user_message(state: WriterState, payload: dict) -> None:
    try:
        state["conversation"] += payload
        graph = retrieve_graph(GRAPH_ID)
        response = state["conversation"].stream_complete(
            tools=graph,
        )

        for chunk in response:
            state["conversation"] += chunk

        graph_data = state["conversation"].messages[-1].get("graph_data")
        if graph_data:
            _handle_contributing_sources(state, graph_data)

    except Exception as e:
        state["conversation"] += {
            "role": "assistant",
            "content": "Something went wrong. Please try again!",
        }
        raise e


def contributing_sources_change_vis(state: WriterState) -> None:
    state["contributing_sources_vis"] = not state["contributing_sources_vis"]
    if state["contributing_sources_vis"]:
        state["contributing_sources_button_text"] = "View contributing sources ▸"
    else:
        state["contributing_sources_button_text"] = "View contributing sources ◂"


initial_state = wf.init_state(
    {
        "adverse_reactions": "Drug adverse reactions will appear here...",
        "prescribing_info_summary": "Prescribing info summary will appear here...",
        "raw_prescribing_info": "Prescribing info will appear here...",
        "related_pubmed_articles": {},
        "contributing_sources_button_text": "View contributing sources ◂",
        "contributing_sources_vis": False,
        "contributing_sources": {},
        "conversation": Conversation(
            [
                {
                    "role": "assistant",
                    "content": "Hi! I can answer your questions "
                    "about the selected medication "
                    "based on its prescribing information "
                    "and related Pubmed articles.",
                },
            ],
        ),
    }
)

initial_state.import_stylesheet("style", "/static/custom.css?115")
