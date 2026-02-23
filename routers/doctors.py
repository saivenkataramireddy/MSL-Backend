from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import schemas, crud, models
from database import get_db
from auth import get_current_user, require_msl_or_agm_or_hod

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
    assigned_msl_id: Optional[str] = None,
    specialty: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_msl_or_agm_or_hod),
):
    query = db.query(models.Doctor)
    if assigned_msl_id:
        query = query.filter(models.Doctor.assigned_msl_id == assigned_msl_id)
    if specialty:
        query = query.filter(models.Doctor.specialty == specialty)
    if region:
        query = query.filter(models.Doctor.region == region)
    return query.all()


@router.patch("/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(
    doctor_id: str,
    doctor_update: dict,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_msl_or_agm_or_hod),
):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    for key, value in doctor_update.items():
        if hasattr(db_doctor, key):
            setattr(db_doctor, key, value)
            
    db.commit()
    db.refresh(db_doctor)
    return db_doctor
