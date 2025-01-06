import asyncio
import json
import os
from datetime import datetime

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
from writer.ai import Conversation, retrieve_graph, stream_complete

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


def user_message(state: WriterState, payload: dict) -> None:
    try:
        state["conversation"] += payload
        graph = retrieve_graph(GRAPH_ID)
        response = state["conversation"].stream_complete(
            tools=graph, config={"model": "palmyra-med"}
        )

        for chunk in response:
            state["conversation"] += chunk

    except Exception as e:
        state["conversation"] += {
            "role": "assistant",
            "content": "Something went wrong. Please try again!",
        }
        raise e


initial_state = wf.init_state(
    {
        "adverse_reactions": "Drug adverse reactions will appear here...",
        "prescribing_info_summary": "Prescribing info summary will appear here...",
        "raw_prescribing_info": "Prescribing info will appear here...",
        "related_pubmed_articles": {},
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

initial_state.import_stylesheet("style", "/static/custom.css?111")
