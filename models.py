from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Enum, Date, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from database import Base
import enum

# ENUMS

class PriorityEnum(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


class RequestStatusEnum(str, enum.Enum):
    Requested = "Requested"
    Under_Review = "Under_Review"
    Assigned = "Assigned"
    Closed = "Closed"

# ROLES
class Role(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


# USERS

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(150))
    email = Column(String(150), unique=True)
    password_hash = Column(Text)
    role_id = Column(String(36), ForeignKey("roles.id"))
    region = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    role = relationship("Role")

# DOCTORS

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(150))
    specialty = Column(String(150))
    hospital = Column(String(150))
    region = Column(String(100))
    therapy_area = Column(String(150))
    assigned_msl_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    assigned_msl = relationship("User")

# MSL ENGAGEMENT REQUEST
class MSLRequest(Base):
    __tablename__ = "msl_engagement_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = Column(String(36), ForeignKey("doctors.id"))
    requested_by = Column(String(36), ForeignKey("users.id"))
    therapy_area = Column(String(150))
    objective = Column(Text)
    expected_outcome = Column(Text)
    priority = Column(Enum(PriorityEnum))
    status = Column(Enum(RequestStatusEnum), default=RequestStatusEnum.Requested)
    created_at = Column(TIMESTAMP, server_default=func.now())

    doctor = relationship("Doctor")
    requester = relationship("User")

# TOUR PLAN
class TourPlan(Base):
    __tablename__ = "tour_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    msl_id = Column(String(36), ForeignKey("users.id"))
    month = Column(Integer)
    year = Column(Integer)
    status = Column(String(20), default="Draft")
    submitted_at = Column(TIMESTAMP, nullable=True)
    approved_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    approved_at = Column(TIMESTAMP, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    msl = relationship("User", foreign_keys=[msl_id])

# DOCTOR INTERACTION
class DoctorInteraction(Base):
    __tablename__ = "doctor_interactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = Column(String(36), ForeignKey("doctors.id"))
    msl_id = Column(String(36), ForeignKey("users.id"))
    visit_date = Column(Date)
    topics_discussed = Column(Text)
    scientific_depth = Column(Integer)
    engagement_quality = Column(Integer)
    clinical_interest_level = Column(Integer)
    objection_complexity = Column(Integer)
    summary = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    doctor = relationship("Doctor")
    msl = relationship("User")


# OBJECTION
class Objection(Base):
    __tablename__ = "objections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = Column(String(36), ForeignKey("doctors.id"))
    interaction_id = Column(String(36), ForeignKey("doctor_interactions.id"))
    raised_by = Column(String(36), ForeignKey("users.id"))
    objection_text = Column(Text)
    category = Column(String(150))
    immediate_response = Column(Text)
    escalation_reason = Column(Text)
    status = Column(String(20), default="Draft")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    doctor = relationship("Doctor")
    interaction = relationship("DoctorInteraction")


# KNOWLEDGE ENTRY
class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255))
    content = Column(Text)
    category = Column(String(50))
    created_by = Column(String(36), ForeignKey("users.id"))
    status = Column(String(20), default="Draft")
    created_at = Column(TIMESTAMP, server_default=func.now())

    creator = relationship("User")
    
# OFFICE ACTIVITY
class OfficeActivity(Base):
    __tablename__ = "office_activities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    msl_id = Column(String(36), ForeignKey("users.id"))
    activity_date = Column(Date)
    category = Column(String(50))
    summary = Column(Text)
    linked_output_id = Column(String(36), ForeignKey("knowledge_entries.id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    msl = relationship("User")


# NOTIFICATION

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    type = Column(String(100))
    reference_id = Column(String(36))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")


# AUDIT LOG

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    table_name = Column(String(100))
    record_id = Column(String(36))
    action = Column(String(20))
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(String(36), ForeignKey("users.id"))
    changed_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
