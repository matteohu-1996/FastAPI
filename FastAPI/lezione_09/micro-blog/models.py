# abbiamo da gestire un micro-blog in cui ci sono utenti che postano post che
# poi possono essere commentati (anonimamente).
# ogni post ha un solo autore (noto), ogni post può avere tanti commenti,
# ma ogni commenti è riferito solo a un post

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from  database import Base

class User(Base):
    # definiamo il nome della tabella
    __tablename__ = "users"

    # definiamo colonne e tipologie/specifiche
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)

    # definiamo le relazioni
    posts = relationship("Post", back_populates="owner")
    # definiamo la relazione che c'e tra classe User (tabella users) e la
    # classe Post (tabella posts).
    # back_populates crea un link bidirezionale tra post e user: anche post
    # saprà a chi appartiene

class Post(Base):
    # nome tabella
    __tablename__ = "posts"

    # colonne e specifiche
    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    body = Column(String(5000))

    # chiave esterna che collega alla tabella users
    user_id = Column(Integer, ForeignKey("users.user_id"))

    # relazioni
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    # nome tabella
    __tablename__ = "comments"

    # colonne e specifiche
    comment_id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500))

    # chiave esterna collega alla tabella dei post
    post_id = Column(Integer, ForeignKey("posts.post_id"))

    # relazioni
    post = relationship("Post", back_populates="comments")

