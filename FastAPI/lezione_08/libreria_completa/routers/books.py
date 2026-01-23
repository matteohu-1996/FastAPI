from fastapi import APIRouter, HTTPException
from typing import List
import schemas
import  db

router = APIRouter()

@router.get("/", response_model=List[schemas.LibroBase])
def get_books():
    return db.db_libri

@router.get("/complete", response_model=List[schemas.LibroCompleto])
def get_complete_books():
    # per ogni libro, cerchiamo l'autore e ne inseriamo i dati
    lista_completa = []
    for i, libro in enumerate(db.db_libri):
        for autore in db.db_autori:
            if autore["id"] == libro["id_author"]:
                libro["author_data"] = autore

        lista_completa.append(libro)
    return lista_completa

@router.get("/{book_id}", response_model=schemas.LibroCompleto)
def get_book(book_id: int):
    # 1 cerchiamo libro dall'id
    libro = None
    for book in db.db_libri:
        if book["id"] == book_id:
            libro = book
            break
    # 2 gestiamo il caso in cui non troviamo il libro (rimane None)
    if not libro:
        raise HTTPException(
            status_code=404,
            detail=f"Il libro con id {book_id} non trovato")
    # 3 cerchiamo l'autore
    autore = None
    for author in db.db_autori:
        if author["id"] == libro["id_author"]:
            autore = author
            break
    # 4 mettiamo insieme i dati e li restituiamo
    libro["author_data"] = autore
    return libro