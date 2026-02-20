from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

from routers import auth
from routers import users
from routers import doctors
from routers import interactions
from routers import roles
from routers import tour
from routers import objections
from routers import knowledge
from routers import office
from routers import notifications

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MSL Engagement Module",
    version="1.0.0",
    description="Medical Science Liaison engagement platform with role-based access control.",
)

# ─── CORS (allow React dev server) ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5174","https://medical-science-liasion.netlify.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)        # /auth/login, /auth/me
app.include_router(users.router)       # /users/
app.include_router(doctors.router)     # /doctors/
app.include_router(interactions.router)# /interactions/
app.include_router(roles.router)       # /roles/
app.include_router(tour.router)        # /tour-plans/
app.include_router(objections.router)  # /objections/
app.include_router(knowledge.router)   # /knowledge/
app.include_router(office.router)      # /office-activities/
app.include_router(notifications.router) # /notifications/


@app.get("/", tags=["Root"])
def home():
    return {
        "message": "Welcome to MSL Engagement Module",
        "status": "Running",
        "docs": "/docs",
    }   
