from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, time, datetime
from enum import Enum

# Пациенты
class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=255, nullable=False)
    date_of_birth: date = Field(nullable=False)
    gender: Optional[str] = Field(max_length=10, default=None)
    oms_policy_number: str = Field(max_length=20, nullable=False)
    phone_number: Optional[str] = Field(max_length=20, default=None)
    address: Optional[str] = Field(default=None)

    appointments: List["Appointment"] = Relationship(back_populates="patient")

# Врачи
class Specialisation(str, Enum):
    THERAPIST = "Терапевт"
    SURGEON = "Хирург"
    GYNECOLOGIST = "Гинеколог"
    CARDIOLOGIST = "Кардиолог"
    NEUROLOGIST = "Невролог"
    PSYCHIATRIST = "Психиатр"

class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=255, nullable=False)
    specialisation: Specialisation = Field(nullable=False)
    office_number: Optional[str] = Field(max_length=10, default=None)
    certificate_number: Optional[str] = Field(default=None)

    schedules: List["Schedule"] = Relationship(back_populates="doctor")

# Расписание
class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctor.id", nullable=False)
    work_date: date = Field(nullable=False) # Дата работы
    start_time: time = Field(nullable=False) # Время начала
    end_time: time = Field(nullable=False) # Время окончания
    slot_duration: int = Field(default=15) # Длительность приёма в минутах

    doctor: "Doctor" = Relationship(back_populates="schedules")
    time_slots: List["TimeSlot"] = Relationship(back_populates="schedule")

# Слоты
class SlotStatus(str, Enum):
    AVAILABLE = "Доступно"
    BOOKED = "Забронировано"
    UNAVAILABLE = "Недоступно"

class TimeSlot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    schedule_id: int = Field(foreign_key="schedule.id", nullable=False)
    start_time: time = Field(nullable=False)
    end_time: time = Field(nullable=False)
    status: SlotStatus = Field(default=SlotStatus.AVAILABLE)

    schedule: "Schedule" = Relationship(back_populates="time_slots")
    appointment: Optional["Appointment"] = Relationship(back_populates="time_slot")

# Записи
class AppointmentStatus(str, Enum):
    PLANNED = "Запланирован"
    COMPLETED = "Завершен"
    CANCELLED = "Отменен"
    NO_SHOW = "no_show"

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id", nullable=False)
    time_slot_id: int = Field(foreign_key="timeslot.id", nullable=False, unique=True)
    status: AppointmentStatus = Field(default=AppointmentStatus.PLANNED)
    created_at: datetime = Field(default_factory=datetime.now)
    # updated_at: datetime = Field(default_factory=datetime.now)

    patient: "Patient" = Relationship(back_populates="appointments")
    time_slot: "TimeSlot" = Relationship(back_populates="appointment")
