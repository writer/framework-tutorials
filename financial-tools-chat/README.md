# Financial Tools Chat

A conversational interface for financial research tools. This application was created using Writer Framework and uses the Palmyra Financial model.

## Description

Financial Tools Chat is an interactive chat application that helps users with various financial research tools. Users can interact with the application through a chat interface to research and analyze:
- Stock price data
- Income statements
- Earnings reports (Note: Earnings reports are stored locally in `earnings-data.json`. Feel free to swap this out with a call to an API that provides earnings data.)

## Prerequisites
First, ensure you have Poetry installed. Then, in the project directory, install the dependencies by running:

```sh
poetry install
```

### Sign up for Writer AI Studio
To build this application, you'll need to sign up for [Writer AI Studio](https://app.writer.com/aistudio/signup?utm_campaign=devrel) and create a new API Key. 

To pass your API key to the Writer Framework, you'll need to set an environment variable called `WRITER_API_KEY`:
```sh
export WRITER_API_KEY=your-api-key
```

You can also set the `WRITER_API_KEY` in the `.env` file.

### Create a no-code text generation application
You'll also need to [create a no-code text generation application](https://dev.writer.com/no-code/building-a-text-generation-app) in Writer AI Studio and add the Palmyra Financial model to it to run the earnings call analysis. Add two fields to the application: `name` (for the symbol) and `data` (for the earnings report). You can use the `earnings-prompt.txt` file as a prompt for the earnings call analysis.

## Edit and run the application
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
