import asyncio

import writer as wf
from dotenv import load_dotenv
from writer import WriterState
from writerai import AsyncWriter
from writerai.types.chat_chat_params import Message

load_dotenv()

def handle_user_input(payload: str,  state: WriterState) -> None:
    asyncio.run(_ask_models(payload, state))


def handle_prompt_button(context: dict, state: WriterState) -> None:
    state["user-prompt"] = state[context["target"]+'-full']
    asyncio.run(_ask_models(state[context["target"]+'-full'], state))


def handle_dropdown_choice(context: dict, payload: str, state: WriterState) -> None:
    if "right" in context["target"]:
        state["palmyra-description-right"] = state["palmyra-models-description"][payload]
    else:
        state["palmyra-description-left"] = state["palmyra-models-description"][payload]


async def _ask_models(prompt: str, state: WriterState) -> None:
    state["palmyra-left-conversation"].append(Message(role="user", content=prompt))
    state["palmyra-right-conversation"].append(Message(role="user", content=prompt))

    async_writer_client = AsyncWriter()

    await asyncio.gather(
        _perform_async_streaming(async_writer_client, state["palmyra-left-model"], "left", state),
        _perform_async_streaming(async_writer_client, state["palmyra-right-model"], "right", state),
    )


async def _perform_async_streaming(client: AsyncWriter, model: str, side: str, state: WriterState) -> None:
    try:
        response = await client.chat.chat(
            model=model,
            messages=state[f"palmyra-{side}-conversation"],
            stream=True,
            max_tokens=state[f"palmyra-{side}-max-tokens"],
            temperature=state[f"palmyra-{side}-temperature"],
        )

        response_message = ""
        state[f"palmyra-{side}-response"] = ""

        async for message in response:
            content = message.choices[0].delta.content
            content = content if content is not None else ""
            response_message += content
            state[f"palmyra-{side}-response"] += content

        state[f"palmyra-{side}-conversation"].append(Message(role="assistant", content=response_message))

    except Exception as e:
        response_message = "Something went wrong. Please, try again."
        state[f"palmyra-{side}-conversation"].append(Message(role="assistant", content=response_message))
        raise e

palmyra_models_description = {
        "palmyra-x-004": "**Palmyra X 004** is our newest and most advanced language model with a large context window of up to 128,000 tokens. This model excels in processing and understanding complex tasks, making it ideal for workflow automation, coding tasks, and data analysis.",
        "palmyra-med": "**Palmyra Medical** is the latest version of our healthcare model and the most accurate in the market. The Writer full-stack generative AI platform is used by the world’s leading Fortune 50 healthcare companies to help improve patient outcomes with powerful AI that are infused with deep medical knowledge.",
        "palmyra-fin-32k": "**Palmyra Financial** is Writer’s specialized language model for the finance industry, designed to support critical financial workflows with precision in terminology and document analysis. Palmyra Fin empowers financial organizations to streamline processes and make data-driven decisions confidently.",
        "palmyra-creative": "**Palmyra Creative** is Writer's purpose-built language model, engineered to elevate creative thinking and writing across diverse professional contexts. With capabilities that amplify originality and adaptability, it caters to industries and teams where innovation drives success. ",
    }

initial_state = wf.init_state(
    {
    "palmyra-models": {
        "palmyra-x-004": "Palmyra X 004",
        "palmyra-med": "Palmyra Medical",
        "palmyra-fin-32k": "Palmyra Financial",
        "palmyra-creative": "Palmyra Creative",
    },
    "palmyra-models-description": palmyra_models_description,
    "palmyra-left-conversation": [],
    "palmyra-left-response": "Model response will appear here...",
    "palmyra-left-model": "palmyra-x-004",
    "palmyra-left-temperature": 0.7,
    "palmyra-left-max-tokens": 16384,
    "palmyra-description-left": palmyra_models_description["palmyra-x-004"],
    "palmyra-right-conversation": [],
    "palmyra-right-response": "Model response will appear here...",
    "palmyra-right-model": "palmyra-creative",
    "palmyra-right-temperature": 0.7,
    "palmyra-right-max-tokens": 16384,
    "palmyra-description-right": palmyra_models_description["palmyra-creative"],
    "user-prompt": "",
    "prompt-left-button": "Brainstorm bakery strategies",
    "prompt-left-button-full": "Imagine you're a struggling small-town bakery competing with a chain that opened across the street. Brainstorm unconventional strategies to win over customers without lowering prices.",
    "prompt-center-button": "Explain AI to a high schooler",
    "prompt-center-button-full": "Write a guide for a programmer who wants to explain their AI side project to a high schooler. The explanation must be engaging, simple, and use humorous analogies, while avoiding technical jargon.",
    "prompt-right-button": "Zero gravity game",
    "prompt-right-button-full": "Design a game that could only exist in zero gravity.",
    }
)

initial_state.import_stylesheet("style", "/static/custom.css")
