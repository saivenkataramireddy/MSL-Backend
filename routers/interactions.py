from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud, models
from auth import get_current_user, require_msl

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.post("/", response_model=schemas.InteractionResponse)
def create_interaction(
    data: schemas.InteractionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_msl),
):
    data.msl_id = current_user.id
    return crud.create_interaction(db, data)


@router.get("/", response_model=list[schemas.InteractionResponse])
def get_all_interactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.DoctorInteraction)
    if current_user.role and current_user.role.name == "MSL":
        query = query.filter(models.DoctorInteraction.msl_id == current_user.id)
    return query.all()
