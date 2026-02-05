from typing import List

from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    pages: int

class BookCreate(BookBase):
    # quando creo un libri, devo dire di chi è?
    # Si: passiamo author_id qui
    author_id: int

class Book(BookBase):
    id: int
    author_id: int
    class Config:
        from_attributes = True

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = []
    class Config:
        from_attributes = True