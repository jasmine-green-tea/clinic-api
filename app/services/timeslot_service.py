from sqlmodel import Session, select
from app.models import Schedule, TimeSlot, SlotStatus
from app.schemas.timeslot import TimeSlotsResponse, TimeSlotCreate
from app.repositories.timeslot_repository import TimeSlotRepository
from typing import List, Optional
from datetime import timedelta, datetime

class TimeSlotService:
    def __init__(self, timeslot_repository: TimeSlotRepository):
        self.timeslot_repo = timeslot_repository

    # Генерация слотов для расписания
    def generate_time_slots(self, schedule: Schedule) -> List[TimeSlotsResponse]:
        current_time = schedule.start_time
        slot_duration = timedelta(minutes=schedule.slot_duration)
        end_time = schedule.end_time

        time_slots_data = []

        while current_time < end_time:
            slot_end = (datetime.combine(schedule.work_date, current_time) + slot_duration).time()
            if slot_end > end_time:
                break

            time_slot_data = TimeSlotCreate(
                schedule_id=schedule.id,
                start_time=current_time,
                end_time=slot_end,
                status=SlotStatus.AVAILABLE
            )
            time_slots_data.append(time_slot_data)
            current_time = slot_end

            # Создаем все слоты одним запросом
        time_slots = self.timeslot_repo.bulk_create(time_slots_data)
        return [TimeSlotsResponse.model_validate(time_slot) for time_slot in time_slots]

    def get_time_slot_by_id(self, time_slot_id: int) -> Optional[TimeSlot]:
        return self.timeslot_repo.get_by_id(time_slot_id)

    #
    def get_time_slots_by_schedule(self, schedule_id: int) -> List[TimeSlotsResponse]:
        time_slots = self.timeslot_repo.get_by_schedule(schedule_id)
        return [TimeSlotsResponse.model_validate(time_slot) for time_slot in time_slots]
    
    def update_time_slot_status(self, time_slot_id: int, status: SlotStatus) -> Optional[TimeSlot]:
        return self.timeslot_repo.update_time_slot_status(time_slot_id, status)
