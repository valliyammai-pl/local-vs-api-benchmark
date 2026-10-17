import os
import time
import csv
import io
from datetime import datetime

import psutil
import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

LOCAL_URL = "http://localhost:11434/api/generate"
LOCAL_MODEL = "smollm2:360m-instruct-q5_K_S"
GEMINI_MODEL = "gemini-3.8-flash"

st.set_page_config(
    page_title="Local vs Cloud AI Benchmark",
    page_icon="🤖",
    layout="wide",
)

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🤖 Local vs Cloud AI Benchmark")
st.caption("Comparing answer quality, latency, and resource usage")

st.info(
    "Research prototype: both models receive the same prompt. "
    "Run multiple trials for more reliable measurements."
)

question = st.text_area(
    "Enter a question for both AI models",
    value="Explain artificial intelligence in three simple sentences.",
    height=110,
)

run_button = st.button("🚀 Compare Both Models", type="primary")

if run_button:
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    local_answer = ""
    gemini_answer = ""
    local_seconds = None
    gemini_seconds = None
    local_error = None
    gemini_error = None
    local_ram_delta = None
    gemini_cost = None

    # Run local model
    with st.spinner("Running local AI through Ollama..."):
        try:
            ram_before = psutil.virtual_memory().used
            start = time.perf_counter()

            response = requests.post(
                LOCAL_URL,
                json={
                    "model": LOCAL_MODEL,
                    "prompt": question,
                    "stream": False,
                    "options": {"num_predict": 80},
                },
                timeout=300,
            )
            response.raise_for_status()
            data = response.json()

            local_seconds = time.perf_counter() - start
            ram_after = psutil.virtual_memory().used

            local_answer = data.get("response", "")
            local_ram_delta = (ram_after - ram_before) / (1024 ** 2)

        except Exception as exc:
            local_error = str(exc)

    # Run Gemini
    with st.spinner("Running cloud AI through Gemini..."):
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise RuntimeError("GEMINI_API_KEY is missing from .env")

            client = genai.Client(api_key=api_key)
            start = time.perf_counter()

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=question,
            )

            gemini_seconds = time.perf_counter() - start
            gemini_answer = response.text or ""

            # Exact cost depends on model pricing and token usage.
            # We leave it blank rather than invent a cost.
            gemini_cost = None

        except Exception as exc:
            gemini_error = str(exc)

    st.session_state.last_result = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "question": question,
        "local_answer": local_answer,
        "local_seconds": local_seconds,
        "local_ram_delta_mb": local_ram_delta,
        "local_error": local_error,
        "gemini_answer": gemini_answer,
        "gemini_seconds": gemini_seconds,
        "gemini_cost": gemini_cost,
        "gemini_error": gemini_error,
    }

    st.session_state.history.append(st.session_state.last_result)

if "last_result" in st.session_state:
    result = st.session_state.last_result

    st.divider()
    st.subheader("Comparison Results")

    left, right = st.columns(2)

    with left:
        st.markdown("### 💻 Local AI — SmolLM2")
        if result["local_error"]:
            st.error(result["local_error"])
        else:
            st.metric("Response time", f'{result["local_seconds"]:.2f} sec')
            st.write(result["local_answer"])

    with right:
        st.markdown("### ☁️ Cloud AI — Gemini")
        if result["gemini_error"]:
            st.error(result["gemini_error"])
        else:
            st.metric("Response time", f'{result["gemini_seconds"]:.2f} sec')
            st.write(result["gemini_answer"])

    st.subheader("Measured Metrics")

    metric_rows = [
        {
            "Metric": "Response time (seconds)",
            "Local SmolLM2": result["local_seconds"],
            "Cloud Gemini": result["gemini_seconds"],
        },
        {
            "Metric": "RAM change during request (MB)",
            "Local SmolLM2": result["local_ram_delta_mb"],
            "Cloud Gemini": "Not measured locally",
        },
        {
            "Metric": "API cost",
            "Local SmolLM2": "No per-request cloud API charge",
            "Cloud Gemini": "Not calculated",
        },
    ]

    st.dataframe([{k: str(v) for k, v in row.items()} for row in metric_rows], width="stretch")

    st.caption(
        "RAM change is a system-wide snapshot difference, not peak model RAM. "
        "Cloud API cost is not calculated yet. Check your provider's pricing "
        "and usage data before reporting cost results."
    )

    st.subheader("Export Experiment Results")

    output = io.StringIO()
    fields = [
        "timestamp",
        "question",
        "local_answer",
        "local_seconds",
        "local_ram_delta_mb",
        "local_error",
        "gemini_answer",
        "gemini_seconds",
        "gemini_error",
    ]

    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    for item in st.session_state.history:
        writer.writerow({key: item.get(key) for key in fields})

    st.download_button(
        "Download results as CSV",
        data=output.getvalue(),
        file_name="benchmark_results.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "Prototype note: response time is measured locally from request start "
    "to response receipt. Answer quality requires a separate, consistent "
    "evaluation rubric."
)
