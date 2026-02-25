from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Query
import models, schemas

# creo dipartimento
def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(
        department_id=department.department_id,
        name=department.name
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

# creo dipendente associandolo a un dipartimento tramite id
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    dept_id = employee.department_id
    dept = db.query(models.Department).filter(
        models.Department.department_id == employee.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail=f"Dipartimento con id "
                                                    f"{dept_id} non "
                                                    "trovato" )
    db_employee = models.Employee(**employee.model_dump())
    try:
        db.add(db_employee)
        db.commit()
        # 2. refresh carica gli attributi generati dal DB (come l'id o i default)
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        db.rollback()  # Annulla tutto se qualcosa va storto (es. department_id inesistente)
        raise e

# creo un badge associandolo a un dipendente tramite id
def create_badge(db: Session, badge: schemas.BadgeCreate):
    employee_id = badge.employee_id
    employee = db.query(models.Employee).filter(models.Employee.employee_id ==
                                         employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Dipendente con id {employee_id} non trovato ")
    db_badge = models.Badge(**badge.model_dump())

    try:
        db.add(db_badge)
        db.commit()
        db.refresh(db_badge)
        return db_badge
    except Exception as e:
        db.rollback()
        raise e

# restituire un dipendente con un join automatico sul badge
def get_employee(db: Session, employee_id: int):
    # Eseguo una JOIN semplice (INNER JOIN) tra Employee e Badge
    return db.query(models.Employee).join(models.Badge)\
        .filter(models.Employee.employee_id == employee_id).first()
