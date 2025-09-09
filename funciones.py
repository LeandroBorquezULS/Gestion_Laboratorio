import datetime
from utils.reserva import Reserva
from utils.reporte import Reporte
from data import (
    encargados,
    laboratorios,
    bloques_horarios,
    bloques_texto,
    reserva_id_counter
)

# -----------------------------
# Funciones auxiliares
# -----------------------------

def login():
    """Inicia sesión de un encargado del laboratorio."""
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    for enc in encargados:
        if enc.verificar_login(usuario, contrasena):
            print("Acceso concedido")
            return enc
    print("Usuario o contraseña incorrectos")
    return None


def obtener_fecha(mensaje):
    """Obtiene una fecha desde la entrada del usuario."""
    fecha_input = input(mensaje)
    if fecha_input == "":
        return datetime.date.today().strftime("%Y-%m-%d")
    return fecha_input


def mostrar_horarios_lab(lab, fecha):
    """Muestra la disponibilidad de un laboratorio para cada bloque horario."""
    print(f"\nDisponibilidad - {lab.nombre_lab} - {fecha}")
    print("=" * 50)
    for i, (hora_inicio, hora_fin) in enumerate(bloques_horarios):
        disponible = lab.esta_disponible(fecha, hora_inicio, hora_fin)
        estado = "Disponible" if disponible else "Ocupado"
        print(f"{i+1}. {bloques_texto[i]} - {estado}")
    print()


def mostrar_reservas_ocupadas(lab, fecha):
    """Lista las reservas activas de un laboratorio para una fecha específica."""
    print(f"\nReservas activas - {lab.nombre_lab} - {fecha}")
    print("=" * 50)
    reservas_activas = lab.obtener_reservas_activas_por_fecha(fecha)
    if not reservas_activas:
        print("No hay reservas activas")
        return []

    reservas_por_bloque = []
    for i, _ in enumerate(bloques_horarios):
        reservas_bloque = lab.obtener_reservas_por_fecha_y_bloque(fecha, i, bloques_horarios)
        for reserva in reservas_bloque:
            reservas_por_bloque.append((i, reserva))

    if not reservas_por_bloque:
        print("No hay reservas ocupadas en bloques horarios")
        return []

    for j, (bloque_idx, reserva) in enumerate(reservas_por_bloque, 1):
        print(f"{j}. Bloque {bloque_idx+1} ({bloques_texto[bloque_idx]}) - "
              f"{reserva.asignatura} - ID: {reserva.id_reserva}")

    return reservas_por_bloque


def crear_reserva(lab, fecha, bloque_idx):
    """Crea una nueva reserva para un laboratorio."""
    global reserva_id_counter
    asignatura = input("Nombre de la asignatura: ")
    hora_inicio, hora_fin = bloques_horarios[bloque_idx]
    reserva = Reserva(reserva_id_counter, asignatura, fecha, hora_inicio, hora_fin, lab_id=lab.id_lab)
    try:
        lab.agregar_reserva(reserva)
        print("Reserva creada correctamente")
        print(f"ID de reserva: {reserva_id_counter}")
        # Actualiza el contador en memoria
        from data import reserva_id_counter as counter_ref
        counter_ref += 1
        globals()['reserva_id_counter'] = counter_ref
    except Exception as e:
        print(f"Error: {e}")


def cancelar_reserva():
    """Cancela una reserva seleccionada por el usuario."""
    print("\nCancelar reserva")
    print("=" * 20)
    fecha = obtener_fecha("Fecha de la reserva (YYYY-MM-DD) [Enter para hoy]: ")

    print("\nLaboratorios:")
    for i, lab in enumerate(laboratorios):
        print(f"{i+1}. {lab.nombre_lab}")

    try:
        lab_idx = int(input("Seleccione laboratorio (número): ")) - 1
        if lab_idx < 0 or lab_idx >= len(laboratorios):
            print("Laboratorio inválido")
            return
    except ValueError:
        print("Entrada inválida")
        return

    lab_seleccionado = laboratorios[lab_idx]
    reservas_ocupadas = mostrar_reservas_ocupadas(lab_seleccionado, fecha)
    if not reservas_ocupadas:
        return

    try:
        opcion = int(input("Seleccione la reserva a cancelar (número): ")) - 1
        if opcion < 0 or opcion >= len(reservas_ocupadas):
            print("Opción inválida")
            return
    except ValueError:
        print("Entrada inválida")
        return

    _, reserva = reservas_ocupadas[opcion]
    confirmacion = input("¿Está seguro de cancelar esta reserva? (s/n): ").lower()
    if confirmacion == 's':
        reserva.estado = "Cancelada"
        print("Reserva cancelada")
    else:
        print("Operación cancelada")


def generar_reporte_mensual():
    """Genera un reporte mensual de las reservas de todos los laboratorios."""
    print("\nGenerar reporte mensual")
    print("=" * 30)
    try:
        anio = int(input("Año (YYYY): "))
        mes = int(input("Mes (1-12): "))
        if not 1 <= mes <= 12:
            print("Mes inválido")
            return
        reporte = Reporte(mes, anio, laboratorios)
        print("\n" + reporte.generar_resumen_mensual())
    except ValueError:
        print("Entrada inválida")
