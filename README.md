# CareerCompass AI

A full-stack AI career assistant designed to help students and fresh graduates with:
- finding suitable internships/jobs
- identifying practical skill gaps
- choosing career paths
- building projects and learning roadmaps
- resume improvement
- interview preparation
- application tracking

## Stack
React + Vite | Python + FastAPI | SQLite | Optional OpenAI API

## Run
Backend:
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

If no OpenAI API key is configured, the app still works with built-in demo career advice.
