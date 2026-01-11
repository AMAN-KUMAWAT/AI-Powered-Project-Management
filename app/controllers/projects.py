from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.project import Project
from pydantic import BaseModel
from typing import Optional
import io
from pypdf import PdfReader

router = APIRouter()

@router.post("/projects")
async def create_project(
    name: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    extracted_text = ""
    if file and file.filename.endswith('.pdf'):
        try:
            pdf_content = await file.read()
            reader = PdfReader(io.BytesIO(pdf_content))
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            
            # Append extracted text to description
            if extracted_text:
                description = f"{description}\n\n[Extracted Requirements]:\n{extracted_text}"
        except Exception as e:
            print(f"Error extracting PDF: {e}")

    db_project = Project(name=name, description=description, priority=priority)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/projects/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}
