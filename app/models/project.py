from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.models.base import Base
import datetime

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="Active")
    priority = Column(String, default="Medium")
    backlog_json = Column(JSON, nullable=True) # NEW: For saving the AI generated plan
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
