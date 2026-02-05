from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import date


def seed_db():
    # PASSO 0: Creazione della struttura (DDL)
    # Questo comando trasforma le nostre classi Python (models.py) in tabelle reali nel database.
    # Se le tabelle esistono gia', non fa nulla.
    models.Base.metadata.create_all(bind=engine)

    # Apriamo una sessione. La sessione e' la nostra "area di lavoro" temporanea.
    db = SessionLocal()

    try:
        # PASSO 1: Controllo Idempotenza
        # Verifichiamo se il database contiene gia' dei dati per evitare di creare duplicati
        # ogni volta che lanciamo lo script.
        if db.query(models.Client).first():
            print("[INFO] Il database contiene gia' dei dati. Operazione annullata.")
            return

        print("[INFO] Inizio il popolamento del database...")

        # PASSO 2: Creazione delle Entita' Indipendenti (Tag)
        # I Tag non dipendono da nessuno, quindi li creiamo per primi.
        tag_python = models.Tag(name="Backend Python", color="#3776AB")
        tag_react = models.Tag(name="Frontend React", color="#61DAFB")
        tag_ai = models.Tag(name="AI & LLM", color="#FFD700")
        tag_pagato = models.Tag(name="Saldato", color="#28A745")
        tag_urgente = models.Tag(name="Urgente", color="#DC3545")
        tag_devops = models.Tag(name="DevOps & Cloud", color="#FF5733")

        # Li aggiungiamo alla sessione (in memoria)
        db.add_all([tag_python, tag_react, tag_ai, tag_pagato, tag_urgente, tag_devops])
        # Eseguiamo il commit per salvare fisicamente i Tag e generare i loro ID
        db.commit()
        print("[OK] Tags creati con successo.")

        # PASSO 3: Creazione dei Clienti
        # Anche i clienti sono entita' principali. Serviranno come chiavi esterne per le fatture.
        client_startup = models.Client(
            name="NextGen StartUp SRL",
            vat_number="12345678901",
            email="amm@nextgen.it"
        )
        client_studio = models.Client(
            name="Studio Legale Rossi",
            vat_number="98765432109",
            email="info@studiorossi.com"
        )
        client_pm = models.Client(
            name="Big Corp SpA",
            vat_number="11223344556",
            email="procurement@bigcorp.com"
        )
        client_logistica = models.Client(
            name="EcoLogistics Scarl",
            vat_number="55667788990",
            email="admin@ecologistics.eu"
        )

        db.add_all([client_startup, client_studio, client_pm, client_logistica])
        db.commit()
        print("[OK] 4 Clienti creati con successo.")

        # PASSO 4: Creazione Fatture con Relazioni Complesse
        # Qui gestiamo contemporaneamente:
        # 1. Relazione 1-a-Molti (Cliente -> Fatture)
        # 2. Relazione 1-a-Molti (Fattura -> Righe/Items)
        # 3. Relazione Molti-a-Molti (Fattura <-> Tag)

        invoices = []

        # FATTURA 1
        # Colleghiamo la fattura al cliente usando 'client_id' (che ora esiste grazie al commit precedente).
        inv_1 = models.Invoice(number="1/2024", date=date(2024, 1, 15), status=models.InvoiceStatus.PAID,
                               client_id=client_startup.id)

        # Popoliamo le righe (Items). SQLAlchemy gestira' le chiavi esterne automaticamente.
        inv_1.items = [
            models.InvoiceItem(description="Sviluppo API Backend (FastAPI)", quantity=20, unit_price=60.0),
            models.InvoiceItem(description="Interfaccia Dashboard (React)", quantity=15, unit_price=60.0),
            models.InvoiceItem(description="Deployment su VPS", quantity=2, unit_price=80.0)
        ]

        # Assegniamo i Tag. Essendo una relazione Molti-a-Molti, passiamo una lista di oggetti Python.
        # SQLAlchemy riempira' automaticamente la tabella di associazione 'invoice_tags'.
        inv_1.tags = [tag_python, tag_react, tag_pagato]
        invoices.append(inv_1)

        # FATTURA 2
        inv_2 = models.Invoice(number="2/2024", date=date(2024, 2, 10), status=models.InvoiceStatus.ISSUED,
                               client_id=client_studio.id)
        inv_2.items = [
            models.InvoiceItem(description="Analisi fattibilità RAG per documenti", quantity=8, unit_price=90.0),
            models.InvoiceItem(description="Setup ambiente locale LLM", quantity=4, unit_price=90.0)
        ]
        inv_2.tags = [tag_ai, tag_urgente]
        invoices.append(inv_2)

        # FATTURA 3
        inv_3 = models.Invoice(number="3/2024", date=date(2024, 3, 1), status=models.InvoiceStatus.DRAFT,
                               client_id=client_pm.id)
        inv_3.items = [models.InvoiceItem(description="Formazione Team su Python/Pandas", quantity=1, unit_price=400.0)]
        inv_3.tags = [tag_python]
        invoices.append(inv_3)

        # FATTURA 4
        inv_4 = models.Invoice(number="4/2024", date=date(2024, 3, 5), status=models.InvoiceStatus.PAID,
                               client_id=client_logistica.id)
        inv_4.items = [
            models.InvoiceItem(description="Refactoring modulo spedizioni", quantity=12, unit_price=65.0),
            models.InvoiceItem(description="Ottimizzazione Query MySQL", quantity=3, unit_price=75.0)
        ]
        inv_4.tags = [tag_python, tag_pagato]
        invoices.append(inv_4)

        # FATTURA 5
        inv_5 = models.Invoice(number="5/2024", date=date(2024, 3, 20), status=models.InvoiceStatus.PAID,
                               client_id=client_startup.id)
        inv_5.items = [models.InvoiceItem(description="Canone manutenzione mensile", quantity=1, unit_price=150.0)]
        inv_5.tags = [tag_pagato, tag_devops]
        invoices.append(inv_5)

        # FATTURA 6
        inv_6 = models.Invoice(number="6/2024", date=date(2024, 4, 2), status=models.InvoiceStatus.ISSUED,
                               client_id=client_studio.id)
        inv_6.items = [
            models.InvoiceItem(description="Sviluppo Chatbot v1.0", quantity=25, unit_price=85.0),
            models.InvoiceItem(description="Integrazione API OpenAI", quantity=5, unit_price=85.0)
        ]
        inv_6.tags = [tag_ai, tag_react]
        invoices.append(inv_6)

        # FATTURA 7
        inv_7 = models.Invoice(number="7/2024", date=date(2024, 4, 10), status=models.InvoiceStatus.DRAFT,
                               client_id=client_logistica.id)
        inv_7.items = [
            models.InvoiceItem(description="Prototipo App Driver (React Native)", quantity=40, unit_price=70.0)]
        inv_7.tags = [tag_react, tag_urgente]
        invoices.append(inv_7)

        # FATTURA 8
        inv_8 = models.Invoice(number="8/2024", date=date(2024, 4, 15), status=models.InvoiceStatus.PAID,
                               client_id=client_pm.id)
        inv_8.items = [
            models.InvoiceItem(description="Script automazione Excel -> DB", quantity=6, unit_price=80.0),
            models.InvoiceItem(description="Debug script legacy", quantity=2, unit_price=80.0)
        ]
        inv_8.tags = [tag_python, tag_pagato]
        invoices.append(inv_8)

        # FATTURA 9
        inv_9 = models.Invoice(number="9/2024", date=date(2024, 5, 1), status=models.InvoiceStatus.ISSUED,
                               client_id=client_startup.id)
        inv_9.items = [models.InvoiceItem(description="Fix critico login Auth0", quantity=3, unit_price=100.0)]
        inv_9.tags = [tag_react, tag_urgente]
        invoices.append(inv_9)

        # FATTURA 10
        inv_10 = models.Invoice(number="10/2024", date=date(2024, 5, 5), status=models.InvoiceStatus.DRAFT,
                                client_id=client_studio.id)
        inv_10.items = [models.InvoiceItem(description="Consulenza Privacy e AI Act", quantity=2, unit_price=120.0)]
        inv_10.tags = [tag_ai]
        invoices.append(inv_10)

        # PASSO 5: Persistenza Finale
        # Aggiungiamo tutte le fatture (che contengono al loro interno gli items e le relazioni con i tag)
        db.add_all(invoices)

        # Il commit finale salva tutto in un'unica transazione. Se qualcosa fallisce, nulla viene salvato.
        db.commit()
        print("[OK] 10 Fatture con relative righe e tag inserite con successo.")

        print("\n[SUCCESSO] Procedura di seeding completata.")

    except Exception as e:
        print(f"[ERRORE] Si e' verificato un problema durante il seeding: {e}")
        # Rollback annulla tutte le modifiche pendenti in caso di errore
        db.rollback()
    finally:
        # Chiudiamo sempre la connessione alla fine
        db.close()


if __name__ == "__main__":
    seed_db()