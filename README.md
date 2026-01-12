# 🚀 Smart AI PM Tool (MVC Hackathon MVP)

Modern, AI-powered project management tool with a strict MVC architecture for scalability.

## 🛠️ MVC Architecture
- **Model (app/models):** SQLAlchemy models for database structure.
- **View (app/views):** Jinja2 templates for the modern glassmorphism UI.
- **Controller (app/controllers):** FastAPI routes handling logic and data flow.

## ⚡ Quick Start (Windows)
1. Double-click `start.bat`
2. Access Site from here:- https://ai-powered-project-management-2.onrender.com/profile
3. Open [http://localhost:8000](http://localhost:8000) in your browser.

## ⚡ Quick Start (Manual)
```bash
python run.py
```

## 📂 Project Structure
```text
smart-ai-pm/
├── README.md                 # Demo instructions
├── PROMPT_LOG.md            # Hackathon proof
├── .env.example             # API keys template
├── run.py                   # ONE-CLICK START
├── start.bat                # Windows demo
├── app/
│   ├── models/              # MODEL: SQLAlchemy schemas
│   ├── views/               # VIEW: Jinja2 templates
│   ├── controllers/         # CONTROLLER: FastAPI routes
│   └── db.py                # Database session
└── data/
    └── smart_pm.db          # SQLite auto-created
```

## ✨ Features
- **Strict MVC Separation:** Scalable and clean codebase.
- **Modern Dashboard:** Glassmorphism UI with Tailwind & Lucide.
- **Project CRUD:** Create and delete projects with instant feedback.
- **Responsive:** Mobile-first design.
- **One-Click Setup:** Auto-installs dependencies.

## 📝 License
MIT
