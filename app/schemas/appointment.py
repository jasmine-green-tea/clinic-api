from sqlmodel import SQLModel
from datetime import datetime, time, date
from typing import Optional, List
from enum import Enum
from .patient import PatientRead
from .doctor import DoctorRead
from app.models import AppointmentStatus, Specialisation

class AppointmentCreate(SQLModel):
    patient_id: int
    time_slot_id: int
    status: AppointmentStatus = AppointmentStatus.PLANNED

class AppointmentRead(SQLModel):
    id: int
    patient_id: int
    time_slot_id: int
    status: AppointmentStatus
    created_at: datetime

class AppointmentWithDetailsRead(SQLModel):
    id: int
    patient_id: int
    time_slot_id: int
    status: AppointmentStatus
    created_at: datetime

    # Детали слота времени
    slot_start_time: time
    slot_end_time: time
    slot_date: date

    # Детали врача
    doctor_id: int
    doctor_name: str
    doctor_specialisation: Specialisation
    office_number: Optional[str] = None

    # Детали расписания
    schedule_id: int

class PatientAppointmentRespose(SQLModel):
    patient_id: int
    patient_name: str
    appointments: List[AppointmentWithDetailsRead]
    total_appointments: int
    upcoming_appointments: int
    completed_appointments: int

class PatientAppointmentsResponse(SQLModel):
    patient_id: int
    patient_name: str
    appointments: List[AppointmentWithDetailsRead]
    total_appointments: int
    upcoming_appointments: int
    completed_appointments: int

class AppointmentResponse(SQLModel):
    id: int
    patient_id: int
    time_slot_id: int
    status: AppointmentStatus
    created_at: datetime