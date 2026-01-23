from pydantic import BaseModel
from typing import List

# iniziamo facendo le classi di base
class AutoreBase(BaseModel):
    id: int
    name: str
    active: bool

class LibroBase(BaseModel):
    id: int
    title: str
    price: float
    id_author: int

# facciamo le classi per trasmettere le informazioni complete di libro e autore
class LibroCompleto(LibroBase): # andiamo ad aggiungere informazioni a quelle presenti in LibroBase
    author_data: AutoreBase

class AutoreConLibri(AutoreBase):
    books: List[LibroBase] = [] # diamo come valore di default una lista vuota