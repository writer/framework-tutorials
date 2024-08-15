# Product description page generator and translator
This Writer Framework application lets you upload product description data to generate formatted or translated product description page copy.

## Usage

1. Upload the data sample from the data folder of the app. Alternatively, you can upload your own data once the column names are the same as those in the sample file.
2. The application will iterate through the data set, rewrite the long description, and combine and format the features and specification fields.
3. The output is provided in downloadable HTML and Excel spreadsheets.
4. There are three languages currently configured for translation: Spanish, French and Hindi. Once the translation button is clicked the app will translate the Excel spreadsheet to all three.

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