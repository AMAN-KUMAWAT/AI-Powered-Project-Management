from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.project import Project
from app.models.backlog import BacklogItem
from pydantic import BaseModel
import json
import random

router = APIRouter()

class BacklogUpdate(BaseModel):
    items: list

@router.post("/projects/{project_id}/generate-backlog")
async def generate_backlog(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # ENHANCED SIMULATED AI OUTPUT (More Epics and Stories)
    epics = []
    epic_names = [
        f"Core {project.name} Architecture",
        "User Authentication & Security",
        "Dashboard & Data Visualization",
        "API Integration & Webhooks",
        "Performance Optimization",
        "Mobile Responsiveness",
        "Admin Control Panel",
        "Third-party Service Integration"
    ]
    
    # Pick 4-6 random epics from the list
    selected_epics = random.sample(epic_names, random.randint(4, 6))
    
    for i, epic_name in enumerate(selected_epics):
        stories = []
        # Generate 4-6 stories per epic
        num_stories = random.randint(4, 6)
        for j in range(num_stories):
            points = random.choice([1, 2, 3, 5, 8, 13])
            sprint = (i // 2) + 1 # Simple sprint assignment
            stories.append({
                "title": f"As a user, I want to {epic_name.lower()} feature part {j+1}",
                "points": points,
                "sprint": sprint
            })
        
        epics.append({
            "title": epic_name,
            "stories": stories
        })

    ai_output = {
        "epics": epics,
        "sprints": [8, 13, 21]
    }
    
    project.backlog_json = ai_output
    
    # NEW: Automatically save individual BacklogItem records upon generation
    # Clear any existing items first
    db.query(BacklogItem).filter(BacklogItem.project_id == project_id).delete()
    
    for epic in ai_output.get("epics", []):
        for story in epic.get("stories", []):
            item = BacklogItem(
                project_id=project_id,
                type="STORY",
                title=story.get("title"),
                description=f"Epic: {epic.get('title')}",
                story_points=story.get("points", 0),
                sprint_number=story.get("sprint", 1),
                status="To Do",
                priority="Medium"
            )
            db.add(item)
    
    project.status = "In Progress"
    db.commit()
    
    return ai_output

@router.get("/projects/{project_id}/backlog-data")
async def get_backlog_data(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.backlog_json or {"epics": [], "sprints": []}

@router.post("/projects/{project_id}/backlog/save-plan")
async def save_backlog_plan(project_id: int, data: dict, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.backlog_json = data
    
    # Clear old items and save new ones for granular tracking
    db.query(BacklogItem).filter(BacklogItem.project_id == project_id).delete()
    
    total_points = 0
    for epic in data.get("epics", []):
        for story in epic.get("stories", []):
            item = BacklogItem(
                project_id=project_id,
                type="STORY",
                title=story.get("title"),
                description=f"Epic: {epic.get('title')}",
                story_points=story.get("points", 0),
                sprint_number=story.get("sprint", 1),
                status="To Do"
            )
            total_points += story.get("points", 0)
            db.add(item)
    
    # Update project status if needed
    project.status = "In Progress"
    db.commit()
    return {"status": "success", "total_points": total_points}
