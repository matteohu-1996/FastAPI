from pydantic import BaseModel
from typing import List, Optional

# partiamo dagli schemi con meno dipendenze = commenti
class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    # per creare un nuovo commento ci serve l'id del post di riferimento
    post_id: int

class Comment(CommentBase):
    comment_id: int
    post_id: int
    class Config:
        from_attributes = True

# schemi dei post
class PostBase(BaseModel):
    title: str
    body: str

class PostCreate(PostBase):
    # per creare un post ci serve l'id del proprietario
    user_id: int

class Post(PostBase): # questa la usiamo per rispondere alle richieste
    post_id: int
    user_id: int
    comments: List[Comment] = [] # mettiamo la lista di commenti, di default vuota
    class Config:
        from_attributes = True

# Provare a fare le 3 classi analoghe per gli utenti, sapendo che un utente
# viene creato con la mail
# Per la classe UserBase, pensare ai parametri/o che sono sempre presenti
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    posts: List[Post] = [] # di default un utente non ha post finché non ne
    # crea uno
    class Config:
        from_attributes = True
