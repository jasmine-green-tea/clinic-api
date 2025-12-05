from sqlmodel import SQLModel
from datetime import time
from typing import Optional, List
from enum import Enum
from app.models import SlotStatus

class TimeSlotCreate(SQLModel):
    schedule_id: int
    start_time: time
    end_time: time
    status: SlotStatus = SlotStatus.AVAILABLE

class TimeSlotsResponse(SQLModel):
    id: int
    schedule_id: int
    start_time: time
    end_time: time
    status: SlotStatus

class TimeSlotResponseWithAppointment(TimeSlotsResponse):
    appointment_id: Optional[int] = None