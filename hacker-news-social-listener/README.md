# AI listener: Hacker News listening app
This application is built using the Writer Framework and is designed to scrape the top posts and comments from Hacker News. It processes the data, uploads it to a Writer Graph for further analysis, and generates AI-powered insights based on the content of the posts.
## Usage

1.Select the number of items you wish to process.
2. The application will generate raw data with analysis of posts and comments.
3. Ask specific questions using the Knowledge Graph chat.
4. Generate a detailed report from the processed data using the Prepared Report feature.

## Running the application
First, ensure you have Poetry installed. Then, in the project directory, install the dependencies by running:

```sh
poetry install
```

To build this application, you'll need to sign up for [Writer AI Studio](https://app.writer.com/aistudio/signup?utm_campaign=devrel), create a new API Key and Knowledge Graph. To pass your API key and Knowledge Graph to the Writer Framework, you'll need to set an environment variables called `WRITER_API_KEY` and `GRAPH_ID`:
```sh
export WRITER_API_KEY=your-api-key
```
```sh
export GRAPH_ID=your-graph-id
```

To make changes or edit the application, navigate to root folder and use the following command:


```sh
writer edit .
```

Once you're ready to run the application, execute:

```sh
writer run .
```

To learn more, check out the [full documentation for Writer Framework](https://dev.writer.com/framework/introduction).

## About Writer

Writer is the full-stack generative AI platform for enterprises. Quickly and easily build and deploy generative AI apps with a suite of developer tools fully integrated with our platform of LLMs, graph-based RAG tools, AI guardrails, and more. Learn more at [writer.com](https://www.writer.com?utm_source=github&utm_medium=readme&utm_campaign=framework).
