# models/reservas.py
import datetime
from core import reservas_bd

class Laboratorio:
    def __init__(self, id_lab, nombre_lab):
        self.id_lab = id_lab
        self.nombre_lab = nombre_lab

    def esta_disponible(self, fecha, bloque_id):
        reservas = reservas_bd.cupos_disponibles(fecha)
        for r in reservas:
            if r["id"] == bloque_id and r["estado"] == "ocupado":
                return False
        return True

    def agregar_reserva(self, fecha, bloque_id, asignatura, encargado):
        if not self.esta_disponible(fecha, bloque_id):
            raise Exception("El laboratorio ya está reservado en ese bloque")
        return reservas_bd.crear_reserva(fecha, bloque_id, asignatura, encargado)

    def obtener_reservas_activas_por_fecha(self, fecha):
        return reservas_bd.cupos_disponibles(fecha)

    def __str__(self):
        return f"{self.nombre_lab}"


class Reserva:
    def __init__(self, id_reserva, asignatura, fecha_reserva, hora_inicio, hora_fin, estado="Pendiente", lab_id=None):
        self.id_reserva = id_reserva
        self.asignatura = asignatura
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
        self.lab_id = lab_id

    def cancelar(self):
        self.estado = "Cancelada"
        return reservas_bd.eliminar_reserva(self.id_reserva, self.fecha_reserva)
