# Portfolio rebalancing recommendation app

This Writer Framework application uses the powerful Palmyra-Fin model to analyze portfolio data and provide recommendations for rebalancing an investment portfolio. You can also download the analysis as a text file and clear results to start over. This app supports PDF or Excel files.

## Usage

1. Upload the data sample from the `example_data` folder of the app. Alternatively, you can upload your own portfolio data in Excel (.xls, .xlsx) or PDF format. Note that you may need adjust the prompts in `prompts.py` to achieve the best results.
2. Once the file is uploaded, the application analyzes your portfolio data, highlighting both positive and negative aspects such as stock selection, sector weightings, and more.
3. Based on this analysis, the app generates recommendations for rebalancing your portfolio to optimize performance.

## Running the application

First, ensure you have Poetry installed. Then, in the project directory, install the dependencies by running:

```sh
poetry install
```

To build this application, you'll need to sign up for [Writer AI Studio](https://app.writer.com/aistudio/signup?utm_campaign=devrel) and create a new API Key. To pass your API key to the Writer Framework, you'll need to set an environment variable called `WRITER_API_KEY`:

```sh
export WRITER_API_KEY=your-api-key
```

To make changes or edit the application, navigate to root folder and use the following command:


```sh
writer edit .
```

Depending on how your environment is set up, you may need to run `writer` with `poetry run` like this:

```sh
poetry run writer edit . 
```

Once you're ready to run the application, execute:

```sh
writer run . 
```

To learn more, check out the [full documentation for Writer Framework](https://dev.writer.com/framework/introduction).

## About Writer

Writer is the full-stack generative AI platform for enterprises. Quickly and easily build and deploy generative AI apps with a suite of developer tools fully integrated with our platform of LLMs, graph-based RAG tools, AI guardrails, and more. Learn more at [writer.com](https://www.writer.com?utm_source=github&utm_medium=readme&utm_campaign=framework).
