import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Ouvre une connexion vers PostgreSQL via le réseau Docker"""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def init_db():
    """Crée les tables si elles n'existent pas encore"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cameras (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            rtsp_url_enc TEXT NOT NULL,
            status VARCHAR(10) DEFAULT 'online',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            camera_id INTEGER REFERENCES cameras(id),
            message TEXT NOT NULL,
            email_sent BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Base de données initialisée avec succès")

def get_all_cameras():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, status, created_at FROM cameras ORDER BY id")
    cameras = cur.fetchall()
    cur.close()
    conn.close()
    return cameras

def add_camera(nom, rtsp_url_enc):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cameras (nom, rtsp_url_enc) VALUES (%s, %s) RETURNING id",
        (nom, rtsp_url_enc)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def update_camera_status(camera_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cameras SET status = %s WHERE id = %s",
        (status, camera_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_camera_rtsp(camera_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT rtsp_url_enc FROM cameras WHERE id = %s", (camera_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def add_alert(camera_id, message, email_sent=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alerts (camera_id, message, email_sent) VALUES (%s, %s, %s)",
        (camera_id, message, email_sent)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_all_alerts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, c.nom, a.message, a.email_sent, a.created_at
        FROM alerts a
        JOIN cameras c ON a.camera_id = c.id
        ORDER BY a.created_at DESC
    """)
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return alerts