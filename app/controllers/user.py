from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import UserProfile
import shutil
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/views")

@router.get("/profile")
async def get_profile(request: Request, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@router.post("/profile/update")
async def update_profile(
    name: str = Form(...),
    email: str = Form(...),
    bio: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(UserProfile).first()
    user.name = name
    user.email = email
    user.bio = bio
    db.commit()
    return {"status": "success"}

@router.post("/profile/theme")
async def update_theme(theme: str, db: Session = Depends(get_db)):
    user = db.query(UserProfile).first()
    if theme in ["light", "dark"]:
        user.theme = theme
        db.commit()
        return {"status": "success", "theme": user.theme}
    raise HTTPException(status_code=400, detail="Invalid theme")

@router.post("/profile/avatar")
async def update_avatar(file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs("static/uploads", exist_ok=True)
    file_path = f"static/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    user = db.query(UserProfile).first()
    user.avatar_url = f"/static/uploads/{file.filename}"
    db.commit()
    return {"status": "success", "avatar_url": user.avatar_url}
