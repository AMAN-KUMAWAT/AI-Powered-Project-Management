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
from app.controllers import projects, performance, jira, backlog, user, code_gen
import os
from datetime import datetime, timedelta

# Initialize database
Base.metadata.create_all(bind=engine)
seed_sample_data()

app = FastAPI(title="Smart AI PM Tool")

# Mount static files
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="app/views")

def get_notifications(db: Session):
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    return db.query(Employee).filter(
        Employee.is_assigned == 0,
        Employee.free_since <= one_day_ago
    ).all()

# Include routers
app.include_router(projects.router)
app.include_router(performance.router)
app.include_router(jira.router)
app.include_router(backlog.router)
app.include_router(user.router)
app.include_router(code_gen.router)

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    all_projects = db.query(Project).order_by(Project.created_at.desc()).all()
    top_performers = db.query(Employee).filter(Employee.performance_score >= 9.0).limit(5).all()
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)

    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "projects": all_projects,
        "top_performers": top_performers,
        "user": user,
        "notifications": notifications
    })

@app.get("/notifications", response_class=HTMLResponse)
async def notifications_view(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    idle_employees = get_notifications(db)
    
    return templates.TemplateResponse("notifications.html", {
        "request": request, 
        "user": user,
        "idle_employees": idle_employees,
        "notifications": idle_employees
    })

@app.get("/resource-planning", response_class=HTMLResponse)
async def resource_planning(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    
    # Employees on notice
    on_notice = db.query(Employee).filter(Employee.is_on_notice == True).all()
    all_employees = db.query(Employee).all()
    
    notice_data = []
    for emp in on_notice:
        days_left = (emp.notice_end_date - datetime.utcnow()).days if emp.notice_end_date else 0
        
        # Find replacements based on skills and role
        replacements = []
        emp_skills = set([s.strip().lower() for s in emp.skills.split(",") if s.strip()])
        
        for candidate in all_employees:
            if candidate.id == emp.id or candidate.is_on_notice:
                continue
            
            # Check role match and skill overlap
            if candidate.role == emp.role or "Senior" in candidate.role or emp.role in candidate.role:
                cand_skills = set([s.strip().lower() for s in candidate.skills.split(",") if s.strip()])
                overlap = emp_skills.intersection(cand_skills)
                
                if overlap:
                    match_percent = (len(overlap) / len(emp_skills)) * 100 if emp_skills else 0
                    replacements.append({
                        "id": candidate.id,
                        "name": candidate.name,
                        "match_score": round(match_percent, 1),
                        "shared_skills": list(overlap)
                    })
        
        # Sort replacements by match score
        replacements.sort(key=lambda x: x['match_score'], reverse=True)
        
        notice_data.append({
            "employee": emp,
            "days_left": max(0, days_left),
            "replacements": replacements[:3], # Top 3 replacements
            "should_hire": len(replacements) == 0
        })
    
    return templates.TemplateResponse("resource_planning.html", {
        "request": request, 
        "user": user,
        "notifications": notifications,
        "notice_data": notice_data
    })

@app.get("/team-dashboard", response_class=HTMLResponse)
async def team_dashboard(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    employees = db.query(Employee).all()
    # Fetch unassigned stories
    unassigned_stories = db.query(BacklogItem).filter(BacklogItem.assigned_to == None, BacklogItem.type == "STORY").all()
    # Fetch assigned stories grouped by employee
    assignments = {}
    for emp in employees:
        assignments[emp.id] = db.query(BacklogItem).filter(BacklogItem.assigned_to == emp.id).all()
    
    return templates.TemplateResponse("team_dashboard.html", {
        "request": request, 
        "user": user, 
        "notifications": notifications,
        "employees": employees,
        "unassigned_stories": unassigned_stories,
        "assignments": assignments
    })

@app.post("/auto-assign")
async def auto_assign(db: Session = Depends(get_db)):
    stories = db.query(BacklogItem).filter(BacklogItem.assigned_to == None, BacklogItem.type == "STORY").all()
    employees = db.query(Employee).filter(Employee.is_assigned == 0).all()
    
    if not employees or not stories:
        return {"status": "no_work_or_resources"}
    
    assigned_count = 0
    for story in stories:
        # Simple AI heuristic: Match role and skill
        for emp in employees:
            if "Dev" in emp.role and "React" in emp.skills and ("UI" in story.title or "Design" in story.title):
                story.assigned_to = emp.id
                emp.is_assigned = 1
                emp.assigned_task = story.title
                assigned_count += 1
                employees.remove(emp) # Prevent over-allocation in this simple simulation
                break
            elif "Dev" in emp.role and "Python" in emp.skills and ("Logic" in story.title or "API" in story.title):
                story.assigned_to = emp.id
                emp.is_assigned = 1
                emp.assigned_task = story.title
                assigned_count += 1
                employees.remove(emp)
                break
    
    db.commit()
    return {"status": "success", "count": assigned_count}

@app.get("/code-hub", response_class=HTMLResponse)
async def code_hub(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    projects = db.query(Project).all()
    return templates.TemplateResponse("code_hub.html", {
        "request": request, 
        "user": user, 
        "notifications": notifications,
        "projects": projects
    })

@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("project_detail.html", {
        "request": request, 
        "project": project, 
        "user": user,
        "notifications": notifications
    })

@app.get("/projects/{project_id}/backlog-editor", response_class=HTMLResponse)
async def backlog_editor(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("backlog_editor.html", {
        "request": request, 
        "project": project, 
        "user": user,
        "notifications": notifications
    })

@app.get("/projects/{project_id}/code-gen", response_class=HTMLResponse)
async def code_generator_view(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("code_generator.html", {
        "request": request, 
        "project": project, 
        "user": user,
        "notifications": notifications
    })

@app.get("/projects/{project_id}/items/{item_type}/{epic_idx}", response_class=HTMLResponse)
@app.get("/projects/{project_id}/items/{item_type}/{epic_idx}/{story_idx}", response_class=HTMLResponse)
async def backlog_item_detail(project_id: int, item_type: str, epic_idx: int, request: Request, story_idx: int = None, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    if not project or not project.backlog_json:
        raise HTTPException(status_code=404, detail="Item not found")
    
    try:
        epic = project.backlog_json['epics'][epic_idx]
        if item_type == 'epic':
            item = {"title": epic['title'], "description": f"Main Epic: {epic['title']}", "points": None}
        else:
            story = epic['stories'][story_idx]
            item = {"title": story['title'], "description": f"User Story under {epic['title']}", "points": story['points'], "sprint": story['sprint']}
    except (IndexError, KeyError):
        raise HTTPException(status_code=404, detail="Item index out of range")

    return templates.TemplateResponse("backlog_item_view.html", {
        "request": request, 
        "project": project, 
        "item": item, 
        "item_type": item_type,
        "user": user,
        "notifications": notifications
    })

@app.get("/team", response_class=HTMLResponse)
async def team_view(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    return templates.TemplateResponse("team.html", {
        "request": request, 
        "employees": employees, 
        "user": user,
        "notifications": notifications
    })

@app.get("/team/{employee_id}", response_class=HTMLResponse)
async def employee_detail(employee_id: int, request: Request, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    metric = db.query(PerformanceMetric).filter(PerformanceMetric.employee_id == employee_id).first()
    user = db.query(UserProfile).first()
    all_projects = db.query(Project).all()
    notifications = get_notifications(db)
    return templates.TemplateResponse("employee_detail.html", {
        "request": request, 
        "employee": employee, 
        "metric": metric, 
        "user": user,
        "projects": all_projects,
        "notifications": notifications
    })

@app.post("/team/{employee_id}/assign-task")
async def assign_task(employee_id: int, data: dict, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    task_name = data.get("task_name")
    employee.is_assigned = 1
    employee.assigned_task = task_name
    employee.free_since = None
    db.commit()
    return {"status": "success", "task": task_name}

@app.post("/team/{employee_id}/unassign-task")
async def unassign_task(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.is_assigned = 0
    employee.assigned_task = None
    employee.free_since = datetime.utcnow()
    db.commit()
    return {"status": "success"}

@app.get("/projects-list", response_class=HTMLResponse)
async def projects_list(request: Request, db: Session = Depends(get_db)):
    all_projects = db.query(Project).order_by(Project.created_at.desc()).all()
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    return templates.TemplateResponse("projects_list.html", {
        "request": request, 
        "projects": all_projects, 
        "user": user,
        "notifications": notifications
    })

@app.get("/backlog", response_class=HTMLResponse)
async def backlog_page(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    notifications = get_notifications(db)
    return templates.TemplateResponse("base.html", {
        "request": request, 
        "user": user,
        "notifications": notifications
    })
