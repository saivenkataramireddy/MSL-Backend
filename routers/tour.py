from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud, models

router = APIRouter(prefix="/tour-plans", tags=["Tour Plans"])

@router.post("/", response_model=schemas.TourPlanResponse)
def create_tour(data: schemas.TourPlanCreate, db: Session = Depends(get_db)):
    return crud.create_tour_plan(db, data)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.TourPlan).all()
