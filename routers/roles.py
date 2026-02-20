from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_hod


router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=schemas.RoleResponse)
def create_role(
    name: str,
    description: str,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_hod),
):
    role = models.Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.get("/", response_model=list[schemas.RoleResponse])
def get_roles(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return db.query(models.Role).all()
