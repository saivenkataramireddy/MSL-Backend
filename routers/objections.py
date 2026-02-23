from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import schemas, crud, models

from auth import get_current_user, require_msl, require_hod, require_agm_or_hod

router = APIRouter(prefix="/objections", tags=["Objections"])

@router.post("/", response_model=schemas.ObjectionResponse)
def create_objection(
    data: schemas.ObjectionCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_msl)
):
    data.raised_by = current_user.id
    return crud.create_objection(db, data)

@router.get("/", response_model=list[schemas.ObjectionResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Objection)
    if current_user.role and current_user.role.name == "MSL":
        query = query.filter(models.Objection.raised_by == current_user.id)
    return query.all()

@router.patch("/{objection_id}/status", response_model=schemas.ObjectionResponse)
def update_objection_status(
    objection_id: str,
    status: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_agm_or_hod)
):
    """Endpoint for AGM or HOD to update objection status (e.g. Escalated, Resolved)."""
    obj = db.query(models.Objection).filter(models.Objection.id == objection_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objection not found")
    
    obj.status = status
    db.commit()
    db.refresh(obj)
    return obj
