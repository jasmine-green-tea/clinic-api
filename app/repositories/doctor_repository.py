from sqlmodel import Session, select
from app.models import Doctor
from app.schemas.doctor import Specialisation, DoctorCreate
from typing import List, Optional

class DoctorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, doctor_data: DoctorCreate) -> Doctor:
        db_doctor = Doctor(**doctor_data.dict()) # Преобразуем схему в модель БД

        self.session.add(db_doctor) # Добавляем в сессию
        self.session.commit() # Коммитим изменения в БД
        self.session.refresh(db_doctor) # Обновляем объект, чтобы получить сгенерированный ID

        return db_doctor
    
    def get_all(self) -> List[Doctor]:
        statement = select(Doctor)
        result = self.session.exec(statement)
        return result.all()

    def get_by_specialisation(self, doctor_specialisation: Specialisation) -> Optional[List[Doctor]]:
        statement = select(Doctor).where(Doctor.specialisation == doctor_specialisation)
        result = self.session.exec(statement)
        return result.all()