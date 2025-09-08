class Reserva:
    def __init__(self, id_reserva, asignatura, fecha_reserva, hora_inicio, hora_fin, estado="Pendiente", lab_id=None):
        self.id_reserva = id_reserva
        self.asignatura = asignatura
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
        self.lab_id = lab_id

    def __str__(self):
        return f"ID: {self.id_reserva} [{self.estado}] {self.asignatura} ({self.fecha_reserva} {self.hora_inicio}-{self.hora_fin})"

    def cancelar(self):
        self.estado = "Cancelada"
        return f"Reserva {self.id_reserva} cancelada"
