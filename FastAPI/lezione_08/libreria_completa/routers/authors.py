from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException
import schemas
import db
from db import db_autori

# istanziamo il router con FastAPI
router = APIRouter()

@router.post("/create", status_code=201)
def create_author(new_author: schemas.AutoreBase):
    # verifichiamo il duplicato
    # Any funzione che prende una lista e restituisce True se almeno un elemento corrisponde a True
    if any(autore["id"] == new_author["id"] for autore in db.db_autori):
        raise HTTPException(
            status_code=409,
            detail=f"L'autore con id '{new_author}' esiste già"
        )

    # se non abbiamo interrotto la funzione con un errore, salviamo l'autore nel DB
    author_data = new_author.model_dump()
    db.db_autori.append(author_data)

    return {
        "message": "L'autore è stato salvato con successo",
        "author": author_data
    }

# Endpoint per ottenere l'elenco di autori (senza libri
@router.get("/", response_model=List[schemas.AutoreBase])
def get_authors():
    return db.db_autori

@router.get("/id_author", response_model=schemas.AutoreConLibri)
def get_author_completo(id_author: int):
    # 1 cerchiamo di ottenere l'autore dal DB
    author = None
    for autore in db.db_autori:
        if autore["id"] == id_author:
            author = autore
            break

    # se author è rimasto None, vuol dire che l'autore non esiste
    if not author:
        raise HTTPException(
            status_code=404,
            detail=f"L'autore con ID {id_author} non esiste"
        )

    # 2 cerchiamo nel DB i libri che ha fatto(avranno id_author = a quello passato)
    books = [libro for libro in db.db_libri if libro["id"] == id_author] # List comprehension

    # 3 uniamo e restituiamo i dati
    author ["books"] = books
    return author

