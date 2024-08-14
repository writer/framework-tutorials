# Embedded Knowledge Graph chat
This Writer Framework application lets you upload files to a Knowledge Graph and then use an embedded no-code chat application to query them with graph-based RAG. The sample data included in the `static` folder is for product descriptions, but you could use this application in any other domain. 

The main functionality of the app is in `main.py`. To run this application, you will need to do three things:

1. Create a Knowledge Graph, either in using AI Studio [no-code tools](https://support.writer.com/article/242-how-to-create-and-manage-a-knowledge-graph#How-to-create-a-new-Knowledge-Graph-dlpSX) or [using the API](https://dev.writer.com/api-guides/knowledge-graph).
2. Create a no-code chat application in AI Studio. You can [follow this guide on our docs](https://dev.writer.com/no-code/building-a-chat-app). Be sure to toggle "Knowledge Graph mode" in the app.
3. In the "Deploy" tab for the chat application, toggle the "Embed" option for the application and retrieve the embed URL. Check out [this document](https://dev.writer.com/no-code/deploying-an-app) to learn how to do this. The embed URL will go in the `iframe` component's `src` input.

You may also want to check out the [Knowledge Graph API reference](https://dev.writer.com/api-guides/api-reference/kg-api/create-graph) and the [File API reference](https://dev.writer.com/api-guides/api-reference/file-api/upload-files).

## Running the application
First, install Writer Frameowrk:

```sh
pip install writer
```

To build this application, you'll need to sign up for [Writer AI Studio](https://app.writer.com/aistudio/signup?utm_campaign=devrel) and create a new Framework application. This will create an API key. To pass your API key to the Writer Framework, you'll need to set an environment variable called `WRITER_API_KEY`:

```sh
export WRITER_API_KEY=your-api-key
```

Then, navigate to this folder and run:

```sh
writer edit .
```

To learn more, check out the [full documentation for Writer Framework](https://dev.writer.com/framework/introduction).

## About Writer

Writer is the full-stack generative AI platform for enterprises. Quickly and easily build and deploy generative AI apps with a suite of developer tools fully integrated with our platform of LLMs, graph-based RAG tools, AI guardrails, and more. Learn more at [writer.com](https://www.writer.com?utm_source=github&utm_medium=readme&utm_campaign=framework).