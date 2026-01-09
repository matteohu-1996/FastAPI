from fastapi import FastAPI, HTTPException

app = FastAPI() #istanziamo un oggetto classe FastAPI che si occuperà di gestire tutta la nostra applicazione server

# creiamo il dizionario che terrà i nostri dati
MENU = {
    1:{"nome": "Carbonara", "prezzo": 14.0},
    2:{"nome": "Tiramisù", "prezzo": 7.0},
    3:{"nome": "Tagliata di manzo", "prezzo": 27.50},
    4:{"nome": "Acqua naturale", "prezzo": 1.50},
}

# 1 Endpoint base -> ROOT
@app.get("/")
def get_info_ristorante():
    #FastAPI si preoccupa al posto nostro di convertire il dizionario in JSON e di gestire la coda del server
    return {
        "nome": "Ristorante Immaginazione",
        "luogo": "via Carlo Alberto 22/A",
        "orari": [
            {"lun-ven": ["09:00-12-00", "15:00-21:00"]},
            {"sab-dom": ["11:00-12-00", "18:00-21:00"]}
        ]
    }

@app.get("/menu")
def get_menu():
    return MENU
@app.get("/menu/{id_piatto}")
def get_piatto_da_id(id_piatto: int):
    # FastAPI si preoccuperà di convertire il numero scritto in formato stringa nell'URL al formato numero int

    # Gestiamo il caso in cui l'id del piatto non è presente
    if id_piatto not in MENU:
        raise HTTPException(
            status_code=404,
            detail=f"Non esiste un piatto con id {id_piatto}"
        )
    return MENU[id_piatto]

# provare a fare funzione che restituisca solo i piatti che costano meno di un prezzo dato
@app.get("/menu/under/{prezzo_max}")
def get_under_prezzo_max(prezzo_max: float):
    lista_piatti = []
    for piatto in MENU.values():
        if piatto["prezzo"] < prezzo_max:
            lista_piatti.append(piatto)
    return lista_piatti
