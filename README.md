# EduGenie – Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant based on the supplied project documentation. It provides:

- Question answering
- Beginner-friendly concept explanation
- MCQ quiz generation
- Educational summarization
- Personalized learning paths

The project uses FastAPI for the backend and HTML/CSS/JavaScript for the web interface. Gemini handles the cloud generative-AI features. An optional LaMini-Flan-T5 local model is included for the explanation module.

## 1. Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── test_api.py
    └── test_modules.py
```

## 2. Prerequisites

Install Python 3.10 or newer.

Check:

```bash
python --version
```

If your computer uses `py` on Windows:

```bash
py --version
```

## 3. Open the project in VS Code

Open VS Code and select:

**File → Open Folder → EduGenie**

Open the integrated terminal:

**Terminal → New Terminal**

## 4. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Configure Gemini

Create a Gemini API key in Google AI Studio.

Copy `.env.example` and rename the copy to:

```text
.env
```

Then put your key in:

```text
GEMINI_API_KEY=your_real_key_here
```

Do not share the `.env` file or commit it to Git.

The current Google GenAI Python SDK is `google-genai`, and it reads `GEMINI_API_KEY` when configured through the environment. The project uses the same client pattern documented by Google.

## 7. Run EduGenie

From the project folder:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 8. Test the application

### Browser test

1. Select **Ask a Question**.
2. Click **Use Sample**.
3. Click **Generate**.
4. Try the other four tasks.

### Health check

Open:

```text
http://127.0.0.1:8000/health
```

You should see a JSON response similar to:

```json
{
  "status": "ok",
  "app": "EduGenie",
  "gemini_configured": true
}
```

### Automated tests

With the virtual environment active:

```bash
pytest
```

The tests mock Gemini responses, so they do not consume API calls.

## 9. Optional local LaMini explanation model

The supplied documentation specifies LaMini-Flan-T5-783M for concept explanation.

The default configuration keeps this disabled because downloading and running a 783M-parameter local model requires considerably more disk space and RAM than the cloud-only setup.

To enable it:

```bash
pip install -r requirements-local.txt
```

Then edit `.env`:

```text
USE_LOCAL_EXPLANATION=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

Restart the server.

If the local model cannot load, EduGenie automatically falls back to Gemini for the explanation request.

## 10. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/health` | Application health |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | MCQ generation |
| POST | `/summarize` | Text summarization |
| POST | `/learn/recommendations` | Learning path |

Example request:

```json
{
  "text": "Explain photosynthesis."
}
```

For `/quiz`:

```json
{
  "text": "Photosynthesis is the process by which green plants use light energy...",
  "count": 3
}
```

## 11. Troubleshooting

### `GEMINI_API_KEY is missing`

Make sure:

- the file is named exactly `.env`
- it is in the same folder as `main.py`
- the line is `GEMINI_API_KEY=...`
- the server was restarted after editing `.env`

### `ModuleNotFoundError`

Activate `.venv` and run:

```bash
pip install -r requirements.txt
```

### Port 8000 is already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open:

```text
http://127.0.0.1:8001
```

### Gemini model error

Change `GEMINI_MODEL` in `.env` to a text-generation model available to your Gemini API key.

## 12. Important submission note

Do not submit your real Gemini API key inside the project. Submit `.env.example` with a placeholder value instead.

For a college demonstration, create your own `.env` locally, run the application, and keep the API key private.
