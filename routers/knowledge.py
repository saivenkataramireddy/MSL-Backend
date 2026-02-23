from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import schemas, crud, models

from auth import get_current_user, require_msl, require_hod

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

@router.post("/", response_model=schemas.KnowledgeResponse)
def create_knowledge(
    data: schemas.KnowledgeCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_msl)
):
    data.created_by = current_user.id
    return crud.create_knowledge(db, data)

@router.get("/")
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.KnowledgeEntry)
    # MSLs only see Published or their own Drafts
    if current_user.role and current_user.role.name == "MSL":
        query = query.filter(
            (models.KnowledgeEntry.status == "Published") | 
            (models.KnowledgeEntry.created_by == current_user.id)
        )
    return query.all()

@router.patch("/{entry_id}/status", response_model=schemas.KnowledgeResponse)
def update_knowledge_status(
    entry_id: str,
    status: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_hod)
):
    """Endpoint for HOD to approve/publish knowledge content."""
    entry = db.query(models.KnowledgeEntry).filter(models.KnowledgeEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    
    entry.status = status
    db.commit()
    db.refresh(entry)
    return entry
