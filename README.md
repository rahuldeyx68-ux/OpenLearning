# OpenLearning

## Overview

OpenLearning is a Flask-based web project that provides an educational math experience with interactive tools and an AI-powered math tutor.

## Features

- Home page with navigation to services
- Graphing tool page
- Geometry viewer page
- Calculator page
- AI chat page for math assistance via `/chat`

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Add your API keys in a `.env` file next to `api.py`:
   - `HF_TOKEN` or `NVIDIA_API_KEY` or `GEMINI_API_KEY`
   - `DESMOS_API_KEY`
3. Start the Flask server:
   ```bash
   python api.py
   ```
4. Open the browser at:
   ```
   http://127.0.0.1:5000/
   ```

## Important Routes

- `/` — Main index page
- `/graph` — Graphing tool
- `/geometry` — Geometry viewer
- `/cal` — Calculator
- `/ai` — AI chat interface
- `/chat` — AI chat backend endpoint

## Notes

- `ai_chat.html` is served by the `/ai` route and uses the `/chat` endpoint.
- The index page links now point to Flask routes instead of direct HTML file access.
- Make sure the `.env` file is present and keys are loaded correctly.
