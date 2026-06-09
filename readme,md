
# lm-runner

**lm-runner** is a robust, configurable pipeline designed for the batch processing and structured data extraction of medical lab reports. It leverages local Large Language Models (LLMs) and Vision-Language Models (VLMs) to process diverse input formats (images, text, and structured rows), extract standardized information, and provide comprehensive observability via Langfuse.

## 🌟 Features

- **Multi-Modal Batch Processing:** Seamlessly processes lab reports from multiple input directories (`data/images`, `data/text`, `data/rows`).
- **Local LLM Integration:** Supports local inference via **LM Studio** (OpenAI-compatible API) and **Ollama**, allowing for secure, on-premise processing of sensitive medical data.
- **Structured Data Extraction:** Enforces strict output schemas (via Pydantic) to ensure the LLM outputs clean, predictable, and usable JSON data.
- **Model Flexibility:** Easily switch between different models (e.g., `qwen3-coder`, `qwen3-vl`, `deepseek-ocr`) via a simple configuration file.
- **Observability & Tracing:** Built-in integration with **Langfuse** to track prompts, token usage, latency, and LLM call traces for debugging and optimization.

## 🏗️ Architecture & Workflow

1. **Ingestion:** The pipeline scans configured directories for raw lab report data (images, raw text, or tabular rows).
2. **Preprocessing:** Data is formatted and prepared for the specific model type (e.g., images are base64 encoded for VLMs).
3. **Inference:** Requests are sent to the local LLM endpoint (LM Studio or Ollama) with a tailored prompt and a strict JSON schema.
4. **Post-processing:** The raw LLM output is parsed, validated against the `LabReport` schema, and saved.
5. **Observability:** Every step, including the exact prompt, response, and latency, is logged to Langfuse.

## 🔄 Core Execution Logic (`main.py`)

The `main.py` script acts as the central orchestrator for the pipeline. Here is a detailed breakdown of its execution flow:

1. **Initialization & Configuration Loading:**
   - Reads `config.yaml` to determine the model provider (LM Studio/Ollama), endpoint URLs, input/output directories, and the target schema name.
   - Initializes the **Langfuse** client for telemetry (if enabled in the config).
   - Instantiates the LLM API client and loads the target **Pydantic schema** (e.g., `LabReport`) to enforce strict JSON formatting.

2. **Data Ingestion:**
   - Scans the configured `input_dir` (e.g., `./data/images`).
   - Loads the files into a processing list. If processing images, it handles the necessary base64 encoding; if processing text/rows, it reads the raw string data.

3. **Batch Processing Loop:**
   - Iterates through each document in the ingestion list.
   - **Prompt Construction:** Dynamically builds the system and user prompts, injecting the JSON schema instructions so the LLM knows exactly how to structure the extracted data.
   - **Inference & Tracing:** Sends the payload to the local LLM. This API call is wrapped in a Langfuse `trace` or `span` to record the exact prompt, raw response, token usage, and latency.
   - **Validation & Parsing:** Extracts the JSON from the LLM's raw text response and validates it against the Pydantic schema. 
   - **Output:** Saves the validated, structured JSON file to the `output_dir`.

4. **Finalization & Telemetry Flush:**
   - Logs a final summary to the console (total files processed, success/failure counts, and total execution time).
   - Flushes the Langfuse client to ensure all traces and metrics are successfully pushed to the Langfuse dashboard.

## ⚙️ Configuration

The pipeline is highly configurable via `config.yaml`. Key settings include:

```yaml
# Example snippet from config.yaml
model:
  provider: "lm_studio" # or "ollama"
  name: "qwen3-coder-30b-a3b-instruct"
  base_url: "http://localhost:1234/v1"

processing:
  input_dir: "./data/images"
  output_dir: "./data/processed"
  schema_name: "LabReport"

observability:
  langfuse_enabled: true
  # langfuse_public_key: "pk-..."
  # langfuse_secret_key: "sk-..."
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A local LLM server running (e.g., [LM Studio](https://lmstudio.ai/) or [Ollama](https://ollama.com/)) with your chosen model downloaded.
- (Optional) A [Langfuse](https://langfuse.com/) account or self-hosted instance for tracing.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/davardoust/lm-runner.git
   cd lm-runner
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (if using Langfuse):**
   Create a `.env` file in the root directory:
   ```env
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=https://cloud.langfuse.com # Or your self-hosted URL
   ```

### Usage

1. Ensure your local LLM server (LM Studio/Ollama) is running and the model specified in `config.yaml` is loaded.
2. Place your input files (images, text, etc.) into the designated input directory (e.g., `./data/images`).
3. Run the pipeline:
   ```bash
   python main.py
   ```
4. Check the output directory (e.g., `./data/processed`) for the extracted structured JSON files.

## 📂 Project Structure

```text
lm-runner/
├── main.py             # Main entry point and pipeline orchestrator
├── config.yaml         # Central configuration file
├── schemas.py          # Pydantic schemas for structured output validation
├── requirements.txt    # Python dependencies
├── src/                # Core pipeline logic (ingestion, inference, parsing)
├── utils/              # Helper utilities (API clients, file I/O, logging)
└── data/               # Data directories
    ├── images/         # Input: Lab report images (for VLMs/OCR)
    ├── text/           # Input: Raw text files
    ├── rows/           # Input: Tabular/row data
    └── processed/      # Output: Extracted structured JSONs
```
