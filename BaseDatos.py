import sqlite3

def crear_bd():
    conn = sqlite3.connect("laboratorio.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Laboratorios (
        id_lab INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_lab TEXT NOT NULL,
        capacidad INTEGER NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reservas (
        id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
        curso TEXT NOT NULL,
        fecha_reserva TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        estado TEXT DEFAULT 'Pendiente',
        id_lab INTEGER,
        FOREIGN KEY (id_lab) REFERENCES Laboratorios (id_lab)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Encargados (
        id_encargado INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL
    )""")

    conn.commit()
    conn.close()


def agregar_laboratorio(nombre, capacidad):
    conn = sqlite3.connect("laboratorio.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Laboratorios (nombre_lab, capacidad) VALUES (?, ?)", 
                   (nombre, capacidad))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    crear_bd()
    agregar_laboratorio("Laboratorio de Computación", 30)
    agregar_laboratorio("Laboratorio de Física", 25)
