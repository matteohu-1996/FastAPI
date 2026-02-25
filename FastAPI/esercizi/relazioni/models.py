from sqlalchemy import Integer, String, Column, ForeignKey, Date
from  sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = 'department'
    department_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    #relazione: un dipartimento contiene molti dipendenti
    employees = relationship('Employee', back_populates='department')

class Employee(Base):
    __tablename__ = 'employee'
    employee_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    role = Column(String(50))

    # relazione A 1:N appartiene a un solo department
    department_id = Column(Integer, ForeignKey('department.department_id'))
    department = relationship('Department', back_populates='employees')

    # relazione B 1:1 possiede un solo badge personale
    badge = relationship('Badge', back_populates='owner',
    uselist=False)

class Badge(Base):
    __tablename__ = 'badge'
    badge_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(7), unique=True)
    expiration_date = Column(Date)

    # relazione appartiene a un solo employee
    employee_id = Column(Integer, ForeignKey('employee.employee_id'), unique=True)
    owner = relationship('Employee', back_populates='badge')


