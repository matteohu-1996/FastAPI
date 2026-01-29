from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1 definiamo la stringa di connessione al DB
# DATABASE_URL = ("linguaggioSQL+motore://nome_utente:password_db@ip_host_db:porta_server_db/nome_db"
DATABASE_URL  = "mysql+pymysql://root:root@localhost:3306/micro_blog"

# 2 creiamo engine - ci connettiamo al DB e stabiliamo il necessario
engine = create_engine(DATABASE_URL)

# 3 creiamo il gestore di sessioni
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine) # colleghiamo il nostro engine ad
# ogni sessione, in pratica verrà usato l'engine che abbiamo creato prima per
# gestire/far funzionare ogni sessione

# 4 creiamo la classe che useremo per ereditare tutte le cose necessarie alla
# comunicazione con il DB dei nostri modelli
Base = declarative_base()
