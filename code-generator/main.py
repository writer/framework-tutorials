import writer as wf
from prompts import prompt
from writer.ai import Conversation


def generate_app_code(state, payload):
    state["conversation"] += {"role": "user", "content": payload}

    state["app_code"] = ""

    for chunk in state["conversation"].stream_complete():
        state["app_code"] += chunk["content"]
        clear_code_from_wrapping(state)
        state.call_frontend_function("scripts", "scrollToLastLine", [])

    state["conversation"] += {"role": "assistant", "content": state["app_code"]}


def clear_code_from_wrapping(state):
    mapping = {"typescript": "", "javascript": "", "tsx": "", "jsx": "", "```": ""}
    for k, v in mapping.items():
        state["app_code"] = state["app_code"].replace(k, v)


initial_state = wf.init_state(
    {
        "my_app": {"title": "Code generator"},
        "app_code": """
import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Hello World!</h1>
    </div>
  );
}

export default App;
    """,
        "conversation": Conversation(
            prompt_or_history=[{"role": "system", "content": prompt}],
            config={"model": "palmyra-x-004"},
        ),
    }
)

initial_state.import_stylesheet("style", "/static/custom.css?6")
initial_state.import_frontend_module("scripts", "/static/custom.js?1")
