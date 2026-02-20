from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud, models

router = APIRouter(prefix="/objections", tags=["Objections"])

@router.post("/", response_model=schemas.ObjectionResponse)
def create_objection(data: schemas.ObjectionCreate, db: Session = Depends(get_db)):
    return crud.create_objection(db, data)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Objection).all()
