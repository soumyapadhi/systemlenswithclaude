# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

SystemLens is a single-file Streamlit app (`app.py`) that uses the Anthropic API to analyze enterprise system artifacts — technical documents, architecture notes, and COBOL source files — and return structured AI-powered insights.

## Running the App

```bash
streamlit run app.py
```

## Dependencies

Install with pip:
```bash
pip install streamlit anthropic pypdf python-docx
```

## API Key Configuration

The app reads `ANTHROPIC_API_KEY` from Streamlit secrets. Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-key-here"
```

## Architecture

The entire application lives in `app.py` with no modules or packages. The structure is:

1. **CSS styling** — injected via `st.markdown(..., unsafe_allow_html=True)` for the dark theme UI
2. **Anthropic client** — initialized once using `st.secrets["ANTHROPIC_API_KEY"]`
3. **File extraction helpers** — `extract_text_from_pdf`, `extract_text_from_docx`, `extract_text_from_txt`, and the dispatcher `extract_artifact_text` (supports `.pdf`, `.docx`, `.txt`, `.cbl`, `.cob`, `.cpy`)
4. **UI layout** — hero section, feature cards, analysis mode selectbox, file uploader, text area, and question input
5. **AI logic** — on button click, builds a structured prompt by combining the analysis mode, artifact text, user question, and a mode-specific `mode_instruction` block, then calls `client.messages.create` with `claude-sonnet-4-5`

## Analysis Modes

Each mode injects a different `mode_instruction` into the prompt that specifies the exact numbered-section output format:

| Mode | Focus |
|------|-------|
| Explain Artifact | System summary, workflow, flow diagram, impact |
| Dependency Analysis | Upstream/downstream dependencies and risks |
| Change Impact Analysis | Impact areas, risks, testing recommendations |
| Onboarding Summary | Beginner-friendly explanation, suggested questions |
| COBOL Breakdown | Program purpose, logic flow, business rules, modernization suggestions |

## Model

The app uses `claude-sonnet-4-5` with `max_tokens=4096`. The system prompt positions Claude as a senior enterprise systems analyst.
