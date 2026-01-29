from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models,schemas,crud
from database import SessionLocal, engine

# per primissima cosa, creiamo le tabelle necessarie se non sono presenti
models.Base.metadata.create_all(bind=engine)

# ATTENZIONE: se usate un server ASGI ASINCRONO (uvicorn) allora siete apposto
# Se invece usate un server WSGI SINCRONO (Gunicorn) questo comando non lo
# potete usare:
# Con i server WSGI, si vanno a istanziare "contemporaneamente" più "workers"
# che somigliano ai thread.
# All'avvio del server, ogni worker prova ad eseguire il comando
# contemporaneamente risultando in un crash del server

# Dependency: funzione che fornisce ad ogni richiesta una sessione col DB
def get_db():
    db = SessionLocal() # istanziamo una sessione col nostro DB
    try:
        yield db    # promette di restituire una connessione col DB
    finally:
        db.close()

# istanziamo la nostra app
app = FastAPI(
    title="Prima prova con SQLAlchemy",
    description="Mini API per interfaccia col DB",
    version="1.0",
)
# Facciamo un endpoint di tipo post per creare una nuova nota (prenderemo in
# input un oggetto che rispetti le specifiche dello schema)
@app.post("/notes", response_model=schemas.NoteComplete)
# Facciamo una funzione che prenda un oggetti con lo schema NoteCreate e una
# connessione al DB
# Ma la connessione al DB non viene "passata dal browser" ma creata
# attraverso la funzione get_db() che abbiamo scritto prima
# é come se obbligassimo a FastApi a prendere la "note" dalla richiesta e a
# richiedere una connessione al DB attraverso il nostro main
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    # chiamiamo la funzione crud e ne restituiamo il risultato
    return crud.create_note(db=db, note=note)

@app.get("/notes", response_model=List[schemas.NoteComplete])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_notes(db=db, skip=skip, limit=limit)
    return notes

@app.get("/notes/{id_note}", response_model=schemas.NoteComplete)
def read_note(id_note: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db=db, id_note=id_note) # cerchiamo di ottenere
    # la nota dal DB
    # se il DB non trova la nota, restituisce None
    if not db_note:
        raise HTTPException(status_code=404,
                            detail=f"Nota con id {id_note} non trovata")
    return db_note
