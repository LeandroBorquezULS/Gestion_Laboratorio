#clases
class Laboratorio:
    def __init__(self, id_lab, nombre_lab, capacidad):
        self.id_lab = id_lab
        self.nombre_lab = nombre_lab
        self.capacidad = capacidad



class Reserva:
    def __init__(self, id_reserva, curso, fecha_reserva, hora_inicio, hora_fin, estado="Pendiente"):
        self.id_reserva = id_reserva
        self.curso = curso
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado 



class Encargado:
    def __init__(self, id_encargado, nombre, usuario, contrasena):
        self.id_encargado = id_encargado
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena


class Reporte:
    def __init__(self, id_reporte, reservas_canceladas, fecha_reporte, cantidad_reservas, lab_mas_usados):
        self.id_reporte = id_reporte
        self.reservas_canceladas = reservas_canceladas
        self.fecha_reporte = fecha_reporte
        self.cantidad_reservas = cantidad_reservas
        self.lab_mas_usados = lab_mas_usados 
