from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, origins="*")

# ⚠️ Stesse credenziali del db_setup.py
DB_CONFIG = {
    "host": "gateway01.eu-central-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "2oqG2yhwBpPeH8k.root",
    "password": "6r8aQms7qNBcZwYw",
    "database": "prenotazionivoli",
    "ssl": {"ssl_verify_cert": True},
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

# ─────────────────────────────────────────
# COMPAGNIE AEREE (livello 1 navigazione)
# ─────────────────────────────────────────

@app.route("/api/compagnie", methods=["GET"])
def get_compagnie():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM COMPAGNIE_AEREE")
        result = cursor.fetchall()
        db.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/compagnie/<int:id>", methods=["GET"])
def get_compagnia(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM COMPAGNIE_AEREE WHERE id_compagnia = %s", (id,))
        result = cursor.fetchone()
        db.close()
        if not result:
            return jsonify({"error": "Compagnia non trovata"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# VOLI (livello 2 navigazione)
# ─────────────────────────────────────────

@app.route("/api/voli", methods=["GET"])
def get_voli():
    try:
        db = get_db()
        cursor = db.cursor()

        # Filtri di ricerca (query params)
        partenza = request.args.get("partenza")
        arrivo = request.args.get("arrivo")
        data = request.args.get("data")
        compagnia = request.args.get("compagnia")

        query = """
            SELECT v.*, 
                   a.modello AS aereo_modello,
                   c.nome AS compagnia_nome,
                   ap.citta AS citta_partenza,
                   aa.citta AS citta_arrivo
            FROM VOLI v
            JOIN AEREI a ON v.id_aereo = a.id_aereo
            JOIN COMPAGNIE_AEREE c ON a.id_compagnia = c.id_compagnia
            JOIN AEROPORTI ap ON v.aeroporto_partenza = ap.id_aeroporto
            JOIN AEROPORTI aa ON v.aeroporto_arrivo = aa.id_aeroporto
            WHERE 1=1
        """
        params = []

        if partenza:
            query += " AND ap.citta LIKE %s"
            params.append(f"%{partenza}%")
        if arrivo:
            query += " AND aa.citta LIKE %s"
            params.append(f"%{arrivo}%")
        if data:
            query += " AND DATE(v.data_partenza) = %s"
            params.append(data)
        if compagnia:
            query += " AND c.id_compagnia = %s"
            params.append(compagnia)

        cursor.execute(query, params)
        result = cursor.fetchall()
        db.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/voli/<int:id>", methods=["GET"])
def get_volo(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT v.*,
                   a.modello AS aereo_modello, a.capienza,
                   c.nome AS compagnia_nome, c.codice_iata AS compagnia_iata,
                   ap.nome AS nome_aeroporto_partenza, ap.citta AS citta_partenza,
                   aa.nome AS nome_aeroporto_arrivo, aa.citta AS citta_arrivo
            FROM VOLI v
            JOIN AEREI a ON v.id_aereo = a.id_aereo
            JOIN COMPAGNIE_AEREE c ON a.id_compagnia = c.id_compagnia
            JOIN AEROPORTI ap ON v.aeroporto_partenza = ap.id_aeroporto
            JOIN AEROPORTI aa ON v.aeroporto_arrivo = aa.id_aeroporto
            WHERE v.id_volo = %s
        """, (id,))
        result = cursor.fetchone()
        db.close()
        if not result:
            return jsonify({"error": "Volo non trovato"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# PRENOTAZIONI (POST — inserimento)
# ─────────────────────────────────────────

@app.route("/api/prenotazioni", methods=["GET"])
def get_prenotazioni():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.*,
                   u.nome AS utente_nome, u.cognome AS utente_cognome,
                   v.numero_volo,
                   ap.citta AS citta_partenza,
                   aa.citta AS citta_arrivo
            FROM PRENOTAZIONI p
            JOIN UTENTI u ON p.id_utente = u.id_utente
            JOIN VOLI v ON p.id_volo = v.id_volo
            JOIN AEROPORTI ap ON v.aeroporto_partenza = ap.id_aeroporto
            JOIN AEROPORTI aa ON v.aeroporto_arrivo = aa.id_aeroporto
        """)
        result = cursor.fetchall()
        db.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/prenotazioni", methods=["POST"])
def crea_prenotazione():
    try:
        data = request.get_json()

        # Validazione campi obbligatori
        if not data.get("id_utente") or not data.get("id_volo"):
            return jsonify({"error": "id_utente e id_volo sono obbligatori"}), 400

        db = get_db()
        cursor = db.cursor()

        # Prendi il prezzo base del volo
        cursor.execute("SELECT prezzo_base FROM VOLI WHERE id_volo = %s", (data["id_volo"],))
        volo = cursor.fetchone()
        if not volo:
            return jsonify({"error": "Volo non trovato"}), 404

        cursor.execute("""
            INSERT INTO PRENOTAZIONI (stato, totale, id_utente, id_volo)
            VALUES (%s, %s, %s, %s)
        """, ("confermata", volo["prezzo_base"], data["id_utente"], data["id_volo"]))

        db.commit()
        new_id = cursor.lastrowid
        db.close()
        return jsonify({"message": "Prenotazione creata", "id_prenotazione": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# UTENTI
# ─────────────────────────────────────────

@app.route("/api/utenti", methods=["GET"])
def get_utenti():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_utente, nome, cognome, email, telefono FROM UTENTI")
        result = cursor.fetchall()
        db.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)