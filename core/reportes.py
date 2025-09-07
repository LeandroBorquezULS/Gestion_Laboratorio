# core/reportes.py
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from core.reservas_bd import cupos_disponibles

def generar_reporte_reservas_pdf(fecha: str, ruta="reporte_reservas.pdf"):
    """
    Genera un PDF con el estado de los bloques en una fecha.
    """
    cupos = cupos_disponibles(fecha)

    # Definir documento
    ruta_absoluta = os.path.abspath(ruta)
    doc = SimpleDocTemplate(ruta_absoluta, pagesize=letter)

    elementos = []

    # Estilos
    estilos = getSampleStyleSheet()
    titulo = Paragraph(f"Reporte de reservas - {fecha}", estilos["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    # Encabezados de tabla
    data = [["Fecha", "Bloque", "Estado", "Clase", "Encargado"]]

    # Filas con la info de la BD
    for c in cupos:
        data.append([
            fecha,
            c["bloque"],
            c["estado"],
            c.get("clase", ""),
            c.get("encargado", "")
        ])

    # Crear tabla
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

    # Construir PDF
    doc.build(elementos)
    return ruta_absoluta
