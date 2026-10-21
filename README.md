# CAP 931 – Sales Research Agent

## Project Overview

The CAP 931 Sales Research Agent is a Python application that helps sales representatives prepare for meetings with prospective customers. It uses AI to research company websites and competitor websites and generates a Word report containing company information, product details, competitive positioning, and discovery questions.

The application uses Streamlit for its user interface and a locally running Ollama model to generate research summaries.

## Features

- Collects product name, category, value proposition, and target customer information.
- Researches a prospective company's website.
- Identifies company products, services, and business priorities.
- Generates five discovery questions for a Chief Data Officer (CDO).
- Researches competitor websites and summarizes their positioning.
- Generates competitor-specific discovery questions.
- Creates a Word report using the provided Per Scholas template.
- Includes source URLs in the generated report.
- Uses a local language model rather than requiring a paid OpenAI API for the main workflow.

## Technologies Used

- Python
- Streamlit
- Ollama
- Qwen 2.5 3B
- Requests
- Beautiful Soup
- python-docx
- pytest
- uv for Python dependency and project management

## Prerequisites

Install the following before running the application:

- Python 3.14 or a compatible version supported by the project.
- uv
- Ollama
- The Qwen 2.5 3B model downloaded in Ollama.

To download the model, run:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before using the application.

## Installation

Clone the repository and open the project directory:

```bash
git clone https://github.com/hbTella/CAP_931_Sales_Agent.git
cd CAP_931_Sales_Agent
```

Install the project dependencies:

```bash
uv sync --dev
```

## Running the Application

Start the Streamlit application:

```bash
uv run streamlit run src/cap_931_sales_agent/app.py
```

Open the local URL displayed in the terminal.

Enter the product details, company website, and competitor website URLs. Submit the form to generate the sales research report.

## Running Tests

Run the automated tests with:

```bash
uv run pytest src/cap_931_sales_agent/ -v
```

The current test suite contains five tests covering company research, competitor research, the LLM client, Ollama configuration, and local-model configuration.

Some tests use simplified or mocked checks. The company research test makes live website and local-model calls, so its runtime may vary.

## Project Structure

```text
CAP_931_Sales_Agent/
├── per_scholas_template.docx
├── pyproject.toml
├── uv.lock
├── README.md
└── src/
    └── cap_931_sales_agent/
        ├── app.py
        ├── company_research_agent.py
        ├── competitor_research_agent.py
        ├── llm_client.py
        ├── report_generator.py
        ├── test_company_research.py
        ├── test_competitor_research.py
        ├── test_llm_client.py
        ├── test_ollama.py
        └── test_openai.py
```

## Limitations

- Research quality depends on the content accessible on the supplied websites.
- The local language model may produce incomplete or inaccurate summaries; generated findings should be verified before a sales meeting.
- The current research process may not discover every relevant company page or product offering.
- Uploaded-document analysis and its integration into the research workflow require further verification.
- The automated tests do not yet provide complete end-to-end coverage of the application.

## Responsible Use

Use publicly accessible information where possible. Verify important claims against the cited sources before relying on them. Avoid entering confidential customer or company information unless you are authorized to do so.

## Author

Hima Bindu Tella

## Repository

https://github.com/hbTella/CAP_931_Sales_Agent
