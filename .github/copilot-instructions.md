## Repository Overview

This repository implements an AI content detector web app. Key runtime pieces:

- **Backend (Flask):** `routes.py` defines HTTP endpoints and app entry in `app.py` runs on port `2222`.
- **Model logic:** `ai_model.py` loads a HuggingFace model/tokenizer globally (at import time) using `config.MODEL_NAME` and exposes `predict_chunks(chunks)`.
- **File handling / OCR:** `file_utils.py` implements `allowed_file(filename)` and `extract_text(file)`; it uses `PyPDF2`, `pdf2image`, and `easyocr` for scanned documents.
- **Scraping:** `scrapper.py` uses Selenium + `webdriver_manager` with Chrome. On macOS the Chrome binary path is hard-coded to `/Applications/Google Chrome.app/...`.
- **Frontend:** templates are in `templates/` and static assets under `static/` (see `index.html`).

**Why these decisions matter**

- The model and tokenizer are loaded once globally to avoid repeated heavyweight initialization per request. Code modifications should preserve that pattern.
- OCR and PDF conversion can be expensive and rely on native libraries; `extract_text` falls back to OCR when PyPDF2 yields no text.
- The scraper requires a local Chrome binary and can be brittle in headless/containerized environments.

**How data flows**

- Incoming request -> `routes.predict` handles form `text` or uploaded `file`.
- Files go through `file_utils.extract_text` (PDF/Docx/image/OCR).
- Text is split using `split_into_chunks` (in `routes.py`) and passed to `ai_model.predict_chunks`.
- `predict_chunks` returns a list of `(ai_prob, human_prob)` tuples; the route zips chunks and probabilities and returns JSON.

## Common tasks & commands

- Create virtualenv and install deps:

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- Run the server locally:

  ```bash
  python app.py  # serves on port 2222
  ```

- Example API usage (form POST):

  ```bash
  curl -X POST -F "text=This is a test." http://localhost:2222/predict
  # Response: JSON list of {chunk, ai_prob, human_prob}
  ```

## Notable implementation patterns & gotchas

- **Global model load:** `ai_model.py` performs `AutoTokenizer.from_pretrained` and `AutoModelForSequenceClassification.from_pretrained` at module import. Avoid relocating this to per-request code.
- **Model output ordering:** The code assumes logits map to `[AI, HUMAN]` and extracts `probs[0][0]` as AI probability. Confirm the class order before swapping models.
- **Chunking:** `split_into_chunks` in `routes.py` normalizes newlines, splits paragraphs, then sentences by punctuation. If you change it, keep consistent chunk sizes for model input.
- **GUI interaction in server:** `/export_pdf` uses a Tkinter folder dialog to select save location. That blocks and requires a GUI session; it will fail silently in headless/container environments. Replace with a request-provided path or downloadable response if running headless.
- **Scraper:** `scrapper.scrap_text` uses Selenium with `--headless=new`. Ensure Chrome is installed and compatible with `webdriver_manager`. On macOS you may need to adjust `options.binary_location` for custom Chrome installs.
- **Tokenizers parallelism env var:** `routes.py` sets `os.environ["TOKENIZERS_PARALLELISM"] = "true"` — keep this if you rely on tokenizer behavior or adjust before tokenization.

## Editing guidelines for AI agents

- When editing inference code, preserve the global model/tokenizer initialization pattern in `ai_model.py`.
- For performance-sensitive changes, prefer batching multiple chunks in `predict_chunks` rather than calling the model per chunk.
- When modifying `file_utils.extract_text`, keep OCR fallback logic intact — scanned PDFs must still be supported.
- If touching `scrapper.py`, document Chrome path assumptions and test on macOS and Linux.

## Key files to inspect

- `routes.py` — HTTP endpoints, chunking, response shape, `export_pdf` behavior.
- `ai_model.py` — model/tokenizer initialization and `predict_chunks` contract.
- `file_utils.py` — file extension whitelist, OCR, and text extraction logic.
- `scrapper.py` — Selenium scraping; platform-specific Chrome path.
- `config.py` — `MODEL_NAME` and `ALLOWED_EXTENSIONS`.

## Quick notes for maintainers

- Large model downloads can take time; to speed up development set `MODEL_NAME` to a local/mini model or cache HF models.
- Running the scraper in CI or containers likely needs headful Chrome or Docker images with Chrome + proper display (or switch to requests-based scraping).

---

If any area is unclear (example: expected class order for `MODEL_NAME`, preferred non-GUI PDF export behavior, or target runtime environments), tell me which section to expand or correct.
