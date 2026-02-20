from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..auth import get_current_user, require_msl_or_agm_or_hod


router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=schemas.DoctorResponse)
def create_doctor(
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_msl_or_agm_or_hod),
):
    return crud.create_doctor(db, doctor)


@router.get("/", response_model=list[schemas.DoctorResponse])
def get_all_doctors(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_msl_or_agm_or_hod),
):
    return crud.get_doctors(db)
