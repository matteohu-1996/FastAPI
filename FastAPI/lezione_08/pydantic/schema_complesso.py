"""
Gestiamo il catalogo dei film del nostro cinema.
Ogni film ha titolo, regista, durata, attori (>0), voto, imdb
Vogliamo gestire l'inserimento nel programma del nostro cinema di film nuovi e togliere quelli "vecchi" [admin]
Del regista sappiamo nome e cognome, come degli attori

Ogni giornata ha in programma i 3 migliori film attivi per voto imdb

[admin]
La nostra dashboard ci deve permette di inserire/eliminare film, registi e attori



"""
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

class Film (BaseModel):
    title: str
    regista: str
    durata: int
    attori: str
    voto: int
    imdb: float

class Regista (BaseModel):
    id: int
    nome: str
    cognome: str
    nome: str
    cognome: str

class Attori (BaseModel):
    id: int
    nome: str
    cognome: str