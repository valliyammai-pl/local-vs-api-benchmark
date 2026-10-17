# Local Versus API Model Benchmark

A comparative study of local Large Language Model (LLM) inference and cloud-based API inference under constrained computing resources.

## Overview

This project compares a locally hosted language model with a cloud-based language model using a common prompt. It provides a dashboard for examining response generation time, answers, and selected system resource measurements.

The project is designed to explore the trade-offs between local and cloud inference on a resource-constrained device.

## Objectives

- Compare local and cloud model response times.
- Display model responses side by side for the same prompt.
- Observe system-level RAM changes during inference.
- Provide a dashboard for viewing comparison metrics.
- Export experiment results for further analysis.

## Models Used

| Type | Model | Interface |
|---|---|---|
| Local | SmolLM2 360M Instruct, Q5 quantized | Ollama |
| Cloud | Gemini | Google Gemini API |

## Technology Stack

- Python
- Streamlit
- Ollama
- Google Gemini API
- Pandas
- Requests
- psutil
- python-dotenv

## Features

- Interactive Streamlit dashboard
- Side-by-side local and cloud responses
- Response latency measurements
- Basic system RAM change measurements
- Experiment results export to CSV

## Project Structure

```text
local-vs-api-benchmark/
├── app.py
├── test_gemini.py
├── .env.example
├── .gitignore
└── README.md
```

*The structure above illustrates the main files; the actual files may vary depending on your project setup.*

## Requirements

- Python 3.10 or later
- Ollama installed and running
- The selected local model downloaded through Ollama
- A Google Gemini API key
- An internet connection for cloud inference

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/valliyammai-pl/local-vs-api-benchmark.git
cd local-vs-api-benchmark
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install streamlit requests pandas python-dotenv psutil google-genai
```

### 4. Configure the Gemini API key

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own key. Never commit your `.env` file or publish your API key.

### 5. Download the local model

```bash
ollama pull smollm2:360m-instruct-q5_K_S
```

Ensure Ollama is running before starting the application.

### 6. Run the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## Evaluation Metrics

- **Response latency:** Time taken for each model request to complete.
- **RAM change:** A system-wide memory snapshot difference during the request; it is not a direct measurement of peak memory used exclusively by the model.
- **Answer comparison:** Responses can be examined side by side. Formal answer-quality scoring requires an additional evaluation method.
- **Cost:** Actual cloud API costs are not yet calculated by the current prototype.

## Limitations

- Results may vary with device resources, network conditions, model configuration, and API availability.
- RAM snapshots do not represent model-specific peak memory usage.
- A single comparison is insufficient to establish general performance conclusions.
- Repeated experiments and a consistent quality evaluation method are needed for reliable conclusions.

## Future Work

- Conduct repeated experiments across multiple prompts.
- Calculate average latency and variability.
- Add a consistent answer-quality evaluation rubric.
- Estimate cloud API costs using applicable provider pricing and usage data.
- Improve resource monitoring and experiment reporting.

## Research Purpose

This project is an academic prototype intended to study the practical trade-offs between local and cloud-based language model inference under constrained computing resources.

## Author

**Valliyammai PL**

## License

A license has not yet been selected. Add an appropriate license before redistributing the project.
