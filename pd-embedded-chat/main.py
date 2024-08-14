import writer as wf
import writer.ai
import time

# Replace your Knowledge Graph ID here
GRAPH_ID = "your-kg-id-here"

# Adjust this timeout and sleep time as needed to avoid spamming the API
MAX_TIMEOUT = 90
SLEEP_TIME = 0.6

# Load the files and let the user know
def handle_file_upload(state, payload):
    state["files"] = payload
    if (len(state["files"]) == 1):
        state["message"] = f'File {state["files"][0]["name"]} ready to upload.'
    else:
        state["message"] = f'{len(state["files"])} files ready to upload.'

# Upload and add file(s) to Knowledge Graph 
def handle_add_to_graph(state):
    # Retrieve the graph
    graph = writer.ai.retrieve_graph(GRAPH_ID)
    current_completed = graph.file_status.completed
    new_completed = current_completed + len(state["files"])
    
    # Upload the files
    for file in state["files"]:
        state["message"] = f'% Kicking off upload of {file["name"]}...'
        uploaded_file = writer.ai.upload_file(data=file["data"], name=file["name"], type=file["type"])
        graph.add_file(uploaded_file)
    
    # Poll the graph until all files are indexed and marked as completed
    state["message"] = "% Processing and indexing files in Knowledge Graph..."
    start_time = time.time()
    while (time.time() - start_time) < MAX_TIMEOUT:
        try:
            updated_graph = writer.ai.retrieve_graph(GRAPH_ID)
            if updated_graph.file_status.completed == new_completed:
                state["message"] = "+ File(s) successfully added to graph."
                return True
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(SLEEP_TIME)
    state["message"] = "- Indexing timed out. Please try again."

# Initialise the state
wf.init_state({
    "my_app": {
        "title": "Chat with product descriptions"
    },
    "message": "",
    "files": []
})