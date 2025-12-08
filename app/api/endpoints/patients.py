from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.services.patient_service import PatientService
from app.repositories.patient_repository import PatientRepository

router = APIRouter(prefix="/patients", tags=["patients"])

def get_patient_service(session: Session = Depends(get_session)) -> PatientService:
    repository = PatientRepository(session)
    return PatientService(repository)

@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient_data: PatientCreate,
    patient_service: PatientService = Depends(get_patient_service)
):
    try:
        return patient_service.create_patient(patient_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PatientRead])
def get_all_patients(
    patient_service: PatientService = Depends(get_patient_service)
):
    return patient_service.get_all_patients()

# PUT метод для полного обновления пациента
@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    patient_service: PatientService = Depends(get_patient_service)
):
    #Полностью обновить данные пациента (PUT)
    try:
        updated_patient = patient_service.update_patient(patient_id, patient_data)
        if not updated_patient:
            raise HTTPException(status_code=404, detail="Пациент не найден")
        return updated_patient
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))