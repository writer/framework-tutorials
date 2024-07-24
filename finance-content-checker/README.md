# Finance copy compliance checker
This application allows the user to paste in text and analyze it based on compliance guidelines.

Note: the prompts in `prompts.py` are tightly coupled to the formatting of the sample data. If you want to use a different format, be sure to update the prompts accordingy.

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