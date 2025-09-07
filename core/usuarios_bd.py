# core/usuarios_bd.py
from core.database import get_connection

def registrar_usuario(nombre: str, usuario: str, contrasena: str, rol: str = "docente"):
    query = """
    INSERT INTO usuarios (nombre, usuario, contrasena, rol)
    VALUES (?, ?, ?, ?)
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre, usuario, contrasena, rol))
            conn.commit()
        return True
    except Exception as e:
        print("Error registrando usuario:", e)
        return False


def autenticar_usuario(usuario: str, contrasena: str):
    query = """
    SELECT id, nombre, rol FROM usuarios
    WHERE usuario = ? AND contrasena = ?
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (usuario, contrasena))
        return cursor.fetchone()  # devuelve (id, nombre, rol) o None


def ver_usuarios_registrados():
    """
    Devuelve una lista de diccionarios con todos los usuarios registrados
    """
    query = "SELECT id, nombre, usuario, rol FROM usuarios ORDER BY nombre"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        usuarios = cursor.fetchall()
    return [{"id": u[0], "nombre": u[1], "usuario": u[2], "rol": u[3]} for u in usuarios]


def quitar_usuario(usuario_id: int):
    """
    Elimina un usuario por su ID. Devuelve True si tuvo éxito, False si hubo error.
    """
    query = "DELETE FROM usuarios WHERE id = ?"
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (usuario_id,))
            conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar usuario:", e)
        return False
