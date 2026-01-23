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
    nuovi_dati = init_cinema()
    cinema_hall.clear() # puliamo la lista ma manteniamo lo stesso indirizzo in memoria
    cinema_hall.extend(nuovi_dati) # aggiungiamo i dati nuovi allo stesso indirizzo in memoria
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
def conta_prenotati(lista_posti: list[dict]) -> int:
    tot_prenotati = 0
    for posto in lista_posti:
        if posto["is_booked"]:
            tot_prenotati += 1
    return tot_prenotati

# 2 fare una funzione che dati dei conteggi da quella sopra [e il numero] dica la media
def media_di_gruppi(gruppi: list[list[dict]]) -> float:
    lista_totali = []
    for gruppo in gruppi:
        totale_gruppo = conta_prenotati(gruppo)
        lista_totali.append(totale_gruppo)
    return sum(lista_totali) / len(lista_totali)
# todo fare la media con un solo for (abbastanza implicito- list comprehension)


# 2.5 facciamo una funzione che estragga righe o colonne della sala dai dati
def raggruppa(tipo="colonna"):
    #controlliamo che il tipo sia tra quelli disponibili, senò diamo errore
    assert tipo in {"colonna", "riga"}, "Il tipo di raggruppamento deve essere 'riga' o 'colonna'"
    gruppi = {}

    for record in cinema_hall:
        chiave = record["number" if tipo == "colonna" else "row"] # otteniamo il nome della colonna/riga del posto corrente
        # cerchiamo di prendere il gruppo con la stessa colonna dal dizionario
        gruppo = gruppi.get(chiave, [])
        gruppo.append(record)  # aggiungiamo il posto corrente all'elenco
        gruppi[chiave] = gruppo # sovrascriviamo l'elenco nel dizionario

    return gruppi

# 3 applicare queste funzioni sia alle righe che alle colonne [da ottenere]
@router.get("/stats")
def calcola_stats():
    righe = raggruppa("riga")
    colonne = raggruppa("colonna")

    media_righe = media_di_gruppi(value for value in righe.values()) # convertiamo dizionario in liste
    media_colonne = media_di_gruppi(value for value in colonne.values())

    conteggi_righe = {chiave: conta_prenotati(valore) for chiave, valore in righe.items()}
    conteggi_colonne = {chiave: conta_prenotati(valore) for chiave, valore in colonne.items()}
    #todo fare una funzione aggrega che data una tipologia di raggruppamento faccia i 3 passaggi sopra

    return {
        "righe": {
            "media": media_righe,
            "conteggi": conteggi_righe
        },
        "colonne": {
            "media": media_colonne,
            "conteggi": conteggi_colonne
        },
    }

