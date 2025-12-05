from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate
from app.models import Patient
from datetime import date
from typing import List

class PatientService:

    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def create_patient(self, patient_data: PatientCreate) -> Patient:
        if not self._validate_oms_policy(patient_data.oms_policy_number):
            raise ValueError("Неверный формат номера полиса ОМС")

        if patient_data.date_of_birth > date.today():
            raise ValueError("Дата рождения не может быть в будущем")

        return self.patient_repository.create(patient_data)

    def _validate_oms_policy(self, oms_number: str) -> bool:
        return len(oms_number) >= 16 and oms_number.isdigit()

    def get_all_patients(self) -> List[Patient]:
        return self.patient_repository.get_all()