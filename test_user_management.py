import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
import models
from auth import hash_password, create_access_token

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    # We use the real DB for now as configured in .env, but usually we'd use a test DB.
    # To keep it safe, we'll just cleanup our test records.
    db = SessionLocal()
    
    # Get Role IDs
    hod_role = db.query(models.Role).filter(models.Role.name == "HOD").first()
    msl_role = db.query(models.Role).filter(models.Role.name == "MSL").first()
    
    if not hod_role or not msl_role:
        pytest.fail("HOD or MSL roles not found in DB. Run seed script first.")

    # Create a HOD user for performing admin actions
    hod_user = db.query(models.User).filter(models.User.email == "test_admin@example.com").first()
    if not hod_user:
        hod_user = models.User(
            full_name="Admin User",
            email="test_admin@example.com",
            password_hash=hash_password("adminpass"),
            role_id=hod_role.id,
            is_active=True
        )
        db.add(hod_user)
        db.commit()
        db.refresh(hod_user)
    
    # Create a regular MSL user
    msl_user = db.query(models.User).filter(models.User.email == "test_msl@example.com").first()
    if not msl_user:
        msl_user = models.User(
            full_name="MSL User",
            email="test_msl@example.com",
            password_hash=hash_password("mslpass"),
            role_id=msl_role.id,
            is_active=True
        )
        db.add(msl_user)
        db.commit()
        db.refresh(msl_user)

    # Generate tokens
    admin_token = create_access_token(data={"sub": hod_user.email})
    msl_token = create_access_token(data={"sub": msl_user.email})
    
    yield {
        "admin_token": admin_token,
        "msl_token": msl_token,
        "msl_role_id": msl_role.id,
        "admin_email": hod_user.email,
        "msl_email": msl_user.email
    }
    
    # Cleanup test users (be careful not to delete real ones if this is production)
    # Since emails are specific to test, it's relatively safe.
    db.query(models.User).filter(models.User.email.in_([
        "test_admin@example.com", 
        "test_msl@example.com", 
        "new_user@example.com",
        "dup@example.com"
    ])).delete(synchronize_session=False)
    db.commit()
    db.close()

def test_hod_can_create_user(setup_db):
    headers = {"Authorization": f"Bearer {setup_db['admin_token']}"}
    payload = {
        "full_name": "New User",
        "email": "new_user@example.com",
        "password": "password123",
        "role_id": setup_db["msl_role_id"],
        "region": "North"
    }
    response = client.post("/users/", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "new_user@example.com"

def test_msl_cannot_create_user(setup_db):
    headers = {"Authorization": f"Bearer {setup_db['msl_token']}"}
    payload = {
        "full_name": "Illegal User",
        "email": "illegal@example.com",
        "password": "password123",
        "role_id": setup_db["msl_role_id"]
    }
    response = client.post("/users/", json=payload, headers=headers)
    assert response.status_code == 403 # Forbidden

def test_duplicate_email_validation(setup_db):
    headers = {"Authorization": f"Bearer {setup_db['admin_token']}"}
    payload = {
        "full_name": "Duplicate User",
        "email": setup_db["admin_email"], # Already exists
        "password": "password123",
        "role_id": setup_db["msl_role_id"]
    }
    response = client.post("/users/", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_user_activation_deactivation(setup_db):
    db_setup = SessionLocal()
    msl_user = db_setup.query(models.User).filter(models.User.email == setup_db["msl_email"]).first()
    user_id = msl_user.id
    db_setup.close()
    
    headers = {"Authorization": f"Bearer {setup_db['admin_token']}"}
    
    # Deactivate
    response = client.patch(f"/users/{user_id}", json={"is_active": False}, headers=headers)
    assert response.status_code == 200
    
    # Verify in DB (new session)
    db_verify1 = SessionLocal()
    updated_user1 = db_verify1.query(models.User).filter(models.User.id == user_id).first()
    assert updated_user1.is_active is False
    db_verify1.close()
    
    # Reactive
    response = client.patch(f"/users/{user_id}", json={"is_active": True}, headers=headers)
    assert response.status_code == 200
    
    # Verify in DB (new session)
    db_verify2 = SessionLocal()
    updated_user2 = db_verify2.query(models.User).filter(models.User.id == user_id).first()
    assert updated_user2.is_active is True
    db_verify2.close()
