from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.db import get_db, engine, seed_sample_data
from app.models.base import Base
from app.models.project import Project
from app.models.employee import Employee
from app.models.performance import PerformanceMetric
from app.models.user import UserProfile
from app.controllers import projects, performance, jira, backlog, user
import os

# Initialize database
Base.metadata.create_all(bind=engine)
seed_sample_data()

app = FastAPI(title="Smart AI PM Tool")

# Mount static files
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="app/views")

# Include routers
app.include_router(projects.router)
app.include_router(performance.router)
app.include_router(jira.router)
app.include_router(backlog.router)
app.include_router(user.router)

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    all_projects = db.query(Project).order_by(Project.created_at.desc()).all()
    top_performers = db.query(Employee).filter(Employee.performance_score >= 9.0).limit(5).all()
    user = db.query(UserProfile).first()
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "projects": all_projects,
        "top_performers": top_performers,
        "user": user
    })

@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(UserProfile).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("project_detail.html", {"request": request, "project": project, "user": user})

@app.get("/projects/{project_id}/backlog-editor", response_class=HTMLResponse)
async def backlog_editor(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(UserProfile).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("backlog_editor.html", {"request": request, "project": project, "user": user})

@app.get("/team", response_class=HTMLResponse)
async def team_view(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    user = db.query(UserProfile).first()
    return templates.TemplateResponse("team.html", {"request": request, "employees": employees, "user": user})

@app.get("/team/{employee_id}", response_class=HTMLResponse)
async def employee_detail(employee_id: int, request: Request, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    metric = db.query(PerformanceMetric).filter(PerformanceMetric.employee_id == employee_id).first()
    user = db.query(UserProfile).first()
    return templates.TemplateResponse("employee_detail.html", {
        "request": request, 
        "employee": employee, 
        "metric": metric,
        "user": user
    })

@app.get("/projects-list", response_class=HTMLResponse)
async def projects_list(request: Request, db: Session = Depends(get_db)):
    all_projects = db.query(Project).order_by(Project.created_at.desc()).all()
    user = db.query(UserProfile).first()
    return templates.TemplateResponse("projects_list.html", {"request": request, "projects": all_projects, "user": user})

@app.get("/backlog", response_class=HTMLResponse)
async def backlog_page(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    return templates.TemplateResponse("base.html", {"request": request, "user": user}) # Placeholder
