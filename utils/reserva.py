   def __init__(self, id_reserva, asignatura, fecha_reserva, hora_inicio, hora_fin, estado="Pendiente", lab_id=None):
        """
        Constructor (__init__):
        - Inicializa los atributos principales de la reserva.
        - Algunos parámetros tienen valores por defecto, por ejemplo:
          estado = "Pendiente", lo cual facilita la creación de reservas nuevas.
        - lab_id puede ser None si aún no se asigna un laboratorio.
        
        Principio aplicado: **encapsulación**.
        Cada reserva mantiene sus propios datos internos como atributos.
        """
        self.id_reserva = id_reserva
        self.asignatura = asignatura
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
        self.lab_id = lab_id

    def __str__(self):
        """
        Método especial __str__:
        - Define cómo se muestra el objeto cuando se usa print() o str(objeto).
        - En lugar de mostrar la dirección de memoria, devuelve una descripción legible.
        
        Principio aplicado: **abstracción**.
        El usuario ve un resumen amigable, sin necesidad de explorar todos los atributos manualmente.
        """
        return f"ID: {self.id_reserva} [{self.estado}] {self.asignatura} ({self.fecha_reserva} {self.hora_inicio}-{self.hora_fin})"

    def cancelar(self):
        """
        Método cancelar:
        - Cambia el estado de la reserva a 'Cancelada'.
        - Retorna un mensaje confirmando la acción.
        
        Aquí se aplica el principio de **responsabilidad** en POO:
        la propia reserva sabe cómo modificar su estado.
        
        Ejemplo:
        reserva.cancelar()
        → "Reserva 12 cancelada"
        """
        self.estado = "Cancelada"
        return f"Reserva {self.id_reserva} cancelada"