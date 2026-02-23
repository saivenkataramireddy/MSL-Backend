from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from auth import require_hod

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_hod)
):
    """
    Returns aggregated metrics for the HOD dashboard.
    """
    total_users = db.query(models.User).count()
    active_msls = db.query(models.User).join(models.Role).filter(models.Role.name == "MSL", models.User.is_active == True).count()
    
    pending_tours = db.query(models.TourPlan).filter(models.TourPlan.status == "Draft").count()
    pending_objections = db.query(models.Objection).filter(models.Objection.status == "Draft").count()
    pending_knowledge = db.query(models.KnowledgeEntry).filter(models.KnowledgeEntry.status == "Draft").count()
    
    # Regional breakdown of interactions
    regional_data = db.query(
        models.User.region, 
        func.count(models.DoctorInteraction.id)
    ).join(models.DoctorInteraction, models.User.id == models.DoctorInteraction.msl_id)\
     .group_by(models.User.region).all()
    
    regional_stats = {region: count for region, count in regional_data if region}

    return {
        "metrics": {
            "total_users": total_users,
            "active_msls": active_msls,
            "pending_tour_plans": pending_tours,
            "pending_objections": pending_objections,
            "pending_knowledge": pending_knowledge
        },
        "regional_interactions": regional_stats
    }
