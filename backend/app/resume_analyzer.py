"""Resume parsing and AI analysis helpers."""

import json

try:
    from openai import OpenAI
except ModuleNotFoundError:
    OpenAI = None

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    PdfReader = None

from .config import OPENAI_API_KEY
from .schemas import ResumeAnalysisResponse


def _get_client():
    if OpenAI is None:
        raise RuntimeError("Missing dependency: install 'openai' to analyze resumes.")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to your .env file.")
    return OpenAI(api_key=OPENAI_API_KEY)


def extract_text_from_pdf(file):
    """Extract concatenated text from all pages in an uploaded PDF file."""
    if PdfReader is None:
        raise RuntimeError("Missing dependency: install 'pypdf' to parse PDF files.")

    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def _analysis_json_schema():
    return {
        "name": "resume_analysis",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "summary": {"type": "string"},
                "ats_meter": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "score": {"type": "integer", "minimum": 0, "maximum": 100},
                        "label": {
                            "type": "string",
                            "enum": ["Poor", "Fair", "Good", "Excellent"],
                        },
                        "color": {
                            "type": "string",
                            "enum": ["red", "orange", "yellow", "green"],
                        },
                    },
                    "required": ["score", "label", "color"],
                },
                "strengths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                },
                "skill_gaps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "skill": {"type": "string"},
                            "importance": {
                                "type": "string",
                                "enum": ["high", "medium", "low"],
                            },
                            "why_it_matters": {"type": "string"},
                            "how_to_learn": {"type": "string"},
                        },
                        "required": [
                            "skill",
                            "importance",
                            "why_it_matters",
                            "how_to_learn",
                        ],
                    },
                },
                "resume_improvements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "section": {"type": "string"},
                            "issue": {"type": "string"},
                            "recommendation": {"type": "string"},
                            "example_rewrite": {"type": "string"},
                        },
                        "required": [
                            "section",
                            "issue",
                            "recommendation",
                            "example_rewrite",
                        ],
                    },
                },
                "career_paths": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "role": {"type": "string"},
                            "match_score": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100,
                            },
                            "rationale": {"type": "string"},
                            "next_steps": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                            },
                        },
                        "required": [
                            "role",
                            "match_score",
                            "rationale",
                            "next_steps",
                        ],
                    },
                    "minItems": 3,
                },
            },
            "required": [
                "summary",
                "ats_meter",
                "strengths",
                "skill_gaps",
                "resume_improvements",
                "career_paths",
            ],
        },
    }


def analyze_resume(resume_text):
    """Analyze resume content and return typed structured insights."""
    client = _get_client()
    if not resume_text:
        raise RuntimeError("No extractable text found in the uploaded PDF.")

    prompt = f"""
Analyze this resume and produce a professional, realistic evaluation.
Return only data according to the provided JSON schema.

Rules:
- ATS score must be 0-100.
- strengths should be concise bullet-like statements.
- skill_gaps should include practical learning advice.
- resume_improvements should include concrete rewrites.
- career_paths should contain 3-5 suitable roles.

Resume text:
{resume_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a senior recruiter and ATS optimization expert.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_schema", "json_schema": _analysis_json_schema()},
        temperature=0.3,
    )

    raw_content = response.choices[0].message.content
    payload = json.loads(raw_content)
    return ResumeAnalysisResponse.model_validate(payload)