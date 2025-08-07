# README.md
# FarmDepot.ai Classified App

A multilingual AI-powered classified ads platform for agricultural products. Users can post, search, and register using voice commands in English, Hausa, Yoruba, and Igbo.

## Features
- Voice-enabled ad posting & search
- Multilingual support
- CrewAI agents with FastAPI backend
- Streamlit frontend with voice recording
- User registration and dashboard

## Project Structure
```
FarmDepot_ai/
├── backend/                # Backend agents & FastAPI API
│   ├── agents/            # AI agents for voice, post, search, etc.
│   ├── tasks/             # Agent tasks
│   ├── db/                # Database models
│   └── main.py            # FastAPI entrypoint
├── frontend/              # Streamlit frontend
│   └── app.py             # Streamlit app
├── static/audios/         # Uploaded voice files
├── templates/             # HTML templates (if needed)
├── requirements.txt       # Dependencies
├── Procfile               # Railway deployment
├── railway.json           # Railway config
└── README.md
```

## Setup Locally
1. Clone the repo:
```bash
git clone https://github.com/your-username/farmdepot_ai.git
cd agric-voice-classified
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
Create `.env` file in the root:
```
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-secret
```

5. Run backend:
```bash
uvicorn backend.main:app --reload
```

6. Run frontend:
```bash
streamlit run frontend/app.py
```

## Deploy to Railway
1. Push code to GitHub
2. Connect Railway to the repo
3. Add environment variables in Railway Dashboard
4. Click "Deploy"

## License
MIT
