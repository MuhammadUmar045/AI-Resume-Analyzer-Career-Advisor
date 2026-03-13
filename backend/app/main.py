"""Main FastAPI application entrypoint."""

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .resume_analyzer import analyze_resume, extract_text_from_pdf
from .schemas import ResumeAnalysisResponse


app = FastAPI(title="AI Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API is running"}


@app.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    try:
        resume_text = extract_text_from_pdf(file.file)
        return analyze_resume(resume_text)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc