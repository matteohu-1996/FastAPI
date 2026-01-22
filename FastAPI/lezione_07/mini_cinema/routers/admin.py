from fastapi import APIRouter, HTTPException
from numpy.ma.core import count

import database
from database import cinema_hall, init_cinema, rows, cols
import random

random.seed(42)

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Benvenuto nel router di admin. Gli endpoint sono..."}

#todo: facciamo un endpoint /random che sceglie un numero casuale di posti casuali e li prenota
# prima di estrarre, prenotare etc, resettiamo cinema_hall (c'è una funzione da qualche parte)
# random.choice sceglie uno o più elementi di una lista e random.sample sceglie un sottoinsieme casuale della lista

@router.post("/random-seed")
def random_seed():
    # 0 resettiamo cinema_hall
    database.cinema_hall = init_cinema().copy
    # per chiarezza, facciamo riferimento esplicito al file database per la nuova assegnazione

    # 1 troviamo il numero (casuale) di posti da prenotare
    n_posti = random.randint(1, rows * cols)

    # 2 scegliamo un sottoinsieme dei posti e li "prenotiamo"
    indici_da_prenotare = random.sample(range(rows * cols), n_posti)
    for indice in indici_da_prenotare:
        cinema_hall[indice]["is_booked"] = True

    # 3 restituiamo l'elenco completo
    return  {
        "prenotati": n_posti,
        "righe": rows,
        "colonne": cols,
        "database": cinema_hall
    }

#todo: facciamo un endpoint /stats che restituisce le seguenti statistiche:
# - riempimento per fila
# - riempimento medio della sala (per file)
# - lo stesso per colonne

# 1 fare una funzione che calcoli il conteggio di un insieme di posti
def conta_posti():
    for posti in cinema_hall:
        count(posti)

# 2 fare una funzione che dati dei conteggi da quella sopra [e il numero] dica la media
# 3 applicare queste funzioni sia alle righe che alle colonne [da ottenere]
