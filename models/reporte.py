# models/reportes.py
import datetime
from core.reportes_bd import generar_reporte_reservas_pdf

class Reporte:
    def __init__(self, mes, anio):
        self.mes = mes
        self.anio = anio

    def generar_resumen_pdf(self):
        fecha_inicio = datetime.date(self.anio, self.mes, 1).strftime("%Y-%m-%d")
        return generar_reporte_reservas_pdf(fecha_inicio)
