from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    books = relationship("Book", back_populates="author")
class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey('author.id'))
    writer = relationship("Author", back_populates="books")