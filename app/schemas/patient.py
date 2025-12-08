from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class PatientCreate(SQLModel):
    full_name: str
    date_of_birth: date
    gender: Optional[str] = None
    oms_policy_number: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

class PatientRead(SQLModel):
    id: int
    full_name: str
    date_of_birth: date
    gender: Optional[str]
    oms_policy_number: str
    phone_number: Optional[str]
    address: Optional[str]
    appointments_count: Optional[int] = 0

class PatientUpdate(SQLModel):
    full_name: Optional[str] = Field(None, max_length=255, description="Полное имя пациента")
    date_of_birth: Optional[date] = Field(None, description="Дата рождения")
    gender: Optional[str] = Field(None, max_length=10, description="Пол")
    oms_policy_number: Optional[str] = Field(None, max_length=20, description="Номер полиса ОМС")
    phone_number: Optional[str] = Field(None, max_length=20, description="Номер телефона")
    address: Optional[str] = Field(None, description="Адрес")