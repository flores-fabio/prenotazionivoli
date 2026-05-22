# RELAZIONE TECNICA — Sistema Prenotazione Voli

## Architettura

Il progetto è un'applicazione fullstack a 3 livelli:
- **Frontend**: Angular 21 (porta 4200)
- **Backend**: Flask/Python (porta 5000)
- **Database**: TiDB Cloud (MySQL-compatible)

Il flusso dati è: UI Angular → HTTP Request → Flask API → Query SQL → TiDB → JSON Response → Angular

## Schema ER

Il database è composto da 10 entità:
COMPAGNIE_AEREE, AEREI, AEROPORTI, VOLI, UTENTI, PRENOTAZIONI, BIGLIETTI, POSTI, PAGAMENTI, BAGAGLI

## Documentazione API

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| /api/compagnie | GET | Lista tutte le compagnie aeree |
| /api/compagnie/:id | GET | Dettaglio singola compagnia |
| /api/voli | GET | Lista voli (con filtri partenza/arrivo/data/compagnia) |
| /api/voli/:id | GET | Dettaglio singolo volo con JOIN |
| /api/prenotazioni | GET | Lista prenotazioni con dati utente e volo |
| /api/prenotazioni | POST | Crea nuova prenotazione |
| /api/utenti | GET | Lista utenti |

## Navigazione a 3 Livelli

1. **Livello 1**: Lista compagnie aeree
2. **Livello 2**: Lista voli filtrati per compagnia (con breadcrumb)
3. **Livello 3**: Dettaglio volo con tutti i dati

## Funzionalità Implementate

- Navigazione a 3 livelli con breadcrumb
- Ricerca voli per città partenza, arrivo e data
- Inserimento nuova prenotazione tramite form
- Gestione errori HTTP (404, 400, 500)
- URL backend centralizzato in un unico punto (api.service.ts)

## Tecnologie Utilizzate

- **Frontend**: Angular 21, TypeScript, HTML/CSS
- **Backend**: Python 3, Flask, flask-cors, PyMySQL
- **Database**: TiDB Cloud (compatibile MySQL)
- **Ambiente**: GitHub Codespaces
