# SystemLens

AI-powered tool for analyzing enterprise systems, legacy code, and technical artifacts. Upload a document or paste a workflow to get structured analysis across five modes: Explain Artifact, Dependency Analysis, Change Impact Analysis, Onboarding Summary, and COBOL Breakdown.

---

## Project Structure

| Part | Path | Description |
|------|------|-------------|
| Streamlit app | `app.py` | Self-contained UI + API calls, deployable to Streamlit Cloud |
| FastAPI backend | `backend/api.py` | REST API exposing `POST /analyze`, deployable to Render |
| React frontend | `frontend/` | Dark-themed UI that calls the FastAPI backend, deployable to Vercel |

---

## One-Time Setup

```bash
git clone https://github.com/soumyapadhi/systemlenswithclaude.git
cd systemlenswithclaude
```

**Backend dependencies**
```bash
pip install -r requirements.txt
```

**Frontend dependencies**
```bash
cd frontend && npm install
```

---

## Run Locally

**Backend** (runs on port 8000):
```bash
ANTHROPIC_API_KEY=your-key python3 -m uvicorn backend.api:app --reload
```

**Frontend** (runs on port 3000, in a separate terminal):
```bash
cd frontend
REACT_APP_API_URL=http://localhost:8000 npm start
```

**Streamlit app** (standalone alternative, in a separate terminal):
```bash
# Add ANTHROPIC_API_KEY to .streamlit/secrets.toml first (see Environment Variables)
streamlit run app.py
```

---

## Deploy

### Backend → Render
1. Create a new **Web Service** and connect this repo
2. Set **Build Command**: `pip install -r requirements.txt`
3. Set **Start Command**: `python3 -m uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `ANTHROPIC_API_KEY`

### Frontend → Vercel
1. Import this repo, set **Root Directory** to `frontend`
2. Add environment variable: `REACT_APP_API_URL=https://your-render-service.onrender.com`
3. Deploy — Vercel auto-detects Create React App

### Streamlit app → Streamlit Cloud
1. Connect repo at [share.streamlit.io](https://share.streamlit.io)
2. Set **Main file path** to `app.py`
3. Add secret under **Advanced settings**: `ANTHROPIC_API_KEY = "your-key"`

---

## Environment Variables

| Variable | Where | Description |
|----------|-------|-------------|
| `ANTHROPIC_API_KEY` | Backend / Streamlit | Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com) |
| `REACT_APP_API_URL` | Frontend (build time) | Full URL of the FastAPI backend, e.g. `http://localhost:8000` |

For local Streamlit development, create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-key"
```

For local React development, create `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:8000
```
