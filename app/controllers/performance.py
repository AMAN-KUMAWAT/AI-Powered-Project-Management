from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.employee import Employee
from app.models.performance import PerformanceMetric
from app.models.user import UserProfile

router = APIRouter()
templates = Jinja2Templates(directory="app/views")

@router.get("/performance")
async def performance_matrix(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    metrics = {m.employee_id: m for m in db.query(PerformanceMetric).all()}
    user = db.query(UserProfile).first()
    return templates.TemplateResponse("performance.html", {
        "request": request, 
        "employees": employees,
        "metrics": metrics,
        "user": user
    })
