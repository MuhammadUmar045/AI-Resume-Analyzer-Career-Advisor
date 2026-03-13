import { ChangeEvent, FormEvent, useMemo, useState } from 'react'
import './App.css'

type Importance = 'high' | 'medium' | 'low'

type AtsMeter = {
  score: number
  label: 'Poor' | 'Fair' | 'Good' | 'Excellent'
  color: 'red' | 'orange' | 'yellow' | 'green'
}

type SkillGapItem = {
  skill: string
  importance: Importance
  why_it_matters: string
  how_to_learn: string
}

type ResumeImprovementItem = {
  section: string
  issue: string
  recommendation: string
  example_rewrite: string
}

type CareerPathItem = {
  role: string
  match_score: number
  rationale: string
  next_steps: string[]
}

type ResumeAnalysisResponse = {
  summary: string
  ats_meter: AtsMeter
  strengths: string[]
  skill_gaps: SkillGapItem[]
  resume_improvements: ResumeImprovementItem[]
  career_paths: CareerPathItem[]
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

const meterColorClass: Record<AtsMeter['color'], string> = {
  red: 'meter-red',
  orange: 'meter-orange',
  yellow: 'meter-yellow',
  green: 'meter-green',
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<ResumeAnalysisResponse | null>(null)

  const meterStyle = useMemo(() => {
    const score = analysis?.ats_meter.score ?? 0
    return {
      background: `conic-gradient(var(--meter-fill) ${score * 3.6}deg, var(--meter-track) ${score * 3.6}deg 360deg)`,
    }
  }, [analysis])

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null
    setSelectedFile(file)
    setError(null)
  }

  const handleAnalyze = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!selectedFile) {
      setError('Please select a PDF resume first.')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/analyze-resume`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as
          | { detail?: string }
          | null
        throw new Error(payload?.detail ?? 'Analysis request failed.')
      }

      const payload = (await response.json()) as ResumeAnalysisResponse
      setAnalysis(payload)
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : 'Unexpected error while analyzing resume.'
      setError(message)
      setAnalysis(null)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-panel">
        <p className="eyebrow">AI Resume Analyzer</p>
        <h1>From Resume To Career Strategy In One Upload</h1>
        <p className="intro-copy">
          Get ATS scoring, skill-gap diagnostics, rewrite-ready improvements, and
          role recommendations in a structured report your frontend can render cleanly.
        </p>
        <form className="upload-form" onSubmit={handleAnalyze}>
          <label className="file-picker" htmlFor="resume-file">
            <span>{selectedFile ? selectedFile.name : 'Choose resume PDF'}</span>
            <input
              id="resume-file"
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
            />
          </label>
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
        </form>
        {error ? <p className="error-banner">{error}</p> : null}
      </section>

      {analysis ? (
        <section className="results-grid">
          <article className="panel summary-panel">
            <h2>Executive Summary</h2>
            <p>{analysis.summary}</p>
          </article>

          <article className="panel ats-panel">
            <h2>ATS Score Meter</h2>
            <div className={`meter-ring ${meterColorClass[analysis.ats_meter.color]}`} style={meterStyle}>
              <div className="meter-core">
                <strong>{analysis.ats_meter.score}</strong>
                <span>{analysis.ats_meter.label}</span>
              </div>
            </div>
          </article>

          <article className="panel strengths-panel">
            <h2>Strengths Snapshot</h2>
            <ul>
              {analysis.strengths.map((strength) => (
                <li key={strength}>{strength}</li>
              ))}
            </ul>
          </article>

          <article className="panel skill-gap-panel">
            <h2>Skill Gap Detector</h2>
            <div className="stack-list">
              {analysis.skill_gaps.map((item) => (
                <section key={item.skill} className="tile">
                  <header>
                    <h3>{item.skill}</h3>
                    <span className={`importance-pill importance-${item.importance}`}>
                      {item.importance}
                    </span>
                  </header>
                  <p>{item.why_it_matters}</p>
                  <p className="learn-path">How to learn: {item.how_to_learn}</p>
                </section>
              ))}
            </div>
          </article>

          <article className="panel improvements-panel">
            <h2>Resume Improvement Generator</h2>
            <div className="stack-list">
              {analysis.resume_improvements.map((item, index) => (
                <section key={`${item.section}-${index}`} className="tile">
                  <h3>{item.section}</h3>
                  <p><strong>Issue:</strong> {item.issue}</p>
                  <p><strong>Recommendation:</strong> {item.recommendation}</p>
                  <blockquote>{item.example_rewrite}</blockquote>
                </section>
              ))}
            </div>
          </article>

          <article className="panel career-panel">
            <h2>Career Path Recommendation</h2>
            <div className="career-grid">
              {analysis.career_paths.map((path) => (
                <section key={path.role} className="career-card">
                  <header>
                    <h3>{path.role}</h3>
                    <span>{path.match_score}% match</span>
                  </header>
                  <p>{path.rationale}</p>
                  <ul>
                    {path.next_steps.map((step) => (
                      <li key={step}>{step}</li>
                    ))}
                  </ul>
                </section>
              ))}
            </div>
          </article>
        </section>
      ) : (
        <section className="empty-state panel">
          <h2>Upload a resume to generate insights</h2>
          <p>
            Your structured report will appear here with ATS meter, skill gaps,
            improvements, and career recommendations.
          </p>
        </section>
      )}
    </main>
  )
}

export default App
