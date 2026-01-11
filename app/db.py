from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.project import Project
from app.models.employee import Employee
from app.models.performance import PerformanceMetric
from app.models.backlog import BacklogItem
from app.models.user import UserProfile
import os

DATABASE_URL = "sqlite:///./data/smart_pm.db"
os.makedirs("./data", exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_sample_data():
    db = SessionLocal()
    # Check if already seeded
    if db.query(Project).first():
        db.close()
        return

    # Seed Projects
    p1 = Project(name="SaaS HR Platform", description="Cloud-based HR management system for SMEs.", priority="High")
    p2 = Project(name="Ecommerce Mobile App", description="Native iOS/Android app for fashion retail.", priority="Medium")
    p3 = Project(name="AI Customer Chatbot", description="NLP-powered support automation for enterprise.", priority="High")
    db.add_all([p1, p2, p3])
    db.commit()

    # Seed Employees
    employees = [
        Employee(name="John Doe", role="Dev", performance_score=9.2),
        Employee(name="Sarah Connor", role="QA", performance_score=8.7),
        Employee(name="Mike Ross", role="PM", performance_score=9.5),
        Employee(name="Harvey Specter", role="Senior Dev", performance_score=9.8),
        Employee(name="Donna Paulsen", role="QA Lead", performance_score=9.4),
        Employee(name="Louis Litt", role="Dev", performance_score=7.8),
        Employee(name="Rachel Zane", role="Designer", performance_score=8.9),
        Employee(name="Jessica Pearson", role="Director", performance_score=9.9),
    ]
    db.add_all(employees)
    db.commit()

    # Seed Performance Metrics
    for emp in employees:
        metric = PerformanceMetric(
            employee_id=emp.id,
            velocity=12.5 if "Dev" in emp.role else 0,
            completion_rate=95.0 if emp.performance_score > 9.0 else 85.0,
            skills="Python, React, AWS" if "Dev" in emp.role else "Agile, Jira, Strategy",
            promotion_ready="Yes" if emp.performance_score >= 9.5 else "No"
        )
        db.add(metric)
    
    # Seed Backlog
    b1 = BacklogItem(title="Setup OAuth2", description="Implement secure login flow", status="Done", priority="High", project_id=p1.id)
    b2 = BacklogItem(title="Design Homepage", description="Create UI mockups for mobile", status="In Progress", priority="Medium", project_id=p2.id)
    db.add_all([b1, b2])
    
    # Seed Default User Profile
    if not db.query(UserProfile).first():
        default_user = UserProfile(
            name="Aman Kumawat",
            email="aman@example.com",
            bio="Product Manager & AI Enthusiast",
            theme="dark"
        )
        db.add(default_user)
    
    db.commit()
    db.close()
    print("Sample data seeded successfully!")
