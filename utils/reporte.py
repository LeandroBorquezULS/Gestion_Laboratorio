import datetime

class Reporte:
    def __init__(self, mes, anio, laboratorios):
        self.mes = mes
        self.anio = anio
        self.laboratorios = laboratorios
        self.reservas = self._obtener_reservas_mes()

    def _obtener_reservas_mes(self):
        reservas_mes = []
        for lab in self.laboratorios:
            for reserva in lab.reservas:
                try:
                    fecha_reserva = datetime.datetime.strptime(reserva.fecha_reserva, "%Y-%m-%d")
                    if (fecha_reserva.month == self.mes and fecha_reserva.year == self.anio
                        and reserva.estado != "Cancelada"):
                        reservas_mes.append(reserva)
                except (ValueError, TypeError):
                    continue
        return reservas_mes

    def generar_resumen_mensual(self):
        if not self.reservas:
            return f"Reporte {self.mes}/{self.anio}: No hay reservas activas"

        self.reservas.sort(key=lambda x: x.fecha_reserva)
        resumen = f"REPORTE MENSUAL - {self.mes}/{self.anio}\n"
        resumen += "=" * 50 + "\n"
        resumen += f"Total de reservas: {len(self.reservas)}\n"
        resumen += "=" * 50 + "\n\n"

        reservas_por_fecha = {}
        for reserva in self.reservas:
            reservas_por_fecha.setdefault(reserva.fecha_reserva, []).append(reserva)

        for fecha, reservas in sorted(reservas_por_fecha.items()):
            resumen += f"{fecha}:\n"
            for reserva in reservas:
                resumen += f"   {reserva.hora_inicio:.2f}-{reserva.hora_fin:.2f} - {reserva.asignatura} (Lab {reserva.lab_id})\n"
            resumen += "\n"
        return resumen
