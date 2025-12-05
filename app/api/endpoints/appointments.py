from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import date

from app.database import get_session
from app.models import Appointment
from app.schemas.appointment import (
    AppointmentCreate, AppointmentRead, PatientAppointmentsResponse
)
from app.repositories.appointment_repository import AppointmentRepository
from app.services.appointment_service import AppointmentService
from app.repositories.timeslot_repository import TimeSlotRepository
from app.services.timeslot_service import TimeSlotService
from app.repositories.patient_repository import PatientRepository

router = APIRouter(prefix="/appointments", tags=["appointments"])

# def get_appointment_service(session: Session = Depends(get_session)) -> AppointmentService:
#     appointment_repo = AppointmentRepository(session)
#     timeslot_repo = TimeSlotRepository(session)
#     patient_repo = PatientRepository(session)
#     return AppointmentService(appointment_repo, timeslot_repo, patient_repo)

def get_appointment_repository(session: Session = Depends(get_session)) -> AppointmentRepository:
    return AppointmentRepository(session)

def get_timeslot_repository(session: Session = Depends(get_session)) -> TimeSlotRepository:
    return TimeSlotRepository(session)

def get_patient_repository(session: Session = Depends(get_session)) -> PatientRepository:
    return PatientRepository(session)

def get_timeslot_service(
    timeslot_repository: TimeSlotRepository = Depends(get_timeslot_repository)
) -> TimeSlotService:
    return TimeSlotService(timeslot_repository)

def get_appointment_service(
    schedule_repository: AppointmentRepository = Depends(get_appointment_repository),
    timeslot_service: TimeSlotService = Depends(get_timeslot_service),
    patient_repository: PatientRepository = Depends(get_patient_repository)
) -> AppointmentService:
    return AppointmentService(schedule_repository, timeslot_service, patient_repository)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_data: AppointmentCreate,
    appointment_service: AppointmentService = Depends(get_appointment_service)
):
    try:
        return appointment_service.create_appointment(appointment_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Получить все записи пациента с детальной информацией и статистикой
@router.get("/{patient_id}", response_model=PatientAppointmentsResponse)
def get_patient_appointments(
    patient_id: int,
    appointment_service: AppointmentService = Depends(get_appointment_service)
):
    try:
        return appointment_service.get_patient_appointments(patient_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Отменить запись и освободить слот
@router.delete("/appointments/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    appointment_service: AppointmentService = Depends(get_appointment_service)
):
    try:
        result = appointment_service.cancel_appointment(appointment_id)
        return {
            "success": True,
            "message": "Запись успешно отменена",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))