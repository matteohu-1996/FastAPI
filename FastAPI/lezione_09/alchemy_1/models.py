# dentro questo file definiamo la struttura del database

from sqlalchemy import Column,Integer,String, Boolean
from database import Base

class Note(Base):
    # 1 definiamo il nome della tabella all'interno del DB
    __tablename__ = 'notes'
    # 2 definiamo le colonne e le rispettive tipologie/specifiche
    id_note = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(500))
    is_active = Column(Boolean, default=True)

