import sys
import os
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend.models import Role, User, Doctor, MSLRequest, PriorityEnum, RequestStatusEnum
from backend.auth import hash_password
import uuid

def seed():
    db: Session = SessionLocal()
    
    # 1. Create Roles
    roles_data = [
        {"name": "MSL", "description": "Medical Science Liaison"},
        {"name": "BM_BL", "description": "Business Manager / Business Leader"},
        {"name": "AGM", "description": "AGM - Medical Affairs"},
        {"name": "HOD", "description": "Head of Medical Affairs"}
    ]
    
    role_objs = {}
    for r in roles_data:
        existing = db.query(Role).filter(Role.name == r["name"]).first()
        if not existing:
            new_role = Role(id=str(uuid.uuid4()), name=r["name"], description=r["description"])
            db.add(new_role)
            db.commit()
            db.refresh(new_role)
            role_objs[r["name"]] = new_role
        else:
            role_objs[r["name"]] = existing

    # 2. Create Test Users
    users_data = [
        {"full_name": "Michael Liaison", "email": "msl@example.com", "password": "password123", "role": "MSL", "region": "North"},
        {"full_name": "Brenda Manager", "email": "bm@example.com", "password": "password123", "role": "BM_BL", "region": "North"},
        {"full_name": "Alice Growth", "email": "agm@example.com", "password": "password123", "role": "AGM", "region": "Global"},
        {"full_name": "Henry Director", "email": "hod@example.com", "password": "password123", "role": "HOD", "region": "Global"}
    ]

    for u in users_data:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            new_user = User(
                id=str(uuid.uuid4()),
                full_name=u["full_name"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                role_id=role_objs[u["role"]].id,
                region=u[ "region"]
            )
            db.add(new_user)
            db.commit()

    # 3. Create some Doctors if none exist
    if db.query(Doctor).count() == 0:
        doctors = [
            {"name": "Dr. Sarah Smith", "specialty": "Oncology", "hospital": "City Hospital", "region": "North", "therapy_area": "Breast Cancer"},
            {"name": "Dr. James Wilson", "specialty": "Cardiology", "hospital": "Heart Center", "region": "South", "therapy_area": "Hypertension"},
            {"name": "Dr. Elena Rodriguez", "specialty": "Neurology", "hospital": "Neuro Clinic", "region": "East", "therapy_area": "Multiple Sclerosis"}
        ]
        for d in doctors:
            new_doc = Doctor(id=str(uuid.uuid4()), **d)
            db.add(new_doc)
        db.commit()

    db.close()
    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed()
