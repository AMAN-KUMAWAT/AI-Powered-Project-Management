from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from app.models.base import Base
import datetime

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String) # Dev, QA, PM, etc.
    performance_score = Column(Float, default=0.0)
    avatar_url = Column(String, nullable=True)
    is_assigned = Column(Integer, default=0) # 0 for Free, 1 for Assigned
    assigned_task = Column(String, nullable=True) # Description of task
    free_since = Column(DateTime, default=datetime.datetime.utcnow) # Tracking idle time
    
    # NEW: Notice Period & Skills
    is_on_notice = Column(Boolean, default=False)
    notice_start_date = Column(DateTime, nullable=True)
    notice_end_date = Column(DateTime, nullable=True)
    skills = Column(String, default="") # Comma separated skills: "React, Python, SQL"
