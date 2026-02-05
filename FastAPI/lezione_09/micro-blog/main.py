from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import engine, SessionLocal

# ------------- CONFIG ---------------


# 1 creiamo le tabelle se non presenti
# solo in server asincroni
models.Base.metadata.create_all(bind=engine)

# 2 istanziamo la app
app = FastAPI(
    title="Micro Blog API",
    description="Mini API per la gestione con SQLAlchemy di un micro-blog",
    version="1.0.0",
)

# 3 creiamo la funzione che fa da dipendenza per creare le sessioni da db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------- ENDPOINT ---------------
# 1 creiazione utente
@app.post("/users/new", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_users(db=db, user=user)

# 2 endpoint /posts/new
@app.post("/posts/new", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_posts(db=db, post=post)

# 3 /comments/new
@app.post("/comments/new", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comments(db=db, comment=comment)

# 4 endpoint che restituisce l'utente completo da id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id) # proviamo a ottenere i
    # dati
    if not db_user: # if db_user is None
        raise HTTPException(status_code=404, detail=f"Utente con id {user_id} non trovato")
    return db_user

# 5 endpoint che restituisce i commenti sotto i post di un utente
@app.get("/users/{user_id}/comments", response_model=List[schemas.Comment])
def read_user_comments_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_user_id(db=db, user_id=user_id)


