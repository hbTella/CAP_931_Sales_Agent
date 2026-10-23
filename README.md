# CAP 931 – AI Sales Agent

## Project Overview

The AI Sales Agent is a Python application that helps sales teams prepare for customer discovery meetings. It researches prospective companies and their competitors, summarizes relevant business information, and generates discovery questions and potential sales opportunities.

The application uses a Streamlit interface and a locally running large language model (LLM) through Ollama to generate research summaries.

## Key Features

### 1. Sales Product Context
- Captures the sales product, category, value proposition, and target customers.
- Supports an uploaded product overview containing product features and business benefits.
- Uses the product information to provide context for sales research.

### 2. Company Website Research
- Retrieves publicly accessible company website content.
- Summarizes the company's mission and overview.
- Identifies products, services, and business priorities from the retrieved evidence.
- Generates five discovery questions for a Chief Data Officer (CDO).
- Displays the source URLs used for research.

### 3. Competitor Research
- Researches competitor websites provided by the user.
- Summarizes competitor offerings and competitive positioning.
- Identifies potential sales opportunities through relevant discovery questions.
- Displays source URLs for further review.

### 4. Local LLM Integration
- Uses Ollama to connect to a locally running language model.
- Uses the `qwen2.5:3b` model to generate research responses.
- Keeps the language model running locally rather than relying on a hosted LLM API.

### 5. Testing and Error Handling
- Includes automated tests for the application.
- Handles website retrieval errors and displays helpful error messages.
- Allows users to validate the generated research before using it in sales conversations.

## Technology Stack

- **Python** – application logic
- **Streamlit** – user interface
- **Ollama** – local LLM runtime
- **Qwen 2.5 3B** – language model
- **uv** – Python project and dependency management
- **Requests and Beautiful Soup** – website retrieval and HTML processing
- **pytest** – automated testing

CAP_931_Sales_Agent/
├── src/
│   └── cap_931_sales_agent/
│       ├── __init__.py
│       ├── app.py
│       ├── company_research_agent.py
│       ├── competitor_research_agent.py
│       └── llm_client.py
├── tests/
│   ├── test_ollama.py
│   ├── test_openai.py
│   ├── test_company_research.py
│   ├── test_competitor_research.py
│   └── test_llm_client.py
├── Hima_Tella_KB_Report_931.md
├── Hima_Tella_ KB_Report_CAP 931 .docx
├── per_scholas_template.docx
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore

The `src/` directory contains the application code, while the `tests/` directory contains the automated tests for the project.

The `src/cap_931_sales_agent/` directory contains the main application and research components. The `pyproject.toml` and `uv.lock` files manage the project dependencies.

## Prerequisites

Before running the application, install:

1. Python compatible with the project configuration.
2. [uv](https://docs.astral.sh/uv/).
3. [Ollama](https://ollama.com/).

## Setup and Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/hbTella/CAP_931_Sales_Agent.git
cd CAP_931_Sales_Agent
```

### Step 2: Install project dependencies

```bash
uv sync
```

This installs the dependencies specified in the project configuration and lockfile.

### Step 3: Download the Ollama model

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before launching the application. If necessary, start its local service using:

```bash
ollama serve
```

If Ollama is already running as a background service, you do not need to start it again.

## Running the Application

From the project root directory, run:

```bash
uv run streamlit run src/cap_931_sales_agent/app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

## How to Use the Application

1. Enter the sales product information and target customer details.
2. Upload the product overview if required by the interface.
3. Enter the prospective company's website URL.
4. Enter one or more competitor website URLs.
5. Run the research workflow.
6. Review the company overview, products and services, business priorities, and CDO discovery questions.
7. Review competitor summaries, competitive positioning, potential sales opportunities, and source URLs.
8. Verify the research before using it in a customer conversation.

## Running Tests

From the project root, run:

```bash
uv run pytest src/cap_931_sales_agent/ -v
```

The tests check the relevant application components and report whether they pass or fail.

## Limitations

- Website research depends on the availability and accessibility of public webpages.
- Some websites may block automated requests or return incomplete content.
- The language model may generate inaccurate or incomplete summaries and questions.
- Product names, company priorities, competitive claims, and source URLs should be verified before being used in business decisions.
- The local model must be available through Ollama for LLM-powered features to work.

## Future Improvements

Potential enhancements include:

- Improving website content extraction and source validation.
- Adding more robust handling of inaccessible websites.
- Improving discovery questions based on company-specific evidence.
- Adding report export options.
- Expanding automated test coverage.

## Author

Hima Bindu Tella

## Disclaimer

This project is intended for learning and sales research assistance. AI-generated content should be reviewed and verified before use in professional sales activities.