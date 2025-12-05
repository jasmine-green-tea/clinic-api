from sqlmodel import SQLModel
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