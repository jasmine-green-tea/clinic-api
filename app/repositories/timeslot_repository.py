from sqlmodel import Session, select
from app.models import TimeSlot
from app.schemas.timeslot import TimeSlotCreate, SlotStatus
from typing import List, Optional
from datetime import date

class TimeSlotRepository:
    def __init__(self, session: Session):
        self.session = session

    def bulk_create(self, time_slots_data: List[TimeSlotCreate]) -> List[TimeSlot]:
        time_slots = [TimeSlot(**data.model_dump()) for data in time_slots_data]

        self.session.add_all(time_slots)
        self.session.commit()

        for slot in time_slots:
            self.session.refresh(slot)

        return time_slots

    def get_by_id(self, time_slot_id: int) -> Optional[TimeSlot]:
        statement = select(TimeSlot).where(TimeSlot.id == time_slot_id)
        result = self.session.exec(statement)
        return result.first()

    def get_by_schedule(self, schedule_id: int) -> List[TimeSlot]:
        statement = select(TimeSlot).where(TimeSlot.schedule_id == schedule_id)
        result = self.session.exec(statement)
        return result.all()

    # Обновление статуса слота
    def update_time_slot_status(self, time_slot_id: int, status: SlotStatus) -> Optional[TimeSlot]:
        try:
            time_slot = self.session.get(TimeSlot, time_slot_id)
            if not time_slot:
                return None

            time_slot.status = status

            self.session.add(time_slot)
            self.session.commit()
            self.session.refresh(time_slot)

            return time_slot
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка в TimeSlotRepository.apdate_time_slot_status: {str(e)}")
            raise