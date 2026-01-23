from fastapi import FastAPI,APIRouter,HTTPException
from pydantic import BaseModel # questo è cio che usiamo per i controlli
from typing import List # questo è cio che usiamo per i controlli

# 1 facciamo il database "finto"
db_libreria = []

# 2 creiamo lo SCHEMA Pydantic
class Libro(BaseModel): # eredita la configurazione da BaseModel
    # questi parametri sono tutti obbligatori
    title: str
    author: str
    pages: int
    year: int
    price: float

class LibroOut(BaseModel):
    title: str
    author: str
    pages: int
    year: int

# 3 costruiamo il router
router = APIRouter()

@router.get("/", response_model=List[LibroOut])
# dichiariamo che il dalla funzione uscirà una lista di libri (con i dati dei libri)
def get_books():
    """
    restituisce l'elenco completo di libri con tutti i dati
    """
    return db_libreria

@router.post("/new", status_code=201)
# per la conferma useremo il codice 201 - Creato con successo
def create_book(new_book: Libro):
    """
    crea un nuovo libro nel database se i dati sono corretti
    il controllo viene fatto automaticamente da Pydantic
    :param new_book: oggetto di classe Libro
    """
    # Prima cosa controlliamo che il libro non esista già
    for libro in db_libreria:
        if libro["title"] == new_book.title and libro["author"] == new_book.author:
            raise HTTPException(
                status_code=409,
                detail=f"Il libro esiste già: id={libro["id"]}"
            )
    # inseriamo il nuovo libro nel DB
    id_libro = len(db_libreria) + 1
    dati_libro = new_book.model_dump() # converte l'oggetto in dizionario
    dati_libro["id"] = id_libro # aggiungiamo il dato dell'ID
    db_libreria.append(dati_libro) # lo aggiungiamo alla lista

    return {
        "message": "Libro creato con successo",
        "book": dati_libro
    }

# 4 creiamo l'app e colleghiamo il router
app = FastAPI(
    title="Primo esempio Pydantic",
    description="Versione base di un'API per la creazione di libri",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/book",
    tags=["Libri"]
)

@app.get("/")
def root():
    return {
        "message": "Vai su /docs per testare l'API"
    }
