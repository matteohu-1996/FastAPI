from pydantic import BaseModel
from typing import Optional, List
from datetime import date as date_time
from models import InvoiceStatus

# schemi per i TAG
class TagBase(BaseModel):
    name: str
    color: str = "#CCCCCC" # diamo un grigio default

class TagCreate(TagBase): # non aggiungiamo niente dal TagBase
    pass

class Tag(TagBase):
    tag_id: int
    class Config:
        from_attributes = True

# schemi per gli ITEM
class InvoiceItemBase(BaseModel): # che eredita opportunamente
    description: str
    quantity: float
    unit_price: float

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    item_id: int
    invoice_id: int

    class Config:
        from_attributes = True

# schemi per le INVOICE
class InvoiceBase(BaseModel):
    number: str
    date: date_time
    status: InvoiceStatus = InvoiceStatus.DRAFT

class InvoiceCreate(InvoiceBase):
    client_id: int
    tags_ids: List[int] = [] # ci mettiamo solamente una lista di id dei tag
    # che associamo alla fattura

class InvoiceResponse(InvoiceBase):
    invoice_id: int
    client_id: int # completamente opzionale
    # todo: includere tutti i dati del cliente
    items: List[InvoiceItem] = []

    tags: List[Tag] = []
    total_amount: float

    class Config:
        from_attributes = True

# schemi dei CLIENT
class ClientBase(BaseModel):
    name: str
    vat_number: str
    email: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    client_id: int
    class Config:
        from_attributes = True