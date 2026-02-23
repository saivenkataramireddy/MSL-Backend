from pydantic import BaseModel, EmailStr
from typing import Optional, Union, List
import enum


# ─── Auth Schemas ──────────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    role: Union[str, None] = None

class RoleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

# ─── User Schemas ──────────────────────────────────────────────────
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role_id: str
    region: Optional[str]


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[str] = None
    region: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    is_active: bool
    role: Optional[RoleResponse] = None

    class Config:
        from_attributes = True


class UserMeResponse(BaseModel):
    id: str
    full_name: str
    email: str
    region: Optional[str]
    is_active: bool
    role: Optional[RoleResponse] = None

    class Config:
        from_attributes = True


# DOCTOR SCHEMAS
class DoctorCreate(BaseModel):
    name: str
    specialty: str
    hospital: str
    region: str
    therapy_area: str


class DoctorResponse(BaseModel):
    id: str
    name: str
    specialty: str
    hospital: str
    region: str
    therapy_area: str
    assigned_msl_id: Optional[str] = None
    is_active: bool
    assigned_msl: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Tour Schema

class TourPlanCreate(BaseModel):
    msl_id: Optional[str] = None
    month: int
    year: int


class TourPlanResponse(BaseModel):
    id: str
    month: int
    year: int
    status: str
    msl: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# DOCTOR INTERACTION

class InteractionCreate(BaseModel):
    doctor_id: str
    msl_id: Optional[str] = None
    visit_date: str
    topics_discussed: str
    scientific_depth: int
    engagement_quality: int
    clinical_interest_level: int
    objection_complexity: int
    summary: str


class InteractionResponse(BaseModel):
    id: str
    doctor_id: str
    summary: str

    class Config:
        from_attributes = True


# OBJECTION
class ObjectionCreate(BaseModel):
    doctor_id: str
    interaction_id: str
    raised_by: Optional[str] = None
    objection_text: str
    category: str


class ObjectionResponse(BaseModel):
    id: str
    objection_text: str
    status: str

    class Config:
        from_attributes = True

# KNOWLEDGE ENTRY

class KnowledgeCreate(BaseModel):
    title: str
    content: str
    category: str
    created_by: Optional[str] = None


class KnowledgeResponse(BaseModel):
    id: str
    title: str
    status: str

    class Config:
        from_attributes = True

# OFFICE ACTIVITY
class OfficeActivityCreate(BaseModel):
    msl_id: Optional[str] = None
    activity_date: str
    category: str
    summary: str


class OfficeActivityResponse(BaseModel):
    id: str
    category: str

    class Config:
        from_attributes = True


# NOTIFICATION
class NotificationResponse(BaseModel):
    id: str
    message: str
    is_read: bool

    class Config:
        from_attributes = True
