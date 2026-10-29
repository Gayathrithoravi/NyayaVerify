# NyayaVerify
LLM-based reasoning and logical verification inspired by Navya-Nyaya.

# NyayaVerify

NyayaVerify is an LLM-based reasoning and logical verification system inspired by Navya-Nyaya.

## Key Features

- Six-stage Nyaya-inspired reasoning pipeline
- Automatic structural validation of generated reasoning
- Formalization of natural-language conclusions
- Z3 SMT-based logical verification
- True, False, and Unknown classification
- Verifier-guided reasoning correction

## Project Structure

- `src/` — Reasoning pipeline, parsing, validation, and verification
- `frontend/` — Web user interface
- `evaluation/` — FOLIO evaluation scripts
- `training/` — Dataset preparation and training utilities
- `tests/` — Test scripts
- `data/` — Dataset files
- `models/` — Model configurations and tokenizer files
- `api.py` — API entry point

## Setup

Create and activate a Python virtual environment, then install dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the frontend from its directory:

```bash
cd frontend
npm install
npm run dev
```

Check `api.py` and the project configuration for the backend startup command.

## Verification

NyayaVerify uses Z3 to check formally encoded logical constraints. Verification depends on the correctness of the formal representation and does not guarantee that every generated natural-language explanation is correct.
