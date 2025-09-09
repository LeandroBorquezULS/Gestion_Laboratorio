from data import laboratorios, bloques_texto
from funciones import (
    login,
    obtener_fecha,
    mostrar_horarios_lab,
    crear_reserva,
    generar_reporte_mensual,
    cancelar_reserva
)

def menu():
    
    #Muestra el menú principal del sistema de reservas de laboratorios.

    print("==== Sistema de Reservas ====")

    # Se fuerza al usuario a iniciar sesión antes de usar el sistema
    enc = None
    while not enc:
        enc = login()


    while True:
        print("\nOpciones:")
        print("1. Crear reserva")
        print("2. Generar reporte mensual")
        print("3. Cancelar reserva")
        print("4. Salir")
        opcion = input("Elija opción: ")

        if opcion == "1":
            # Crear una nueva reserva
            fecha = obtener_fecha("Fecha de reserva (YYYY-MM-DD) [Enter para hoy]: ")

            # Mostrar laboratorios
            print("\nLaboratorios disponibles:")
            for i, lab in enumerate(laboratorios):
                print(f"{i+1}. {lab.nombre_lab}")

            # Seleccionar laboratorio
            try:
                lab_idx = int(input("Elija laboratorio (número): ")) - 1
                if lab_idx < 0 or lab_idx >= len(laboratorios):
                    print("Laboratorio inválido")
                    continue
            except ValueError:
                print("Entrada inválida")
                continue

            lab_seleccionado = laboratorios[lab_idx]

            # Mostrar horarios disponibles
            mostrar_horarios_lab(lab_seleccionado, fecha)
            try:
                bloque_idx = int(input("Elija bloque horario: ")) - 1
                if bloque_idx < 0 or bloque_idx >= len(bloques_texto):
                    print("Bloque inválido")
                    continue
            except ValueError:
                print("Entrada inválida")
                continue

            # Crear la reserva en el bloque seleccionado
            crear_reserva(lab_seleccionado, fecha, bloque_idx)

        elif opcion == "2":
            generar_reporte_mensual()

        elif opcion == "3":
            cancelar_reserva()

        elif opcion == "4":

            print("Saliendo...")
            break

        else:
            print("Opción inválida")
