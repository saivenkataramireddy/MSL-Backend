from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
import schemas, crud, models
from typing import Optional

from auth import get_current_user, require_msl, require_hod

router = APIRouter(prefix="/tour-plans", tags=["Tour Plans"])

@router.post("/", response_model=schemas.TourPlanResponse)
def create_tour(
    data: schemas.TourPlanCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_msl)
):
    data.msl_id = current_user.id
    return crud.create_tour_plan(db, data)

@router.get("/", response_model=list[schemas.TourPlanResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.TourPlan)
    # If MSL, only show their own plans
    if current_user.role and current_user.role.name == "MSL":
        query = query.filter(models.TourPlan.msl_id == current_user.id)
    return query.all()

@router.patch("/{plan_id}/approve", response_model=schemas.TourPlanResponse)
def approve_tour_plan(
    plan_id: str,
    approved: bool = True,
    rejection_reason: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_hod)
):
    plan = db.query(models.TourPlan).filter(models.TourPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Tour plan not found")
    
    plan.status = "Approved" if approved else "Rejected"
    plan.approved_by = current_user.id
    plan.approved_at = datetime.utcnow()
    if not approved and rejection_reason:
        plan.rejection_reason = rejection_reason
        
    db.commit()
    db.refresh(plan)
    return plan
