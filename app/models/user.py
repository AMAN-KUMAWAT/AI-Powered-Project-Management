from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Aman Kumawat")
    email = Column(String, default="aman@example.com")
    bio = Column(Text, default="Product Manager & AI Enthusiast")
    avatar_url = Column(String, nullable=True)
    theme = Column(String, default="dark") # "dark" or "light"
