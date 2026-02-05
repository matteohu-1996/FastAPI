from sqlalchemy.orm import Session
import models, schemas

# funzioni di creazione
def create_user(db: Session, user: schemas.UserCreate):
    # 1 istanziamo un nuovo user per il db
    db_user= models.User(email=user.email)

    # 2 inseriamo l'oggetto nel database
    db.add(db_user) # questo inserimento per ora è solo nella ram

    # 3 "attualiziamo" l'inserimento salvandolo nel db nel disco fisso
    db.commit()

    # 4 refreshamo il db nella ram per ottenere l'istanza completa
    db.refresh(db_user)

    # returniamo la riga creata
    return db_user

def create_post(db: Session, post: schemas.PostCreate):
    db_post= models.Post(**post.model_dump()) # post.model_dump() o
    # post.dict() convertono l'oggetto in dizionario

    # post = {"title": title, "body": corpo, "user_id": 3}
    # funz(**post) = funz(title="titolo", body="corpo", user_id="3")
    # funz ("prova", "body prova", user_id=6)

    db.add(db_post)
    db.commit()

    db.refresh(db_post)
    return db_post

def create_comments(db: Session, comment: schemas.CommentCreate):
    db_comment= models.Comment(**comment.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# otteniamo un utente da id
def get_user(db: Session, user_id: int):
    # in base a come abbiamo scritto model e schemas, SQLAlchemy capisce da
    # solo che bisogna fare una join con le altre tabelle, non serve
    # dirglielo esplicitamente come invece dobbiamo fare nella funzione sotto
    return db.query(models.User).filter(models.User.id == user_id).first()

# Query: voglio ottenere tutti i commenti sotto i post di un certo utente da id
def get_comments_by_user_id(db: Session, user_id: int):
    # .join() uniamo le tabelle del db, l'unione viene fatta automaticamente
    # sugli id dichiarati nelle ForeignKey e nelle relationship
    return db.query(models.Comment)\
        .join(models.Post)\
        .join(models.User)\
        .filter(models.User.user_id == user_id)\
        .all()
        # .limit()

