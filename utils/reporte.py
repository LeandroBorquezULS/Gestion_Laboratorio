import datetime


#Se crea la clase reporte con sus respectivos atributos usando su respectivo constructor

class Reporte:
    def __init__(self, mes, anio, laboratorios):
        self.mes = mes
        self.anio = anio
        self.laboratorios = laboratorios
        self.reservas = self._obtener_reservas_mes()



    def _obtener_reservas_mes(self):
        """
        Método privado (_obtener_reservas_mes):
        Recorre todos los laboratorios y sus reservas, filtrando solo las que:
        - Pertenecen al mes y año solicitados.
        - No están canceladas.
        
        Este método demuestra **abstracción**: el usuario de la clase Reporte 
        no necesita preocuparse por cómo se filtran las reservas, 
        solo recibe el resultado listo.
        """
        reservas_mes = []
        for lab in self.laboratorios:
            for reserva in lab.reservas:
                try:
                    # Se intenta convertir la fecha en un objeto datetime para validar.
                    fecha_reserva = datetime.datetime.strptime(reserva.fecha_reserva, "%Y-%m-%d")
                    
                    # Lógica de filtrado: coincide mes/año y estado válido.
                    if (fecha_reserva.month == self.mes and fecha_reserva.year == self.anio
                        and reserva.estado != "Cancelada"):
                        reservas_mes.append(reserva)
                except (ValueError, TypeError):
                    # Manejo de errores: si la fecha está mal formateada o es inválida,
                    # simplemente se omite esa reserva en lugar de romper el programa.
                    continue
        return reservas_mes

    def generar_resumen_mensual(self):
        """
        Método público (generar_resumen_mensual):
        Construye un resumen en formato de texto de todas las reservas filtradas.
        
        Principios aplicados:
        - **Polimorfismo implícito**: aunque las reservas provienen de distintos laboratorios,
          todas pueden procesarse igual porque se asume que cumplen la misma interfaz
          (tienen fecha_reserva, hora_inicio, hora_fin, asignatura, lab_id, estado).
        - **Separación de responsabilidades**: este método solo arma el reporte,
          no filtra ni procesa datos (eso ya lo hizo _obtener_reservas_mes).
        """
        if not self.reservas:
            # Caso base: no hay reservas válidas
            return f"Reporte {self.mes}/{self.anio}: No hay reservas activas"

        # Se ordenan las reservas cronológicamente.
        self.reservas.sort(key=lambda x: x.fecha_reserva)

        # Encabezado del reporte
        resumen = f"REPORTE MENSUAL - {self.mes}/{self.anio}\n"
        resumen += "=" * 50 + "\n"
        resumen += f"Total de reservas: {len(self.reservas)}\n"
        resumen += "=" * 50 + "\n\n"

        # Agrupamos reservas por fecha para mostrar de forma más clara
        reservas_por_fecha = {}
        for reserva in self.reservas:
            reservas_por_fecha.setdefault(reserva.fecha_reserva, []).append(reserva)

        # Se recorre cada día con sus reservas correspondientes
        for fecha, reservas in sorted(reservas_por_fecha.items()):
            resumen += f"{fecha}:\n"
            for reserva in reservas:
                resumen += f"   {reserva.hora_inicio:.2f}-{reserva.hora_fin:.2f} - {reserva.asignatura} (Lab {reserva.lab_id})\n"
            resumen += "\n"

        return resumen