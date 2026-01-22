from fastapi import APIRouter, HTTPException

# Creiamo il nostro router istanziando l'APIRouter di fastapi
router = APIRouter()

# Creiamo un mini json con gli utenti
users_db = [
    {"id": 1, "username": "aabb", "password": "123", "role": "admin"},
    {"id": 2, "username": "bbcc", "password": "456", "role": "user"},
    {"id": 3, "username": "ccdd", "password": "789", "role": "user"},
    {"id": 4, "username": "ddee", "password": "101", "role": "user"},
]

# Creiamo le rotte a cui risponde il nostro router (sono di fatto gli endpoint)
@router.get("/")  # Definiamo la rotta di "root"
def get_users():
    """
    Restituisce tutti gli utenti disponibili (senza pw)
    :return: [{id: str, username: str, role: str}, ...]
    """
    lista_output = []
    for row in users_db:
        row = row.copy()  # Rendiamo indipendente la nostra riga dalla lista originale
        del row['password']  # Togliamo la coppia "password" valore dalla riga
        lista_output.append(row)

    return lista_output

# Creiamo l'endpoint per restituire i dati di un utente (che non mette la pw)
@router.get("/{user_id}/me")
def read_user(user_id: int):
    """
    Cerca e restituisce i dati dell'utente con id passato
    :param user_id: ID dell'utente nel "db"
    :return: {id: str, username: str, password: str, role: str}
    """
    # Per ogni riga nel db, cerchiamo quella che ha id = user_id
    for row in users_db:
        if row['id'] == user_id:
            # Se la troviamo, interrompiamo il for, restituendo i dati dell'utente trovato
            return row

    # Se siamo usciti dal for, vuol dire che non abbiamo trovato l'id cercato, quindi
    # restituiamo un errore 404
    raise HTTPException(
        status_code=404,
        detail=f"L'utente con ID {user_id} non è stato trovato"
    )















