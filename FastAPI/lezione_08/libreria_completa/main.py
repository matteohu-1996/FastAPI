from fastapi import FastAPI,APIRouter,HTTPException
from routers import authors, books
from pydantic import BaseModel # questo è cio che usiamo per i controlli
from typing import List # questo è cio che usiamo per i controlli

router = APIRouter()

app = FastAPI(
    title="Libreria più bella",
    description="Seconda Implementazione dell'API delle libreria con Pydantic",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Vai su /docs per testare l'API"
    }
app.include_router(
    authors.router,
    prefix="/authors",
    tags=["Autori"]
)
app.include_router(
    books.router,
    prefix="/books",
    tags=["Libri"]
)