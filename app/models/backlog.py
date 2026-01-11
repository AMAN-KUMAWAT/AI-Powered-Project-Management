from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from app.models.base import Base
import datetime

class BacklogItem(Base):
    __tablename__ = "backlog_items"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    type = Column(String) # EPIC, STORY, SPRINT
    status = Column(String, default="To Do") # To Do, In Progress, Done
    priority = Column(String, default="Medium")
    title = Column(String, index=True)
    description = Column(Text)
    story_points = Column(Integer, default=0)
    sprint_number = Column(Integer, default=1)
    editable_content = Column(JSON, nullable=True) # For custom fields/AI output
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
