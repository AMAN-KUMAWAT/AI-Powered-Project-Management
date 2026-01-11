from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.models.base import Base

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    velocity = Column(Float)
    completion_rate = Column(Float)
    skills = Column(String) # JSON string or comma-separated
    promotion_ready = Column(String, default="No") # Yes, No, Needs Review
