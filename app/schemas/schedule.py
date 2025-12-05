from sqlmodel import SQLModel
from datetime import date, time
from typing import Optional, List
from app.schemas.timeslot import TimeSlotsResponse
# from app.schemas.doctor import DoctorRead, Specialisation

class ScheduleCreate(SQLModel):
    doctor_id: int
    work_date: date
    start_time: time
    end_time: time
    slot_duration: int = 15

class ScheduleResponse(SQLModel):
    id: int
    doctor_id: int
    work_date: date
    start_time: time
    end_time: time
    slot_duration: int

class DoctorScheduleQuery(SQLModel):
    doctor_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ScheduleWithTimeSlotsResponse(SQLModel):
    id: int
    doctor_id: int
    work_date: date
    start_time: time
    end_time: time
    slot_duration: int
    time_slots: List[TimeSlotsResponse] = []

    class Config:
        from_attributes = True

class DoctorScheduleResponse(SQLModel):
    doctor_id: int
    schedules: List[ScheduleWithTimeSlotsResponse]
    total_schedules: int
    total_time_slots: int