from fastapi import FastAPI
from routers import bookings, admin

app = FastAPI(
    title="Mini Cinema API",
    description="Mini API per la gestione di una sala del Minicinema",
    version="1.0"
)

app.include_router(
    bookings.router,
    prefix="/bookings",
    tags=["Prenotazioni", "Consultazione"]
)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)

