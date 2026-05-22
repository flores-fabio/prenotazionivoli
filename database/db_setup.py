import pymysql

# ⚠️ MODIFICA QUESTI VALORI con i tuoi dati TiDB
connection = pymysql.connect(
    host="gateway01.eu-central-1.prod.aws.tidbcloud.com",  # il tuo host
    port=4000,
    user="2oqG2yhwBpPeH8k.root",       # il tuo user
    password="6r8aQms7qNBcZwYw",   # la tua password
    # DOPO (corretta per Codespace):
    ssl={"ssl_verify_cert": True},
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()

# Crea il database
cursor.execute("CREATE DATABASE IF NOT EXISTS prenotazionivoli")
cursor.execute("USE prenotazionivoli")

# ── TABELLE ──────────────────────────────────────────────

cursor.execute("""
CREATE TABLE IF NOT EXISTS COMPAGNIE_AEREE (
    id_compagnia INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    paese VARCHAR(100),
    codice_iata VARCHAR(10),
    sito_web VARCHAR(100)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS AEROPORTI (
    id_aeroporto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    citta VARCHAR(100),
    nazione VARCHAR(100),
    codice_iata VARCHAR(10),
    codice_icao VARCHAR(10)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS AEREI (
    id_aereo INT AUTO_INCREMENT PRIMARY KEY,
    modello VARCHAR(100),
    costruttore VARCHAR(100),
    capienza INT,
    anno_produzione INT,
    id_compagnia INT,
    FOREIGN KEY (id_compagnia) REFERENCES COMPAGNIE_AEREE(id_compagnia)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS UTENTI (
    id_utente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cognome VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    telefono VARCHAR(20),
    data_registrazione DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_nascita DATE
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS VOLI (
    id_volo INT AUTO_INCREMENT PRIMARY KEY,
    numero_volo VARCHAR(20),
    data_partenza DATETIME,
    data_arrivo DATETIME,
    prezzo_base DECIMAL(10,2),
    stato VARCHAR(20),
    id_aereo INT,
    aeroporto_partenza INT,
    aeroporto_arrivo INT,
    FOREIGN KEY (id_aereo) REFERENCES AEREI(id_aereo),
    FOREIGN KEY (aeroporto_partenza) REFERENCES AEROPORTI(id_aeroporto),
    FOREIGN KEY (aeroporto_arrivo) REFERENCES AEROPORTI(id_aeroporto)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS POSTI (
    id_posto INT AUTO_INCREMENT PRIMARY KEY,
    numero_posto VARCHAR(5),
    fila INT,
    lato CHAR(1),
    classe VARCHAR(20),
    id_aereo INT,
    FOREIGN KEY (id_aereo) REFERENCES AEREI(id_aereo)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PRENOTAZIONI (
    id_prenotazione INT AUTO_INCREMENT PRIMARY KEY,
    data_prenotazione DATETIME DEFAULT CURRENT_TIMESTAMP,
    stato VARCHAR(20),
    totale DECIMAL(10,2),
    id_utente INT,
    id_volo INT,
    FOREIGN KEY (id_utente) REFERENCES UTENTI(id_utente),
    FOREIGN KEY (id_volo) REFERENCES VOLI(id_volo)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS BIGLIETTI (
    id_biglietto INT AUTO_INCREMENT PRIMARY KEY,
    codice_biglietto VARCHAR(50),
    classe VARCHAR(20),
    prezzo DECIMAL(10,2),
    id_prenotazione INT,
    id_posto INT,
    FOREIGN KEY (id_prenotazione) REFERENCES PRENOTAZIONI(id_prenotazione),
    FOREIGN KEY (id_posto) REFERENCES POSTI(id_posto)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PAGAMENTI (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    metodo_pagamento VARCHAR(30),
    importo DECIMAL(10,2),
    valuta VARCHAR(10),
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    stato VARCHAR(20),
    id_prenotazione INT,
    FOREIGN KEY (id_prenotazione) REFERENCES PRENOTAZIONI(id_prenotazione)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS BAGAGLI (
    id_bagaglio INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(20),
    peso_kg DECIMAL(5,2),
    dimensioni VARCHAR(50),
    costo DECIMAL(10,2),
    id_biglietto INT,
    FOREIGN KEY (id_biglietto) REFERENCES BIGLIETTI(id_biglietto)
)""")

# ── DATI DI ESEMPIO ───────────────────────────────────────

cursor.execute("INSERT INTO COMPAGNIE_AEREE (nome, paese, codice_iata, sito_web) VALUES ('Ryanair','Irlanda','FR','www.ryanair.com')")
cursor.execute("INSERT INTO COMPAGNIE_AEREE (nome, paese, codice_iata, sito_web) VALUES ('Alitalia','Italia','AZ','www.alitalia.com')")
cursor.execute("INSERT INTO COMPAGNIE_AEREE (nome, paese, codice_iata, sito_web) VALUES ('Lufthansa','Germania','LH','www.lufthansa.com')")

cursor.execute("INSERT INTO AEROPORTI (nome, citta, nazione, codice_iata, codice_icao) VALUES ('Malpensa','Milano','Italia','MXP','LIMC')")
cursor.execute("INSERT INTO AEROPORTI (nome, citta, nazione, codice_iata, codice_icao) VALUES ('Fiumicino','Roma','Italia','FCO','LIRF')")
cursor.execute("INSERT INTO AEROPORTI (nome, citta, nazione, codice_iata, codice_icao) VALUES ('Heathrow','Londra','UK','LHR','EGLL')")
cursor.execute("INSERT INTO AEROPORTI (nome, citta, nazione, codice_iata, codice_icao) VALUES ('Charles de Gaulle','Parigi','Francia','CDG','LFPG')")

cursor.execute("INSERT INTO AEREI (modello, costruttore, capienza, anno_produzione, id_compagnia) VALUES ('Boeing 737','Boeing',189,2018,1)")
cursor.execute("INSERT INTO AEREI (modello, costruttore, capienza, anno_produzione, id_compagnia) VALUES ('Airbus A320','Airbus',180,2019,2)")
cursor.execute("INSERT INTO AEREI (modello, costruttore, capienza, anno_produzione, id_compagnia) VALUES ('Airbus A380','Airbus',555,2020,3)")

cursor.execute("INSERT INTO UTENTI (nome, cognome, email, password_hash, telefono, data_nascita) VALUES ('Mario','Rossi','mario@email.com','hash123','+39123456','1990-05-15')")
cursor.execute("INSERT INTO UTENTI (nome, cognome, email, password_hash, telefono, data_nascita) VALUES ('Giulia','Bianchi','giulia@email.com','hash456','+39654321','1995-08-22')")

cursor.execute("INSERT INTO VOLI (numero_volo, data_partenza, data_arrivo, prezzo_base, stato, id_aereo, aeroporto_partenza, aeroporto_arrivo) VALUES ('FR1234','2025-07-01 08:00:00','2025-07-01 10:30:00',89.99,'attivo',1,1,3)")
cursor.execute("INSERT INTO VOLI (numero_volo, data_partenza, data_arrivo, prezzo_base, stato, id_aereo, aeroporto_partenza, aeroporto_arrivo) VALUES ('AZ5678','2025-07-02 14:00:00','2025-07-02 15:30:00',59.99,'attivo',2,2,1)")
cursor.execute("INSERT INTO VOLI (numero_volo, data_partenza, data_arrivo, prezzo_base, stato, id_aereo, aeroporto_partenza, aeroporto_arrivo) VALUES ('LH9999','2025-07-05 06:00:00','2025-07-05 08:00:00',129.99,'attivo',3,1,4)")
cursor.execute("INSERT INTO VOLI (numero_volo, data_partenza, data_arrivo, prezzo_base, stato, id_aereo, aeroporto_partenza, aeroporto_arrivo) VALUES ('FR4321','2025-07-10 16:00:00','2025-07-10 18:00:00',75.00,'attivo',1,3,1)")

cursor.execute("INSERT INTO POSTI (numero_posto, fila, lato, classe, id_aereo) VALUES ('1A',1,'A','business',1)")
cursor.execute("INSERT INTO POSTI (numero_posto, fila, lato, classe, id_aereo) VALUES ('10B',10,'B','economy',1)")
cursor.execute("INSERT INTO POSTI (numero_posto, fila, lato, classe, id_aereo) VALUES ('5C',5,'C','economy',2)")

cursor.execute("INSERT INTO PRENOTAZIONI (stato, totale, id_utente, id_volo) VALUES ('confermata',89.99,1,1)")
cursor.execute("INSERT INTO PRENOTAZIONI (stato, totale, id_utente, id_volo) VALUES ('confermata',59.99,2,2)")

cursor.execute("INSERT INTO BIGLIETTI (codice_biglietto, classe, prezzo, id_prenotazione, id_posto) VALUES ('BIG-001','economy',89.99,1,2)")
cursor.execute("INSERT INTO BIGLIETTI (codice_biglietto, classe, prezzo, id_prenotazione, id_posto) VALUES ('BIG-002','economy',59.99,2,3)")

cursor.execute("INSERT INTO PAGAMENTI (metodo_pagamento, importo, valuta, stato, id_prenotazione) VALUES ('carta_credito',89.99,'EUR','completato',1)")
cursor.execute("INSERT INTO PAGAMENTI (metodo_pagamento, importo, valuta, stato, id_prenotazione) VALUES ('paypal',59.99,'EUR','completato',2)")

cursor.execute("INSERT INTO BAGAGLI (tipo, peso_kg, dimensioni, costo, id_biglietto) VALUES ('cabina',7.00,'55x35x20',0.00,1)")
cursor.execute("INSERT INTO BAGAGLI (tipo, peso_kg, dimensioni, costo, id_biglietto) VALUES ('stiva',23.00,'70x50x30',25.00,2)")

connection.commit()
print("✅ Database creato e popolato con successo!")
cursor.close()
connection.close()