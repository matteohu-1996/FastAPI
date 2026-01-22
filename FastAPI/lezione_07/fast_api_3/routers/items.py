from fastapi import APIRouter, HTTPException

# Istanziamo un oggetto di classe APIRouter che gestirà le rotte degli items
router = APIRouter()

# Fake items
items_db = [
    {"id": 1, "name": "Mouse", "price": 12.5},
    {"id": 2, "name": "Tastiera", "price": 22.7},
    {"id": 3, "name": "Monitor", "price": 119.3},
    {"id": 4, "name": "Auricolari", "price": 39.5},
    {"id": 5, "name": "Microfono", "price": 27.89},
]

@router.get("/")
def get_items():
    """
    Restituisce tutti gli item presenti nel "DB"
    :return: {id: int, name: str, price: float}
    """
    return items_db

@router.get("/{item_id}")
def get_item(item_id: int):
    """
    Cerca e restituisce l'item con id passato
    :param item_id: ID da cercare nel "db"
    :return: {id: int, name: str, price: float}
    """
    for row in items_db:
        if row['id'] == item_id:
            return row

    raise HTTPException(
        status_code=404,
        detail=f"L'item con id {item_id} non esiste"
    )