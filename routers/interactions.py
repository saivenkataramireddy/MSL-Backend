from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud, models
from ..auth import get_current_user, require_msl

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.post("/", response_model=schemas.InteractionResponse)
def create_interaction(
    data: schemas.InteractionCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_msl),
):
    return crud.create_interaction(db, data)


@router.get("/", response_model=list[schemas.InteractionResponse])
def get_all_interactions(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return db.query(models.DoctorInteraction).all()
