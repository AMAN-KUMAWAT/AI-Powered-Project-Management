from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.employee import Employee
from app.models.performance import PerformanceMetric
from app.models.user import UserProfile

router = APIRouter()
from app.views import templates

from datetime import datetime, timedelta

@router.get("/performance")
async def performance_matrix(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    metrics = {m.employee_id: m for m in db.query(PerformanceMetric).all()}
    user = db.query(UserProfile).first()
    
    # Notifications logic
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    notifications = db.query(Employee).filter(
        Employee.is_assigned == 0,
        Employee.free_since <= one_day_ago
    ).all()

    return templates.TemplateResponse("performance.html", {
        "request": request, 
        "employees": employees,
        "metrics": metrics,
        "user": user,
        "notifications": notifications
    })
