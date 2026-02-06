from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Badge
class BadgeBase(BaseModel):
    badge_employee_name: str
    badge_code: str

class BadgeCreate(BadgeBase):
    expiration_date: date
    employee_id: int

class Badge(BaseModel):
    badge_id: int
    expiration_date: date
    class Config:
        from_attributes = True


# dipartimenti
class DepartmentBase(BaseModel):
    department_name: str

class DepartmentCreate(DepartmentBase):
    pass


# dipendenti
class EmployeeBase(BaseModel):
    full_name: str
    role: str
    department_id: int = Field(..., gt=0)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(BaseModel):
    employee_id: int
    badge: Badge
    badge: Optional[Badge] = None
    department: DepartmentBase
    class Config:
        from_attributes = True


class DepartmentResponse(BaseModel):
    department_id: int
    employees: List[EmployeeResponse]
    class Config:
        from_attributes = True
