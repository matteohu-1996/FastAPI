# Simuliamo una sala cinema 5x5 (Righe A-E, Colonne 1-5)
# Esempio record: {"id": "A1", "row": "A", "number": 1, "is_booked": False}
import pprint

cinema_hall = []

rows = 5
cols = 5

def init_cinema():
    """Resetta la sala cinema allo stato iniziale (tutto libero)."""
    global cinema_hall
    cinema_hall = []
    for r in range(65, rows + 65):
        for c in range(1, cols + 1):
            cinema_hall.append({
                "id": f"{chr(r)}{c}",  # ID univoco es. "A1"
                "row": chr(r),
                "number": c,
                "is_booked": False
            })
    return cinema_hall

# Inizializziamo subito la sala
init_cinema()
pprint.pprint(cinema_hall)

# TODO: scrivere la funzione di sopra senza for esplcito (list comprehension)