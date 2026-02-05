from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models,schemas,crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal() # istanziamo una sessione col nostro DB
    try:
        yield db    # promette di restituire una connessione col DB
    finally:
        db.close()
app = FastAPI(
    title="Esercizio Biblioteca",
    description="esercizio Biblioteca",
    version="1.0",
)

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.post("/books/")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_books(db=db, book=book)

