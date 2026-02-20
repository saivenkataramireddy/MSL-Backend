from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models

router = APIRouter(prefix="/office-activities", tags=["Office Activities"])

@router.post("/")
def create_activity(data: schemas.OfficeActivityCreate, db: Session = Depends(get_db)):
    obj = models.OfficeActivity(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.OfficeActivity).all()
