from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas.doctor import Specialisation, DoctorCreate, DoctorRead
from app.services.doctor_service import DoctorService
from app.repositories.doctor_repository import DoctorRepository

router = APIRouter(prefix="/doctors", tags=["doctors"])

def get_doctor_service(session: Session = Depends(get_session)) -> DoctorService:
    repository = DoctorRepository(session)
    return DoctorService(repository)

@router.post("/", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
def create_doctor(
    doctor_data: DoctorCreate,
    doctor_service: DoctorService = Depends(get_doctor_service)
):
    try:
        return doctor_service.create_doctor(doctor_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[DoctorRead])
def get_all_doctors(
    doctor_service: DoctorService = Depends(get_doctor_service)
):
    return doctor_service.get_all_doctors()

@router.get("/{doctor_specialisation}", response_model=List[DoctorRead])
def get_doctor(
    doctor_specialisation: Specialisation,
    doctor_service: DoctorService = Depends(get_doctor_service)
):
    doctor = doctor_service.get_doctor(doctor_specialisation)
    if not doctor:
        raise HTTPException(status_code=404, detail="Доктор не найден")
    return doctor
