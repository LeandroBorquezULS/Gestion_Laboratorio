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
    
####################################################################

def reset_bd():
    conn = sqlite3.connect("laboratorio.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Reservas")
    cursor.execute("DROP TABLE IF EXISTS Laboratorios")
    cursor.execute("DROP TABLE IF EXISTS encargados")
    conn.commit()

def agregar_reserva(curso, fecha_reserva, hora_inicio, hora_fin, id_lab, estado):
    conn = sqlite3.connect("laboratorio.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("INSERT INTO Reservas (curso, fecha_reserva, hora_inicio, hora_fin, id_lab, estado) VALUES (?, ?, ?, ?, ?, ?)",
                   (curso, fecha_reserva, hora_inicio, hora_fin, id_lab, estado))
    conn.commit()
    conn.close()

def mostrar_reservas():
    conn = sqlite3.connect("laboratorio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reservas")
    return cursor.fetchall()

def agregar_encargados(id_encargado, nombre, usuario, contrasena):
    conn = sqlite3.connect("laboratorio.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Encargados (id_encargado, nombre, usuario, contrasena) VALUES (?, ?, ?, ?)", 
                   (id_encargado, nombre, usuario, contrasena))
    conn.commit()
    conn.close()

def mostrar_encargados():
    conn = sqlite3.connect("laboratorio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM encargados")
    return cursor.fetchall()

if __name__ == '__main__':
    reset_bd()
    crear_bd()
    agregar_reserva("clase de computacion", "31-08-2025", "09:00", "11:00", 1, "pendiente")
    print("Reservas:\n", mostrar_reservas())
    print("encargados \n", mostrar_encargados())