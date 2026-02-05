from sqlalchemy.orm import Session
import models, schemas

# -------------- TAGS -----------------
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tags(db: Session):
   return db.query(models.Tag).all()

# -------------- CLIENTS -----------------

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# todo: limitare i client ricevuti con offset limit

def get_clients(db: Session):
    return db.query(models.Client).limit(50).all()

# todo: fare una funzione che ottenga un client da id

# -------------- INVOICES -----------------

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    # 1 è necessario recuperare dalla fattura il campo con la lista di id dei
# tags
    tag_ids = invoice.tag_ids # 1.1 prendiamo dall'oggetto
    invoice_data = invoice.model_dump() # 1.2 estraiamo i dati dalla fattura
    invoice_data.pop("tag_ids") # rimuoviamo dal dizionario con i dati la
    # lista di tag

    # 2 creiamo la fattura di base
    db_invoice = models.Invoice(**invoice_data)

    # 3 cerchiamo nel db i tag corrispondenti agli id che abbiamo nella lista
    if tag_ids:
        # 3.1 facciamo la query per i nostri tag
        # select * from tags where tag_id IN ([lista di id])
        tags = db.query(models.Tag).filter(models.Tag.tag_ids.in_(tag_ids)).all()
        # con i riferimenti che abbiamo scritto in models.py SQLAlchemy
        # conosce la relazione e le tabelle necessarie per gestirla, infatti
        # andrà a popolare automaticamente la tabella di JOIN o (bridge) con
        # le chiavi di tag e fatture corrispondenti
        db_invoice.tags = tags

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

# todo: fare schema e funzione per ottenere un elenco di fatture

def get_invoice_by_id(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.invoice_id ==
                                           invoice_id).first()

# -------------- ITEMS -----------------
def create_invoice_item(db: Session, invoice: schemas.InvoiceItemCreate,
                        invoice_id: int):
    db_item = models.InvoiceItem(**invoice.model_dump(), invoice_id= invoice_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
