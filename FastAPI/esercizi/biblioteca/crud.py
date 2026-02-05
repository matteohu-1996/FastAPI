from sqlalchemy.orm import Session
import models, schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.create_author(
        name=author.name,
        books=author.books
    )
    db.add(db_author)

    db.commit()

    db.refresh(db_author)

    return db_author

def create_books(db: Session, books: schemas.BooksCreate):
    db_books = models.create_books(
        title=books.title,
        pages=books.pages,
    )