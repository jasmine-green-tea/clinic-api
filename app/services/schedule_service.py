from app.repositories.schedule_repository import ScheduleRepository
from app.services.timeslot_service import TimeSlotService
from app.models import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleWithTimeSlotsResponse, DoctorScheduleQuery, DoctorScheduleResponse
from typing import List, Optional
from datetime import date, timedelta

class ScheduleService:
    def __init__(self,
                 schedule_repository: ScheduleRepository,
                 timeslot_service: TimeSlotService):
        self.schedule_repository = schedule_repository
        self.timeslot_service = timeslot_service

    # Создание расписания и создание слотов
    def create_schedule_with_slots(self, schedule_data: ScheduleCreate) -> ScheduleWithTimeSlotsResponse:
        try:
            schedule = self.schedule_repository.create(schedule_data)
            self.timeslot_service.generate_time_slots(schedule)

            return ScheduleResponse.from_orm(schedule)
        except Exception as e:
            self.schedule_repository.session.rollback()
            raise e

    # Получение расписания по id со слотами
    def get_schedule_with_slots(self, schedule_id: int) -> Optional[ScheduleWithTimeSlotsResponse]:
        schedule_data = self.schedule_repository.get_schedule_by_id(schedule_id)
        if not schedule_data:
            return None

        time_slots = self.timeslot_service.get_time_slots_by_schedule(schedule_id)

        return ScheduleWithTimeSlotsResponse(
                **schedule_data.model_dump(),
                time_slots=time_slots
            )

    # Получаем расписание врача
    def get_doctor_schedule(self, query: DoctorScheduleQuery) -> DoctorScheduleResponse:
        try:
            print(f"Получение расписания для врача {query.doctor_id} с {query.start_date} по {query.end_date}")

            # Если даты не указаны, используем текущую неделю по умолчанию
            start_date = query.start_date or date.today()
            end_date = query.end_date or (date.today() + timedelta(days=7))

            # Получаем расписания через репозиторий
            schedules_data = self.schedule_repository.get_schedules_by_doctor(
                doctor_id=query.doctor_id,
                start_date=start_date,
                end_date=end_date
            )

            print(f"Найдено расписаний: {len(schedules_data)}")

            # Для каждого расписания получаем слоты времени
            schedules_with_slots = []
            total_time_slots = 0

            for schedule_data in schedules_data:
                time_slots = self.timeslot_service.get_time_slots_by_schedule(schedule_data["id"])
                total_time_slots += len(time_slots)

                schedule_with_slots = ScheduleWithTimeSlotsResponse(
                    **schedule_data,
                    time_slots=time_slots
                )
                schedules_with_slots.append(schedule_with_slots)

            response = DoctorScheduleResponse(
                doctor_id=query.doctor_id,
                schedules=schedules_with_slots,
                total_schedules=len(schedules_with_slots),
                total_time_slots=total_time_slots
            )

            print(f"Успешно сформирован ответ: {response.total_schedules} расписаний, {response.total_time_slots} слотов")
            return response

        except Exception as e:
            error_msg = f"Ошибка в ScheduleService.get_doctor_schedule: {str(e)}"
            print(error_msg)
            raise Exception(error_msg) from e

