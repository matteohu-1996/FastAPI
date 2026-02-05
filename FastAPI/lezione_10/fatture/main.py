from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import models, schemas, crud
from database import SessionLocal, engine

# todo organizzare meglio la struttura delle cartelle/file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestore di base delle fatture ",
    description="Piccola API per la gestione semplificata delle fatture di "
                "una sola partita IVA",
    version="1.0.0",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------- ENDPOINT ------------------------
# Endpoint per la creazione di una nuova fattura
@app.post("/invoices", response_model=schemas.InvoiceResponse)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    return crud.create_invoice(db, invoice=invoice)


# Endpoint per inserire gli items
@app.post("/invoices/{invoice_id}/items", response_model=schemas.InvoiceItem)
def add_item_to_invoice(
    invoice_id: int,
    item: schemas.InvoiceItemCreate,
    db: Session = Depends(get_db),
):
    return crud.create_invoice_item(db=db, item=item, invoice_id=invoice_id)

@app.get("/invoices/{invoice_id}", response_model=schemas.InvoiceResponse)
def read_invoice_by_id(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = crud.get_invoice_by_id(db, invoice_id)
    if not db_invoice:
        raise HTTPException(status_code=404, detail=f"Fattura con id "
                                                    f"{invoice_id}")
    return db_invoice
