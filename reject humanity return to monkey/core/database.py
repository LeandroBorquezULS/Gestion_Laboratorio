# core/database.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "reservas.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def inicializar_bd():
    with get_connection() as conn:
        cursor = conn.cursor()

        # crear tabla de usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('admin', 'docente'))
        )
        """)

        # Crear tabla de bloques
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bloques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL
        )
        """)

        # Crear tabla de reservas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            bloque_id INTEGER NOT NULL,
            clase TEXT NOT NULL,
            encargado TEXT,
            FOREIGN KEY(bloque_id) REFERENCES bloques(id),
            UNIQUE(fecha, bloque_id)
        )
        """)

        # Insertar bloques fijos si no existen
        bloques = [
            ("08:00", "09:30"),
            ("09:45", "11:15"),
            ("11:30", "13:00"),
            ("14:30", "16:00"),
            ("16:15", "17:45"),
            ("18:00", "19:30")
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO bloques (id, hora_inicio, hora_fin)
            VALUES (?, ?, ?)
        """, [(i + 1, b[0], b[1]) for i, b in enumerate(bloques)])
        conn.commit()
