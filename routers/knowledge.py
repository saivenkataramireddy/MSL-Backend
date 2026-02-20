from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud, models

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

@router.post("/", response_model=schemas.KnowledgeResponse)
def create_knowledge(data: schemas.KnowledgeCreate, db: Session = Depends(get_db)):
    return crud.create_knowledge(db, data)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.KnowledgeEntry).all()
