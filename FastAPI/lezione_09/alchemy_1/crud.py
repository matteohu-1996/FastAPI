from fastapi import FastAPI
from sqlalchemy.orm import Session
import models, schemas

# facciamo le funzioni che ci servono per interagire col DB
# 1 scriviamo la funzione per ottenere una nota
def get_note(db: Session, id_note: int): # il parametro "db" che viene
# passato alla funzione è di tipo Session
    return db.query(models.Note).filter(models.Note.id_note == id_note).first()
    # db.query() seleziona la tabella (e/o le colonne)
    # .filter() applichiamo un WHERE
    # .first() otteniamo solamente il primo risultato

# 2 scriviamo la funzione che ottiene tutte le note
def get_notes(db: Session, skip: int = 0, limit: int = 100):
    # skip e limit vanno a limitare e gestire il numero di record che
    # restituisce contemporaneamente a chi ha fatto richiesta, non è quasi mai
    # necessario ottenere tutto ciò che abbiamo ma possiamo suddividere la nostra
    # risposta in blocchi a partire da numero "skip" per "limit" record
    return db.query(models.Note).offset(skip).limit(limit).all()
    # db.query() fa lo stesso di prima chiede una tabella
    # .offset(skip) stacchiamo dalla risposta i primi "skip" elementi


    # .all() restituiamo la risposta tutta insieme

def create_note(db: Session, note: schemas.NoteCreate):
    # 1 creiamo l'istanza del modello SQLAlchemy
    db_note = models.Note(
        title=note.title,
        content=note.content
    )

    # 2 aggiungiamo la nota alla sessione
    db.add(db_note)

    # 3 facciamo il commit della modifica (salviamo effettivamente la modifica
    # nel disco)
    db.commit()

    # 4 facciamo il refresh del DB "in RAM" per ottenere l'id della nota
    # appena salvata
    db.refresh(db_note)

    # 5 restituire
    return db_note

