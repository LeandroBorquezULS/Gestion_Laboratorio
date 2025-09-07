# reservas.py
from core.database import get_connection

def cupos_disponibles(fecha: str):
    """
    Devuelve una lista con el estado de cada bloque para la fecha indicada.
    """
    query = """
    SELECT b.id, b.hora_inicio, b.hora_fin,
           r.clase, r.encargado
    FROM bloques b
    LEFT JOIN reservas r
    ON b.id = r.bloque_id AND r.fecha = ?
    ORDER BY b.id
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (fecha,))
        datos = cursor.fetchall()

    resultados = []
    for bloque_id, inicio, fin, clase, encargado in datos:
        resultados.append({
            "id": bloque_id,
            "bloque": f"{inicio} - {fin}",
            "estado": "ocupado" if clase else "disponible",
            "clase": clase,
            "encargado": encargado
        })
    return resultados


def crear_reserva(fecha: str, bloque_id: int, clase: str, encargado: str = None):
    """
    Intenta crear una reserva. Devuelve True si tuvo éxito, False si ya está ocupada.
    """
    query = """
    INSERT INTO reservas (fecha, bloque_id, clase, encargado)
    VALUES (?, ?, ?, ?)
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (fecha, bloque_id, clase, encargado))
            conn.commit()
        return True
    except:
        return False


def crear_informe(fecha_inicio: str, fecha_fin: str):
    """
    Devuelve una lista de todas las reservas en el rango dado.
    """
    query = """
    SELECT r.fecha, b.hora_inicio, b.hora_fin, r.clase, r.encargado
    FROM reservas r
    JOIN bloques b ON r.bloque_id = b.id
    WHERE r.fecha BETWEEN ? AND ?
    ORDER BY r.fecha, b.hora_inicio
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (fecha_inicio, fecha_fin))
        return cursor.fetchall()
