"""Pydantic schemas for structured resume analysis responses."""

from typing import List, Literal

from pydantic import BaseModel, Field


class AtsMeter(BaseModel):
    score: int = Field(..., ge=0, le=100)
    label: Literal["Poor", "Fair", "Good", "Excellent"]
    color: Literal["red", "orange", "yellow", "green"]


class SkillGapItem(BaseModel):
    skill: str
    importance: Literal["high", "medium", "low"]
    why_it_matters: str
    how_to_learn: str


class ResumeImprovementItem(BaseModel):
    section: str
    issue: str
    recommendation: str
    example_rewrite: str


class CareerPathItem(BaseModel):
    role: str
    match_score: int = Field(..., ge=0, le=100)
    rationale: str
    next_steps: List[str]


class ResumeAnalysisResponse(BaseModel):
    summary: str
    ats_meter: AtsMeter
    strengths: List[str]
    skill_gaps: List[SkillGapItem]
    resume_improvements: List[ResumeImprovementItem]
    career_paths: List[CareerPathItem]
