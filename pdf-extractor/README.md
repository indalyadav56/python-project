### LLM PDF Data Extraction (Example)

This example extracts structured data from a PDF using an LLM. It supports:
- OpenAI (default if `OPENAI_API_KEY` is set)
- Ollama (local) if `OLLAMA_MODEL` is set and an Ollama server is running

#### 1) Setup
```bash
# From the repo root
cd pdf-extractor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- For OpenAI: export your API key
```bash
export OPENAI_API_KEY=sk-...
```

- For Ollama: make sure Ollama is running, pull a model, and set model name
```bash
# Example models: llama3, llama3.1, mistral
ollama pull llama3
export OLLAMA_MODEL=llama3
# Optional base URL (defaults to http://localhost:11434)
export OLLAMA_BASE_URL=http://localhost:11434
```

(Optional) Create a `.env` file in `pdf-extractor/` with any of the above environment variables.

#### 2) Generate sample PDF
```bash
python make_sample_invoice.py
# -> prints the absolute path to examples/sample_invoice.pdf
```

#### 3) Run extraction
```bash
# OpenAI example
python extractor.py --pdf /absolute/path/to/examples/sample_invoice.pdf --schema invoice --out out.json --model gpt-4o-mini

# Ollama example
python extractor.py --provider ollama --model llama3 --pdf /absolute/path/to/examples/sample_invoice.pdf --schema invoice --out out.json
```
- If `OPENAI_API_KEY` is set, OpenAI is used. Otherwise if `OLLAMA_MODEL` is set, Ollama is used.
- `--model` is forwarded to the selected provider (`gpt-4o-mini` for OpenAI, `llama3` for Ollama, etc.).

#### 4) Output
- Writes structured JSON to `out.json` and prints a summary to stdout.

#### Notes
- This is a minimal example. Very large PDFs may exceed context limits; consider chunking or a map-reduce approach for production.
- Scanned PDFs may require OCR first (e.g., with Tesseract) before LLM extraction.
