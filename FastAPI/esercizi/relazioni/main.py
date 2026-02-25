from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud

# Inizializzazione delle tabelle
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dipendenza database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/departments/", response_model=schemas.DepartmentResponse)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db=db, department=department)

@app.post("/employees/", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

@app.post("/badges/", response_model=schemas.Badge)
def create_badge(badge: schemas.BadgeCreate, db: Session = Depends(get_db)):
    return crud.create_badge(db=db, badge=badge)

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeResponse)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    # Cerco il dipendente direttamente nel database per assicurarmi di avere l'oggetto Employee
    # che contiene le relazioni con badge e department (JSON annidato)
    db_employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Dipendente non trovato")
    
    return db_employee
