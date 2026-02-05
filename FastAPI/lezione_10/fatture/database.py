from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# definiamo url di connessione al db
DATABASE_URL="mysql+pymysql://root:root@localhost:3306/fatture"

# definiamo l'engine
engine = create_engine(DATABASE_URL)

# definiamo il gestore di sessione
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# definiamo base per i modelli
Base = declarative_base()
