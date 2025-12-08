from sqlmodel import Session, select, func
from app.models import Patient, Appointment
from app.schemas.patient import PatientCreate, PatientUpdate
from typing import List, Optional, Dict, Any

class PatientRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, patient_data: PatientCreate) -> Patient:
        db_patient = Patient(**patient_data.dict()) # Преобразуем схему в модель БД

        self.session.add(db_patient) # Добавляем в сессию
        self.session.commit() # Коммитим изменения в БД
        self.session.refresh(db_patient) # Обновляем объект, чтобы получить сгенерированный ID

        return db_patient

    def get_all(self) -> List[Patient]:
        statement = select(Patient)
        result = self.session.exec(statement)
        return result.all()

    def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.session.get(Patient, patient_id)

    # Получить пациента со статистикой записей
    def get_patient_with_stats(self, patient_id: int) -> Optional[Dict[str, Any]]:
        patient = self.session.get(Patient, patient_id)
        if not patient:
            return None

        # Подсчет записей по статусам
        statement = select(
            Appointment.status,
            func.count(Appointment.id).label('count')
        ).where(
            Appointment.patient_id == patient_id
        ).group_by(Appointment.status)

        result = self.session.exec(statement)
        stats = {row[0]: row[1] for row in result}

        return {
            "patient": patient,
            "appointments_count": sum(stats.values()),
            "appointments_by_status": stats
        }

    # Обновить данные пациента
    def update_patient(self, patient_id: int, patient_data: PatientUpdate) -> Optional[Patient]:
        try:
            patient = self.session.get(Patient, patient_id)
            if not patient:
                return None

            # Получаем только те поля, которые были переданы (не None)
            update_data = patient_data.dict(exclude_unset=True)

            # # Если обновляется номер полиса, проверяем уникальность
            # if 'oms_policy_number' in update_data and update_data['oms_policy_number']:
            #     existing = self.get_patient_by_oms_number(update_data['oms_policy_number'])
            #     if existing and existing.id != patient_id:
            #         raise ValueError("Пациент с таким номером полиса ОМС уже существует")

            # Обновляем поля
            for field, value in update_data.items():
                setattr(patient, field, value)

            self.session.add(patient)
            self.session.commit()
            self.session.refresh(patient)
            return patient
        except Exception as e:
            self.session.rollback()
            raise