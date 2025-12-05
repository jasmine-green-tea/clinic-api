from fastapi import FastAPI
from app.database import create_db_and_tables
from app.api.endpoints import patients, doctors, schedules, appointments

app = FastAPI(
    title="Clinic API",
    description="API для управления поликлиникой",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(schedules.router)
app.include_router(appointments.router)

@app.post("/")
def read_root():
    return {"message": "Clinic API is running"}