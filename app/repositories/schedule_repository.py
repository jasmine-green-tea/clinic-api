from sqlmodel import Session, select, and_
from typing import List, Optional, Dict, Any
from datetime import date, timedelta
from app.models import Schedule
from app.schemas.schedule import ScheduleCreate

class ScheduleRepository:
    def __init__(self, session: Session):
        self.session = session

    # Создание расписания
    def create(self, schedule_data: ScheduleCreate) -> Schedule:
        db_schedule = Schedule(**schedule_data.dict())

        self.session.add(db_schedule)
        self.session.commit()
        self.session.refresh(db_schedule)

        return db_schedule

    # Получение расписания по id
    def get_schedule_by_id(self, schedule_id: int) -> Optional[Schedule]:
        statement = select(Schedule).where(Schedule.id == schedule_id)
        result = self.session.exec(statement)
        return result.first()

    # Получения распсиания врача за указанный период
    def get_schedules_by_doctor(
            self,
            doctor_id: int,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        try:
            # Базовый запрос для врача
            statement = select(Schedule).where(Schedule.doctor_id == doctor_id)

            # Добавляем фильтрацию по дате если указана
            if start_date and end_date:
                statement = statement.where(
                    and_(
                        Schedule.work_date >= start_date,
                        Schedule.work_date <= end_date
                    )
                )
            elif start_date:
                statement = statement.where(Schedule.work_date >= start_date)
            elif end_date:
                statement = statement.where(Schedule.work_date <= end_date)

            # Сортируем по дате
            statement = statement.order_by(Schedule.work_date)

            result = self.session.exec(statement)
            schedules = result.all()

            # Преобразуем в словари
            return [{
                "id": schedule.id,
                "doctor_id": schedule.doctor_id,
                "work_date": schedule.work_date,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "slot_duration": schedule.slot_duration
            } for schedule in schedules]

        except Exception as e:
            print(f"Ошибка в ScheduleRepository.get_schedules_by_doctor_and_date_range: {str(e)}")
            raise