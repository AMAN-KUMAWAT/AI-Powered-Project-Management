from sqlalchemy import Column, Integer, String, Float
from app.models.base import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String) # Dev, QA, PM, etc.
    performance_score = Column(Float, default=0.0)
    avatar_url = Column(String, nullable=True)
