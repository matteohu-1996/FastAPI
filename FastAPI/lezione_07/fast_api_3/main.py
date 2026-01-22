from fastapi import FastAPI
from routers import users, items

# Come sempre istanziamo l'oggetto di classe FastAPI
app = FastAPI(
    title="Esempio 3 di FastAPI",
    description="Semplice API che si occupa di spiegare il funzionamento dei routers",
    version="1.0.0"
)

# Root dell'APPLICAZIONE
@app.get("/")
def root():
    return {"message": "visita --- per vedere gli utenti o ---- per ottenere gli item"}

# Collegamento ai router
# 1. Router utenti
app.include_router(
    users.router,
    prefix="/users",
    tags=['Utenti']
)

# 2. Router items
app.include_router(
    items.router,
    prefix="/items",
    tags=["Items"]
)










