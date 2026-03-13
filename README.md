# AI Resume Analyzer

A full-stack AI app that analyzes PDF resumes and returns structured, frontend-ready insights.

## What This Project Does

Upload a resume PDF and get:

- Structured JSON analysis from AI
- ATS score meter data
- Skill gap detection with learning guidance
- Resume improvement suggestions with rewrite examples
- Career path recommendations with match scores and next steps

## Working Demo Flow

1. User uploads a resume PDF in the React UI.
2. Frontend sends `multipart/form-data` to FastAPI endpoint `/analyze-resume`.
3. Backend extracts text from PDF.
4. OpenAI returns JSON using a strict JSON schema.
5. Backend validates response with Pydantic models.
6. Frontend renders ATS meter, skill gaps, improvements, and career paths.

## Tech Stack

- Frontend: React 19 + TypeScript + Vite
- Backend: FastAPI + Pydantic
- AI: OpenAI Chat Completions
- PDF parsing: pypdf

## Requirements

- Python 3.11+ recommended
- Node.js 20+ recommended
- npm 10+ recommended
- OpenAI API key

## Environment Variables

Create `backend/.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Optional frontend env in `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If omitted, frontend defaults to `http://127.0.0.1:8000`.

## Installation

### 1) Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Frontend setup

```bash
cd frontend
npm install
```

## Run The Project

Open two terminals.

### Terminal A: Start backend

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### Terminal B: Start frontend

```bash
cd frontend
npm run dev
```

Frontend runs at: `http://localhost:5173`

## Verify It Is Working

- Open `http://localhost:5173`
- Upload a PDF resume
- Click **Analyze Resume**
- Confirm the UI renders:
  - ATS Score Meter
  - Strengths Snapshot
  - Skill Gap Detector
  - Resume Improvement Generator
  - Career Path Recommendation

You can also test backend health:

```bash
curl http://127.0.0.1:8000/
```

Expected:

```json
{"message":"AI Resume Analyzer API is running"}
```

## API Contract

### POST `/analyze-resume`

Request: `multipart/form-data`

- `file`: PDF resume file

Response shape:

```json
{
  "summary": "string",
  "ats_meter": {
    "score": 0,
    "label": "Poor | Fair | Good | Excellent",
    "color": "red | orange | yellow | green"
  },
  "strengths": ["string"],
  "skill_gaps": [
    {
      "skill": "string",
      "importance": "high | medium | low",
      "why_it_matters": "string",
      "how_to_learn": "string"
    }
  ],
  "resume_improvements": [
    {
      "section": "string",
      "issue": "string",
      "recommendation": "string",
      "example_rewrite": "string"
    }
  ],
  "career_paths": [
    {
      "role": "string",
      "match_score": 0,
      "rationale": "string",
      "next_steps": ["string"]
    }
  ]
}
```

## Project Structure

```text
ai-resume-analyzer/
  backend/
    app/
      config.py
      main.py
      resume_analyzer.py
      schemas.py
    requirements.txt
  frontend/
    src/
      App.tsx
      App.css
      index.css
```

## Notes

- CORS is enabled for local frontend origins (`localhost:5173` and `127.0.0.1:5173`).
- If analysis fails, check:
  - `OPENAI_API_KEY` exists in `backend/.env`
  - Backend dependencies are installed
  - Uploaded file is a valid PDF
