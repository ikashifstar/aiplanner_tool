# AI Planner Tool

This repository contains two main entrypoints:

- A **video generation pipeline** exposed via the CLI in `src/cli.py` that validates metadata, builds a stub script/scene plan, and assembles placeholder media artifacts.
- A **Gradio-based trip planner UI** in `app.py` that calls the Groq API to generate travel plans.

## Setup
1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Trip planner only) Export your Groq API key:
   ```bash
   export GROQ_API_KEY=<your_key>
   ```

## Running the video pipeline CLI
Invoke the CLI with required metadata arguments. The pipeline writes placeholder outputs to the provided `--output-dir` and reports the final video path.
```bash
python -m src.cli \
  --title "Sample Video" \
  --resolution 1080p \
  --duration 120 \
  --video-type explainer \
  --output-dir output
```

## Running the trip planner UI
Launch the Gradio interface (requires the Groq API key):
```bash
python app.py
```
A local URL will be printed in the terminal for interacting with the UI.

## Tests
Run the unit test suite:
```bash
pytest
```
