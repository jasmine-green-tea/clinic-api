from app.repositories.appointment_repository import AppointmentRepository
from app.services.timeslot_service import TimeSlotService
from app.repositories.timeslot_repository import TimeSlotRepository
from app.repositories.patient_repository import PatientRepository
from app.models import Appointment, AppointmentStatus, TimeSlot, SlotStatus
from app.schemas.appointment import AppointmentCreate, AppointmentRead, PatientAppointmentRespose, AppointmentWithDetailsRead, AppointmentResponse
from app.schemas.timeslot import TimeSlotResponseWithAppointment
from typing import Optional, Dict, Any
from datetime import datetime, date

class AppointmentService:
    # def __init__(self,
    #              appointment_repository: AppointmentRepository,
    #              timeslot_repository: TimeSlotRepository,
    #              patient_repository: PatientRepository):
    #     self.appointment_repo = appointment_repository
    #     self.timeslot_repo = timeslot_repository
    #     self.patient_repo = patient_repository

    def __init__(self,
                 appointment_repository: AppointmentRepository,
                 timeslot_service: TimeSlotService,
                 patient_repository: PatientRepository):
        self.appointment_repository = appointment_repository
        self.timeslot_service = timeslot_service
        self.patient_repository = patient_repository

    # Создать запись
    def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        try:
            print(f"Начало бронирования слота {appointment_data.time_slot_id} для пациента {appointment_data.patient_id}")

            # Проверяем существование пациента
            patient = self.patient_repository.get_patient_by_id(appointment_data.patient_id)
            if not patient:
                raise ValueError("Пациент не найден")

            # Проверяем, что слот существует и доступен
            time_slot = self.timeslot_service.get_time_slot_by_id(appointment_data.time_slot_id)
            if not time_slot:
                raise ValueError("Временной слот не найден")

            if time_slot.status != SlotStatus.AVAILABLE:
                raise ValueError("Этот временной слот уже занят")

            # Создаем запись
            appointment_dict = {
                "patient_id": appointment_data.patient_id,
                "time_slot_id": appointment_data.time_slot_id,
                "status": AppointmentStatus.PLANNED
            }

            appointment = self.appointment_repository.create(appointment_dict)
            print(f"Запись создана: ID {appointment.id}")

            updated_time_slot = self.timeslot_service.update_time_slot_status(
                appointment_data.time_slot_id,
                SlotStatus.BOOKED
            )

            # if not updated_time_slot:
            #     # Откатываем создание записи если не удалось обновить слот
            #     self.appointment_repository.delete_appointment(appointment.id)
            #     raise ValueError("Не удалось обновить статус слота")

            print(f"Статус слота обновлен на: {updated_time_slot.status}")

            return {
                "appointment": AppointmentRead.model_validate(appointment),
                "time_slot": TimeSlotResponseWithAppointment(
                    id=updated_time_slot.id,
                    schedule_id=updated_time_slot.schedule_id,
                    start_time=updated_time_slot.start_time,
                    end_time=updated_time_slot.end_time,
                    status=updated_time_slot.status,
                    appointment_id=appointment.id
                )
                # Добавить имя пациента
            }
        except Exception as e:
            print(f"Ошибка бронирования: {str(e)}")
            raise

    # Получить все записи пациента
    def get_patient_appointments(self, patient_id: int) -> PatientAppointmentRespose:
        try:
            # Проверяем существование пациента
            patient = self.patient_repository.get_patient_by_id(patient_id)
            if not patient:
                raise ValueError(f"Пациент с ID {patient_id} не найден")

            # Получаем записи с деталями
            appointment_data = self.appointment_repository.get_appointments_by_patient_with_details(patient_id)

            # Преобразуем в схему ответа
            appointments = []
            for appointment, time_slot, schedule, doctor in appointment_data:
                appointment_with_details = AppointmentWithDetailsRead(
                    id=appointment.id,
                    patient_id=appointment.patient_id,
                    time_slot_id=appointment.time_slot_id,
                    status=appointment.status,
                    created_at=appointment.created_at,
                    slot_start_time=time_slot.start_time,
                    slot_end_time=time_slot.end_time,
                    slot_date=schedule.work_date,
                    doctor_id=doctor.id,
                    doctor_name=doctor.full_name,
                    doctor_specialisation=doctor.specialisation,
                    office_number=doctor.office_number,
                    schedule_id=schedule.id
                )
                appointments.append(appointment_with_details)

            # Подсчитываем статистику
            total_appointments = len(appointments)
            upcoming_appointments = len([
                a for a in appointments
                if a.status == AppointmentStatus.PLANNED and
                (a.slot_date > date.today() or
                 (a.slot_date == date.today() and a.slot_start_time > datetime.now().time()))
            ])
            completed_appointments = len([
                a for a in appointments
                if a.status == AppointmentStatus.COMPLETED
            ])

            response = PatientAppointmentRespose(
                patient_id=patient_id,
                patient_name=patient.full_name,
                appointments=appointments,
                total_appointments=total_appointments,
                upcoming_appointments=upcoming_appointments,
                completed_appointments=completed_appointments
            )

            return response

        except Exception as e:
            print(f"Ошибка получения записей пациента: {str(e)}")
            raise

    # Получить запись по id

    # Отменить запись и освободить слот
    def cancel_appointment(self, appointment_id: int) -> Dict[str, Any]:
        try:
            print(f"Отмена записи {appointment_id}")

            # 1. Получаем запись
            appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
            if not appointment:
                raise ValueError(f"Запись с ID {appointment_id} не найдена")

            # 2. Обновляем статус записи
            updated_appointment = self.appointment_repository.update_appointment_status(
                appointment_id,
                AppointmentStatus.CANCELLED
            )

            # 3. Освобождаем слот
            updated_time_slot = self.timeslot_service.update_time_slot_status(
                appointment.time_slot_id,
                SlotStatus.AVAILABLE
            )

            return {
                "appointment": AppointmentResponse.from_orm(updated_appointment),
                "time_slot": TimeSlotResponseWithAppointment(
                    id=updated_time_slot.id,
                    schedule_id=updated_time_slot.schedule_id,
                    start_time=updated_time_slot.start_time,
                    end_time=updated_time_slot.end_time,
                    status=updated_time_slot.status,
                    appointment_id=None
                )
            }
        except Exception as e:
            print(f"Ошибка отмены записи: {str(e)}")
            raise