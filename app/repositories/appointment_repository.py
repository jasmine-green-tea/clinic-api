from sqlmodel import Session, select, and_
from app.models import Appointment, AppointmentStatus, Doctor, TimeSlot, Schedule
from app.schemas.appointment import AppointmentCreate
from typing import List, Optional, Tuple
from datetime import datetime, date, time

class AppointmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, appointment_data: dict) -> Appointment:
        db_appointment = Appointment(**appointment_data)
        self.session.add(db_appointment)
        self.session.commit()
        self.session.refresh(db_appointment)
        return db_appointment

    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        statement = select(Appointment).where(Appointment.id == appointment_id)
        result = self.session.exec(statement)
        return result.first()

    # Получить все записи пациента
    def get_appointment_by_patient(self, patient_id: int) -> List[Appointment]:
        statement = select(Appointment).where(Appointment.patient_id == patient_id)
        result = self.session.exec(statement)
        return result.all()

    # Получить записи пациента с детальной информацией о слотах, расписании и врачах
    def get_appointments_by_patient_with_details(self, patient_id: int) -> List[Tuple[Appointment, TimeSlot, Schedule, Doctor]]:
        statement = (
            select(Appointment, TimeSlot, Schedule, Doctor)
            .join(TimeSlot, Appointment.time_slot_id == TimeSlot.id)
            .join(Schedule, TimeSlot.schedule_id == Schedule.id)
            .join(Doctor, Schedule.doctor_id == Doctor.id)
            .where(Appointment.patient_id == patient_id)
            .order_by(Schedule.work_date, TimeSlot.start_time)
        )
        result = self.session.exec(statement)
        return result.all()

    # Получить запись по id
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        return self.session.get(Appointment, appointment_id)

    # Обновить статус записи
    def update_appointment_status(self, appointment_id: int, status: AppointmentStatus) -> Optional[Appointment]:
        appointment = self.session.get(Appointment, appointment_id)
        if not appointment:
            return None

        appointment.status = status
        self.session.add(appointment)
        self.session.commit()
        self.session.refresh(appointment)
        return appointment

    # Удалить запись
    def delete_appointment(self, appointment_id: int) -> bool:
        appointment = self.session.get(Appointment, appointment_id)
        if not appointment:
            return False

        self.session.delete(appointment)
        self.session.commit()
        return True