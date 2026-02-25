from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Badge
class BadgeBase(BaseModel):
    code: str
    expiration_date: date

class BadgeCreate(BadgeBase):
    employee_id: int

class Badge(BadgeBase):
    badge_id: int
    class Config:
        from_attributes = True


# dipartimenti
class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    department_id: Optional[int] = None


# dipendenti
class EmployeeBase(BaseModel):
    full_name: str
    role: str
    department_id: int = Field(..., gt=0)

class EmployeeCreate(EmployeeBase):
    employee_id: Optional[int] = None

class EmployeeResponse(BaseModel):
    employee_id: int
    badge: Optional[Badge] = None
    class Config:
        from_attributes = True


class DepartmentResponse(BaseModel):
    department_id: int
    name: str
    employees: List[EmployeeResponse] = []
    class Config:
        from_attributes = True
