from app.repositories.doctor_repository import DoctorRepository
from app.schemas.doctor import Specialisation, DoctorCreate
from app.models import Doctor
from typing import List, Optional

class DoctorService:

    def __init__(self, doctor_repository: DoctorRepository):
        self.doctor_repository = doctor_repository

    def create_doctor(self, doctor_data: DoctorCreate) -> Doctor:
        return self.doctor_repository.create(doctor_data)

    def get_all_doctors(self) -> List[Doctor]:
        return self.doctor_repository.get_all()

    def get_doctor(self, doctor_specialisation: Specialisation) -> Optional[List[Doctor]]:
        return self.doctor_repository.get_by_specialisation(doctor_specialisation)