from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, models
from database import get_db
from auth import get_current_user, require_hod, require_msl_or_agm_or_hod

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_hod),   # Only admins can create users
):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_hod),
):
    return db.query(models.User).all()


@router.get("/msls", response_model=list[schemas.UserResponse])
def list_msls(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_msl_or_agm_or_hod),
):
    """Returns all active MSL users."""
    return db.query(models.User).join(models.Role).filter(
        models.Role.name == "MSL", 
        models.User.is_active == True
    ).all()


@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user_status(
    user_id: str,
    status_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_hod),
):
    """Update user activation status, role, or other fields."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = status_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
        
    db.commit()
    db.refresh(user)
    return user
