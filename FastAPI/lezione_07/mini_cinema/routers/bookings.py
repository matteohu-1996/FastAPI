import matplotlib.pyplot as plt
from fastapi import APIRouter, HTTPException
from database import cinema_hall, rows
import math

a = cinema_hall

router = APIRouter()

# 1. Facciamo l'endpoint di root in cui spieghiamo il router
@router.get("/")
def booking_root():
    return {
        "message": "Visita /seats per i posti o /book/{seat_id} per prenotare un posto"
    }

# 2. Facciamo l'endpoint che fornisce la lista dei posti liberi disponibili
@router.get("/seats")
def get_available_seats():
    """
    Restituisce tutti i posti liberi disponibili o lista vuota se finiti
    """
    return [row for row in cinema_hall if not row['is_booked']]
    # per row si intende la riga del DB e non della sala

#todo fare un metodo get allo stesso endpoint che dica se il posto è libero o no
@router.post("/book/{seat_id}")
def book_seat(seat_id: str):
    # 1. Rendere l'id tutto maiuscolo (normalizzazione input)
    seat_id = seat_id.upper()

    # 2. Cerca il posto nella lista
    target_seat = None  # variabile che usiamo per mettere l'indice del nostro
    # posto nella lista (se lo troviamo)

    for i, row in enumerate(cinema_hall):
        if row['id'] == seat_id:
            # 2.1 Se lo trovi, segnalo come esistente
            target_seat = i
            break  # Se abbiamo trovato il posto, non serve continuare a cercare

    # 3. Se il posto non esiste, dai errore 404
    if not target_seat: # Non lo abbiamo trovato, è rimasto None
        raise HTTPException(
            status_code=404,
            detail=f"Il posto {seat_id} non è presente in sala"
        )

    # 4. Se il posto è prenotato, dai errore 409 (conflict)
    if cinema_hall[target_seat]['is_booked']:
        raise HTTPException(
            status_code=409,
            detail=f"Il posto {seat_id} è già occupato"
        )

    # 5. Effettua la prenotazione e dai conferma
    cinema_hall[target_seat]['is_booked'] = True

    return {
        "message": f"Il posto {seat_id} è stato prenotato con successo"
    }

# 3. Facciamo una funzione che dia il miglior posto disponibile
@router.get("/seats/best")
def get_best_seat():
    # TODO: importare anche rows e cols dal file con cinema_hall
    # TODO: far mettere all'utente un indice di tolleranza (alto, medio, basso)
    # 1 calcoliamo i parametri da passare alla funzione gaussiana
    media = (rows - 1) / 2
    varianza = (rows - 1 - media ) / 3 # todo rendere "variabile" il 3

    # 2 calcoliamo il punteggio di gradimento
    # 2.1 otteniamo i posti liberi
    posti_liberi = [posto for posto in cinema_hall if not posto['is_booked']]

    # 2.2 calcoliamo il nostro punteggio su ogni posto
    punteggio_max = (-1, -1)
    i_max = 0
    for i,posto in enumerate(posti_liberi):
        x = posto["number"] - 1
        punteggio_col = gaussiana(media, varianza, x)

        r = posto["row"]
        punteggio_row = ord(r) - 65

        if punteggio_col > punteggio_max[0]:
            punteggio_max = (punteggio_col, punteggio_row)
            i_max = i
        elif punteggio_col == punteggio_max[0] and punteggio_row > punteggio_max[1]:
            punteggio_max = (punteggio_col, punteggio_row)
            i_max = i

    if punteggio_max[0] != -1:
        # abbiamo trovato almeno un posto libero
        return cinema_hall[i_max]

    return {"message": "Non ci sono posti disponibili"}

def gaussiana(media: float, var: float, x: float):
    primo_blocco = 1 / (var * math.sqrt(2 * math.pi))
    esponente = - (x - media) ** 2 / (2 * var ** 2)

    return primo_blocco * math.exp(esponente)

# def print_grafico(m: float, v: float):
    asse_x = [i for i in range(10)]
    asse_y = [gaussiana(m,v,punto) for punto in asse_x]

    # fare il grafico
    plt.plot(asse_x,asse_y)
    plt.show()

# if __name__ == "__main__":
    # media + var * 3 = fila_max => var = (fila_max - media) / 3
    fila_max = 10
    m = (fila_max - 1) / 2
    v = (fila_max -1 - m) / 5

