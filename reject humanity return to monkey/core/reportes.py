# core/reportes.py
import os
import calendar
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from core.reservas_bd import cupos_disponibles

def generar_reporte_reservas_pdf(fecha: str, ruta_base="report"):
    """
    Genera un PDF mensual.
    - Una página por día.
    - Formato horizontal (landscape) para aprovechar el espacio.
    - Si el archivo ya existe, agrega numeración incremental.
    """
    # Convertir fecha seleccionada a datetime
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")

    # Primer y último día del mes
    primer_dia = fecha_dt.replace(day=1)
    ultimo_dia = fecha_dt.replace(day=calendar.monthrange(fecha_dt.year, fecha_dt.month)[1])

    # Crear carpeta si no existe
    if not os.path.exists(ruta_base):
        os.makedirs(ruta_base)

    # Nombre base del archivo
    base_nombre = f"reporte_{primer_dia.strftime('%Y-%m-%d')}_{ultimo_dia.strftime('%Y-%m-%d')}"
    ruta_pdf = os.path.join(ruta_base, f"{base_nombre}.pdf")

    # Si ya existe, agregar numeración incremental
    contador = 1
    while os.path.exists(ruta_pdf):
        ruta_pdf = os.path.join(ruta_base, f"{base_nombre}_{contador}.pdf")
        contador += 1

    # Documento en formato horizontal
    ruta_absoluta = os.path.abspath(ruta_pdf)
    doc = SimpleDocTemplate(ruta_absoluta, pagesize=landscape(letter))
    elementos = []

    # Estilos de texto
    estilos = getSampleStyleSheet()

    # Recorrer todos los días del mes
    fecha_iter = primer_dia
    while fecha_iter <= ultimo_dia:
        fecha_str = fecha_iter.strftime("%Y-%m-%d")

        # Título de la página/día
        titulo = Paragraph(f"Reporte de reservas - {fecha_iter.strftime('%d/%m/%Y')}", estilos["Title"])
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))

        # Encabezados de la tabla
        data = [["Bloque", "Estado", "Clase", "Encargado"]]

        # Obtener cupos disponibles del día
        cupos = cupos_disponibles(fecha_str)
        for c in cupos:
            data.append([
                c["bloque"],
                c["estado"],
                c.get("clase", ""),
                c.get("encargado", "")
            ])

        # Si no hay datos para el día, mostrar mensaje
        if len(data) == 1:
            data.append(["-", "Sin reservas", "-", "-"])

        # Crear tabla para el día
        tabla = Table(data, repeatRows=1)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabla)

        # Salto de página excepto para el último día
        if fecha_iter < ultimo_dia:
            elementos.append(PageBreak())

        fecha_iter += timedelta(days=1)

    # Construir el PDF
    doc.build(elementos)
    return ruta_absoluta
