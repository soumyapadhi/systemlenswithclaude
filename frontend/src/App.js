import React, { useRef, useState } from 'react';
import { marked } from 'marked';
import './App.css';

const ANALYSIS_MODES = [
  'Explain Artifact',
  'Dependency Analysis',
  'Change Impact Analysis',
  'Onboarding Summary',
  'COBOL Breakdown',
];

const ACCEPTED_EXTENSIONS = '.cbl,.cob,.jcl,.job,.txt,.cpy,.pdf,.docx';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function App() {
  const [analysisMode, setAnalysisMode] = useState(ANALYSIS_MODES[0]);
  const [artifact, setArtifact] = useState('');
  const [question, setQuestion] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [resultMode, setResultMode] = useState('');
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  function handleFileChange(e) {
    const selected = e.target.files[0] || null;
    setFile(selected);
  }

  function clearFile() {
    setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setResult(null);

    if (!file && !artifact.trim()) {
      setError('Please upload a file or paste an artifact.');
      return;
    }
    if (!question.trim()) {
      setError('Please enter a question.');
      return;
    }

    const formData = new FormData();
    formData.append('analysis_mode', analysisMode);
    formData.append('question', question);
    formData.append('artifact', artifact);
    if (file) formData.append('file', file);

    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();

      if (data.error) {
        setError(data.error);
      } else {
        setResult(data.result);
        setResultMode(data.analysis_mode);
      }
    } catch (err) {
      setError(err.message || 'Something went wrong. Is the API server running?');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      {/* ── Hero ── */}
      <div className="hero">
        <div className="hero-topline">AI Product Prototype • Enterprise Systems • Legacy Modernization</div>
        <h1 className="hero-title">
          🔎 <span className="hero-highlight">SystemLens</span>
        </h1>
        <p className="hero-description">
          Understand enterprise systems, technical artifacts, and legacy code faster.
          Upload a document or paste a workflow to analyze dependencies, assess release impact,
          generate onboarding summaries, and break down COBOL logic into business-readable explanations.
        </p>
        <div className="hero-badges">
          {['Explain Artifacts', 'Trace Dependencies', 'Assess Change Impact', 'Onboarding Summaries', 'COBOL Breakdown'].map(b => (
            <span key={b} className="hero-badge">{b}</span>
          ))}
        </div>
        <p className="hero-footer-note">
          Designed to help engineers, TPMs, PMs, and modernization teams make sense of complex systems.
        </p>
      </div>

      {/* ── Feature cards ── */}
      <div className="feature-grid">
        <div className="feature-card">
          <div className="feature-card-title">⚙️ Explain Systems</div>
          <div className="feature-card-text">Turn technical artifacts into clear system and workflow understanding.</div>
        </div>
        <div className="feature-card">
          <div className="feature-card-title">🔗 Trace Dependencies</div>
          <div className="feature-card-text">Surface upstream and downstream connections before making changes.</div>
        </div>
        <div className="feature-card">
          <div className="feature-card-title">🧠 Decode Legacy Logic</div>
          <div className="feature-card-text">Translate COBOL and legacy flows into business-readable explanations.</div>
        </div>
      </div>

      <hr className="divider" />

      {/* ── Form ── */}
      <form className="form-section" onSubmit={handleSubmit}>
        {/* Analysis mode */}
        <div>
          <label htmlFor="mode">🔍 Choose analysis mode</label>
          <select
            id="mode"
            value={analysisMode}
            onChange={e => setAnalysisMode(e.target.value)}
          >
            {ANALYSIS_MODES.map(m => (
              <option key={m} value={m}>{m}</option>
            ))}
          </select>
        </div>

        {/* File upload */}
        <div>
          <label>Upload a file</label>
          <div className="file-upload-area">
            <label className="file-upload-label" htmlFor="file-input">
              <span className="file-upload-icon">📂</span>
              <span className="file-upload-text">Click to browse or drag and drop</span>
              <span className="file-upload-hint">PDF, DOCX, TXT, CBL, COB, CPY, JCL, JOB</span>
              <input
                id="file-input"
                ref={fileInputRef}
                type="file"
                accept={ACCEPTED_EXTENSIONS}
                onChange={handleFileChange}
              />
            </label>
            {file && (
              <div className="file-selected">
                📄 {file.name}
                <button
                  type="button"
                  className="file-clear-btn"
                  onClick={clearFile}
                  aria-label="Remove file"
                >
                  ✕
                </button>
              </div>
            )}
          </div>
          <p className="small-note">Best results with text-based PDFs, DOCX files, and structured technical documents.</p>
        </div>

        {/* Artifact paste */}
        <div>
          <label htmlFor="artifact">Or paste code, architecture notes, API documentation, or process notes</label>
          <textarea
            id="artifact"
            value={artifact}
            onChange={e => setArtifact(e.target.value)}
            placeholder="Paste a workflow, architecture note, service interaction, requirement document excerpt, or process description here..."
          />
        </div>

        {/* Question */}
        <div>
          <label htmlFor="question">Ask a question</label>
          <input
            id="question"
            type="text"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="Example: Give me a beginner-friendly summary of this flow"
          />
        </div>

        <button className="run-btn" type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Run Analysis'}
        </button>
      </form>

      {/* ── Loading ── */}
      {loading && (
        <div className="spinner-wrapper">
          <div className="spinner" />
          Analyzing artifact...
        </div>
      )}

      {/* ── Error ── */}
      {error && <div className="error-box">⚠️ {error}</div>}

      {/* ── Results ── */}
      {result && (
        <div className="results-section">
          <div className="results-heading">AI Output — {resultMode}</div>
          <div
            className="results-body"
            dangerouslySetInnerHTML={{ __html: marked(result) }}
          />
        </div>
      )}
    </div>
  );
}
