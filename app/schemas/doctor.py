from sqlmodel import SQLModel
from datetime import date
from typing import Optional
from app.models import Specialisation

class DoctorCreate(SQLModel):
    full_name: str
    specialisation: Specialisation
    office_number: Optional[str] = None
    certificate_number: Optional[str] = None
    # department_id: int

class DoctorRead(SQLModel):
    id: int
    full_name: str
    specialisation: Specialisation
    office_number: Optional[str]
    certificate_number: Optional[str]
    # department_id: int