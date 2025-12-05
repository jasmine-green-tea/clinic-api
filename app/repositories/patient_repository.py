from sqlmodel import Session, select
from app.models import Patient
from app.schemas.patient import PatientCreate
from typing import List, Optional

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