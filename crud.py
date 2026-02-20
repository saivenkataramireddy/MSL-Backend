from sqlalchemy.orm import Session
from . import models
from .auth import hash_password


def create_user(db: Session, user):
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hash_password(user.password),
        role_id=user.role_id,
        region=user.region,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_doctor(db: Session, doctor):
    db_doc = models.Doctor(**doctor.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def get_doctors(db: Session):
    return db.query(models.Doctor).all()


def create_tour_plan(db: Session, data):
    obj = models.TourPlan(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_interaction(db: Session, data):
    obj = models.DoctorInteraction(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_objection(db: Session, data):
    obj = models.Objection(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_knowledge(db: Session, data):
    obj = models.KnowledgeEntry(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
