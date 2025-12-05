from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import date

from app.database import get_session
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, DoctorScheduleResponse, DoctorScheduleQuery
from app.services.schedule_service import ScheduleService
from app.repositories.schedule_repository import ScheduleRepository
from app.services.timeslot_service import TimeSlotService
from app.repositories.timeslot_repository import TimeSlotRepository

router = APIRouter(prefix="/schedules", tags=["schedules"])

# def get_schedule_service(session: Session = Depends(get_session)) -> ScheduleService:
#     repository = ScheduleRepository(session)
#     return ScheduleService(repository)

# def get_timeslot_service(session: Session = Depends(get_session)) -> TimeSlotService:
#     repository = TimeSlotRepository(session)
#     return TimeSlotService(repository)

# def get_schedule_service(session: Session = Depends(get_session)) -> ScheduleService:
#     service = get_timeslot_service()
#     repository = ScheduleRepository(session)
#     return ScheduleService(repository, service)

def get_schedule_repository(session: Session = Depends(get_session)) -> ScheduleRepository:
    return ScheduleRepository(session)

def get_timeslot_repository(session: Session = Depends(get_session)) -> TimeSlotRepository:
    return TimeSlotRepository(session)

def get_timeslot_service(
    timeslot_repository: TimeSlotRepository = Depends(get_timeslot_repository)
) -> TimeSlotService:
    return TimeSlotService(timeslot_repository)

def get_schedule_service(
    schedule_repository: ScheduleRepository = Depends(get_schedule_repository),
    timeslot_service: TimeSlotService = Depends(get_timeslot_service)
) -> ScheduleService:
    return ScheduleService(schedule_repository, timeslot_service)

# Создание расписания
@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule_data: ScheduleCreate,
    schedule_service: ScheduleService = Depends(get_schedule_service)
):
    try:
        return schedule_service.create_schedule_with_slots(schedule_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating schedule: {str(e)}")

# Получение расписания по id
@router.get("/{schedule_id}")
def get_schedule_with_slots(
    schedule_id: int,
    schedule_service: ScheduleService = Depends(get_schedule_service)
):
    result = schedule_service.get_schedule_with_slots(schedule_id)
    if not result:
        raise HTTPException(status_code=404, detail="Расписание не найдено")
    return result

# Получение расписания врача за указанный период
@router.get("/{doctor_id}/doctor", response_model=DoctorScheduleResponse)
def get_doctor_schedule(
    doctor_id: int,
    start_date: Optional[date] = Query(None, description="Начальная дата периода"),
    end_date: Optional[date] = Query(None, description="Конечная дата периода"),
    schedule_service: ScheduleService = Depends(get_schedule_service)
):
    try:
        query = DoctorScheduleQuery(
            doctor_id=doctor_id,
            start_date=start_date,
            end_date=end_date
        )
        return schedule_service.get_doctor_schedule(query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting doctor schedule: {str(e)}")