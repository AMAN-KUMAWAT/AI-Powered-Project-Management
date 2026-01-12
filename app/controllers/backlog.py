from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.project import Project
from app.models.backlog import BacklogItem
from pydantic import BaseModel
import json
import random

from app.views import templates

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
    # Realistic Story Mapping based on Epic Names
    story_templates = {
        "Core SaaS HR Platform Architecture": [
            "Initialize multi-tenant database schema",
            "Setup centralized logging and monitoring",
            "Implement base repository pattern",
            "Configure environment-specific secrets",
            "Deploy infrastructure as code"
        ],
        "User Authentication & Security": [
            "Integrate OAuth2 with Google/Microsoft",
            "Implement multi-factor authentication",
            "Create password reset workflow",
            "Setup JWT token rotation",
            "Audit log for security events"
        ],
        "Dashboard & Data Visualization": [
            "Real-time analytics widget for HR",
            "Custom report builder for managers",
            "Interactive employee growth chart",
            "Departmental budget heatmap",
            "Export dashboard as PDF/CSV"
        ],
        "API Integration & Webhooks": [
            "External API gateway for partners",
            "Webhook triggers for payroll events",
            "Integration with Slack notifications",
            "Sync employee data with ERP",
            "Public API documentation portal"
        ],
        "Performance Optimization": [
            "Cache frequent database queries",
            "Optimize image asset delivery",
            "Implement database indexing",
            "Lazy load heavy UI components",
            "Reduce bundle size for mobile"
        ],
        "Mobile Responsiveness": [
            "PWA support for offline access",
            "Adaptive sidebar for small screens",
            "Touch-friendly data grids",
            "Native push notification support",
            "Optimize mobile checkout flow"
        ],
        "Admin Control Panel": [
            "Role-based access control (RBAC)",
            "Organization settings management",
            "Global system health monitor",
            "Manage enterprise license keys",
            "Bulk user import via CSV"
        ],
        "Third-party Service Integration": [
            "Salesforce CRM data sync",
            "Stripe payment gateway setup",
            "AWS S3 bucket for uploads",
            "SendGrid email template engine",
            "GitHub CI/CD pipeline integration"
        ],
        "Ecommerce Mobile App": [
            "Product catalog search & filters",
            "Shopping cart persistent state",
            "Secure checkout with Apple Pay",
            "Order tracking real-time status",
            "User product reviews system"
        ],
        "AI Customer Chatbot": [
            "Train NLP model with FAQ data",
            "Live chat handover to human agent",
            "Sentiment analysis for support",
            "Intelligent auto-reply bot",
            "Voice-to-text input support"
        ]
    }

    selected_epics = random.sample(epic_names, random.randint(4, 6))
    
    for i, epic_name in enumerate(selected_epics):
        stories = []
        # Get specific templates if available, otherwise use generic realistic names
        templates = story_templates.get(epic_name, [
            f"Implement core logic for {epic_name}",
            f"Unit test {epic_name} modules",
            f"Documentation for {epic_name}",
            f"Frontend wiring for {epic_name}",
            f"Edge case handling in {epic_name}"
        ])
        
        # Pick 4-6 stories per epic
        num_stories = random.randint(min(4, len(templates)), min(6, len(templates)))
        chosen_stories = random.sample(templates, num_stories)
        
        for j, story_title in enumerate(chosen_stories):
            points = random.choice([1, 2, 3, 5, 8, 13])
            sprint = (i // 2) + 1 # Simple sprint assignment
            stories.append({
                "title": story_title,
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
