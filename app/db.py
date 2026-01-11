from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.project import Project
from app.models.employee import Employee
from app.models.performance import PerformanceMetric
from app.models.backlog import BacklogItem
from app.models.user import UserProfile
import os
from datetime import datetime, timedelta

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

    # Seed Employees with Skills and Notice Periods
    now = datetime.utcnow()
    two_days_ago = now - timedelta(days=2)
    thirty_days_from_now = now + timedelta(days=30)
    fifteen_days_from_now = now + timedelta(days=15)
    
    employees = [
        # Notice Period Employees (Unique Names)
        Employee(
            name="Robert Stark", role="Dev", performance_score=9.2, free_since=two_days_ago,
            is_on_notice=True, notice_start_date=now - timedelta(days=15), notice_end_date=fifteen_days_from_now,
            skills="React, Python, SQL, AWS"
        ),
        Employee(
            name="Sarah Connor", role="QA", performance_score=8.7, free_since=two_days_ago,
            is_on_notice=False, skills="Selenium, Python, Jira, Automation"
        ),
        Employee(
            name="Arthur Morgan", role="PM", performance_score=9.5, free_since=two_days_ago,
            is_on_notice=True, notice_start_date=now - timedelta(days=5), notice_end_date=now + timedelta(days=25),
            skills="Agile, Jira, Strategy, Stakeholder Management"
        ),
        # Replacements & Others
        Employee(
            name="Harvey Specter", role="Senior Dev", performance_score=9.8, free_since=two_days_ago,
            skills="React, Python, AWS, Docker, Kubernetes"
        ),
        Employee(
            name="Donna Paulsen", role="QA Lead", performance_score=9.4, free_since=two_days_ago,
            skills="Selenium, QA Strategy, Leadership, Python"
        ),
        Employee(
            name="Louis Litt", role="Dev", performance_score=7.8, free_since=two_days_ago,
            skills="React, JavaScript, SQL"
        ),
        Employee(
            name="Rachel Zane", role="Designer", performance_score=8.9, free_since=two_days_ago,
            skills="Figma, UI/UX, Adobe XD"
        ),
        Employee(
            name="Jessica Pearson", role="Director", performance_score=9.9, free_since=two_days_ago,
            skills="Leadership, Strategy, Operations"
        ),
        Employee(
            name="Katrina Bennett", role="Dev", performance_score=8.5, free_since=two_days_ago,
            skills="Python, Django, PostgreSQL"
        ),
        Employee(
            name="Alex Williams", role="PM", performance_score=9.1, free_since=two_days_ago,
            skills="Agile, Scum, Strategy"
        ),
    ]
    db.add_all(employees)
    db.commit()

    # Seed Performance Metrics
    for emp in employees:
        metric = PerformanceMetric(
            employee_id=emp.id,
            velocity=12.5 if "Dev" in emp.role else 0,
            completion_rate=95.0 if emp.performance_score > 9.0 else 85.0,
            skills=emp.skills,
            promotion_ready="Yes" if emp.performance_score >= 9.5 else "No"
        )
        db.add(metric)
    
    # Seed Backlog
    b1 = BacklogItem(title="Setup OAuth2", description="Implement secure login flow", status="Done", priority="High", project_id=p1.id, type="STORY", story_points=5)
    b2 = BacklogItem(title="Design Homepage", description="Create UI mockups for mobile", status="In Progress", priority="Medium", project_id=p2.id, type="STORY", story_points=3)
    b3 = BacklogItem(title="API Gateway", description="Connect microservices with Ocelot", status="To Do", priority="High", project_id=p1.id, type="STORY", story_points=8)
    b4 = BacklogItem(title="React Dashboard UI", description="Implement main analytics view in React", status="To Do", priority="Medium", project_id=p1.id, type="STORY", story_points=5)
    b5 = BacklogItem(title="Data Visualization", description="D3.js charts for performance metrics", status="To Do", priority="Low", project_id=p2.id, type="STORY", story_points=3)
    b6 = BacklogItem(title="Python Logic Engine", description="Process NLP data from chatbot", status="To Do", priority="High", project_id=p3.id, type="STORY", story_points=13)
    db.add_all([b1, b2, b3, b4, b5, b6])
    
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
