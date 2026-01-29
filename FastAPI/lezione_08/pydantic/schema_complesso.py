"""
Gestiamo il catalogo dei film del nostro cinema.
Ogni film ha titolo, regista, durata, attori (>0), voto imdb
Vogliamo gestire l'inserimento nel programma del nostro cinema di film nuovi e togliere quelli "vecchi" [admin]
Del regista sappiamo nome e cognome, come degli attori

Ogni giornata ha in programma i 3 migliori film attivi per voto imdb

[admin]
La nostra dashboard ci deve permette di inserire/eliminare film, registi e attori



"""
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

class FilmBase (BaseModel):
    id: int
    title: str
    id_director: int
    ids_actor: List[int]
    duration: int # in secondi, va bene anche minuti
    imdb: float # voto del film

class RegistaBase (BaseModel):
    id: int
    name: str
    surname: str


class AttoreBase (BaseModel):
    id: int
    name: str
    surname: str

class FilmCompleto(BaseModel): # per come stiamo scrivendo il codice, questi
    # parametri sono obbligatori
    id: int
    title: str
    duration: int
    imdb: float
    director: RegistaBase # mettiamo in questo campo tutti i dati del regista
    actors: List[AttoreBase]

class FilmGiornata(BaseModel):
    lista_film: List[FilmCompleto] # perchè abbiamo in mente che nella home
    # del cinema si vedranno in dettaglio i film della giornata

