# Prescribing Information App

This is a Python application built with [Writer Framework](https://github.com/writer/writer-framework) that provides detailed prescribing information, side effects, and related PubMed articles for medications. The app uses the OpenFDA API and PubMed database to gather comprehensive drug information and present it in an easily digestible format. This application uses [Palmyra Med](https://huggingface.co/Writer/Palmyra-Med-70B) to summarize the prescribing information and our [graph-based RAG tool](https://dev.writer.com/api-guides/kg-chat) powered by Palmyra X 004 to enable users to ask questions about the fetched information.

To learn more about Writer Framework, check out our [comprehensive docs](https://dev.writer.com/framework/introduction).

## Features

- Fetch and display full prescribing information from OpenFDA API
- Show drug side effects and adverse reactions
- Search and display related PubMed articles
- Automatic summarization of prescribing information using Palmyra Med
- Interactive chat interface for drug-related queries using our graph-based RAG tool
- Display of contributing sources for information

## Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- Writer Framework API Key (follow the [Writer Framework Quickstart guide](https://dev.writer.com/framework/quickstart) to get one)
- Knowledge Graph ID (you can create a Knowledge Graph [through AI Studio](https://support.writer.com/article/242-how-to-create-and-manage-a-knowledge-graph) or [through the API](https://dev.writer.com/api-guides/knowledge-graph))

## Installation

1. Clone the repository and navigate to the project directory:

```sh
cd prescribing-info-app
```

2. Install dependencies using Poetry:

```sh
poetry install
```

3. Create a `.env` file in the project root and add your credentials:

```sh
WRITER_API_KEY=your-api-key
GRAPH_ID=your-graph-id
```

## Usage

1. Activate the Poetry virtual environment:

```sh
poetry shell
```

2. Run the application:

```sh
writer run .
```

3. To make changes or edit the application:

```sh
writer edit .
```

## Project Structure

- `main.py` - Core application logic and Writer Framework integration
- `utils.py` - Utility functions for API interactions and data processing
- `prompts.py` - Prompt templates
- `static/` - Static files and CSS
- `.env` - Environment variables (not tracked in git)

## About Writer

Writer is the full-stack generative AI platform for enterprises. Quickly and easily build and deploy generative AI apps with a suite of developer tools fully integrated with our platform of LLMs, graph-based RAG tools, AI guardrails, and more. Learn more at [writer.com](https://www.writer.com?utm_source=github&utm_medium=readme&utm_campaign=devrel). 