class Laboratorio:
    def __init__(self, id_lab, nombre_lab):
        self.id_lab = id_lab
        self.nombre_lab = nombre_lab
        self.reservas = []

    def esta_disponible(self, fecha, hora_inicio, hora_fin):
        for r in self.reservas:
            if (r.fecha_reserva == fecha and r.estado != "Cancelada"
                and not (hora_fin <= r.hora_inicio or hora_inicio >= r.hora_fin)):
                return False
        return True

    def agregar_reserva(self, reserva):
        if not self.esta_disponible(reserva.fecha_reserva, reserva.hora_inicio, reserva.hora_fin):
            raise Exception("El laboratorio ya está reservado en ese bloque")
        self.reservas.append(reserva)

    def obtener_reservas_activas_por_fecha(self, fecha):
        return [r for r in self.reservas if r.fecha_reserva == fecha and r.estado != "Cancelada"]

    def obtener_reservas_por_fecha_y_bloque(self, fecha, bloque_idx, bloques_horarios):
        hora_inicio, hora_fin = bloques_horarios[bloque_idx]
        return [
            reserva for reserva in self.reservas
            if (reserva.fecha_reserva == fecha and reserva.estado != "Cancelada"
                and not (hora_fin <= reserva.hora_inicio or hora_inicio >= reserva.hora_fin))
        ]

    def __str__(self):
        return f"{self.nombre_lab}"
