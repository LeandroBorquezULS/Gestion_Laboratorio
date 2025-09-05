# -----------------------------
# Clases
# -----------------------------

class Persona:
    def __init__(self, nombre, usuario):
        self._nombre = nombre
        self._usuario = usuario

    def mostrar_info(self):
        return f"Persona: {self._nombre}, Usuario: {self._usuario}"

class Encargado(Persona):
    def __init__(self, nombre, usuario, id_encargado, contrasena):
        super().__init__(nombre, usuario)
        self.id_encargado = id_encargado
        self.__contrasena = contrasena

    def verificar_login(self, usuario, contrasena):
        return self._usuario == usuario and self.__contrasena == contrasena

    def mostrar_info(self):
        return f"Encargado: {self._nombre}, Usuario: {self._usuario}"

class Laboratorio:
    def __init__(self, id_lab, nombre_lab, capacidad):
        self.id_lab = id_lab
        self.nombre_lab = nombre_lab
        self.capacidad_total = capacidad
        self.reservas = []

    def cupos_disponibles(self, fecha, hora_inicio, hora_fin):
        # Cuenta los cupos que ya están reservados en el mismo bloque y fecha
        ocupados = sum(getattr(r, "cupos", 1) for r in self.reservas 
                       if r.fecha_reserva == fecha and not (hora_fin <= r.hora_inicio or hora_inicio >= r.hora_fin))
        return self.capacidad_total - ocupados

    def agregar_reserva(self, reserva, cupos_solicitados=1):
        disponibles = self.cupos_disponibles(reserva.fecha_reserva, reserva.hora_inicio, reserva.hora_fin)
        if cupos_solicitados > disponibles:
            raise Exception(f"No hay cupos suficientes en el laboratorio (Disponibles: {disponibles})")
        
        reserva.cupos = cupos_solicitados
        self.reservas.append(reserva)

    def __str__(self):
        return f"{self.nombre_lab} (Capacidad: {self.capacidad_total})"

class Reserva:
    def __init__(self, id_reserva, curso, fecha_reserva, hora_inicio, hora_fin, estado="Pendiente", lab_id=None):
        self.id_reserva = id_reserva
        self.curso = curso
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
        self.lab_id = lab_id
        self.cupos = 1

    def __str__(self):
        return f"[{self.estado}] {self.curso} ({self.fecha_reserva} {self.hora_inicio}-{self.hora_fin}) - Cupos: {self.cupos}"

class Reporte:
    def __init__(self, fecha, reservas, laboratorios):
        self.fecha = fecha
        self.reservas = reservas
        self.laboratorios = laboratorios

    def generar_resumen(self):
        resumen_reservas = [str(r) for r in self.reservas]
        return (f"📊 Reporte del {self.fecha}\n"
                f"Total reservas: {len(self.reservas)}\n"
                f"Laboratorios: {[lab.nombre_lab for lab in self.laboratorios]}\n"
                f"Reservas:\n" + "\n".join(resumen_reservas))


# Crear encargado admin
encargados =[
    Encargado("administrador", "admin", 999, "admin"),
    Encargado("administrador2", "admin2", 998, "admin2")
]

reserva_id_counter = 1

# Login simplificado
def login():
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    for enc in encargados:
        if enc.verificar_login(usuario, contrasena):
            print("✅ Login correcto")
            return enc
    print("Usuario o contraseña incorrectos")
    return None

# Bloques de horarios
bloques_horarios = [
    (8, 9.5),
    (9.75, 11.25),
    (11.5, 13),
    (14.5, 16),
    (16.25, 17.75)
]

bloques_texto = [
    "08:00 - 09:30",
    "09:45 - 11:15",
    "11:30 - 13:00",
    "14:30 - 16:00",
    "16:15 - 17:45"
]

# Crear reserva con cupos dinámicos
def crear_reserva(lab, fecha, bloque_idx):
    global reserva_id_counter
    curso = input("Nombre del curso: ")
    cupos = int(input(f"Número de alumnos (máx {lab.cupos_disponibles(fecha, *bloques_horarios[bloque_idx])}): "))

    if cupos > lab.cupos_disponibles(fecha, *bloques_horarios[bloque_idx]):
        print("❌ No hay suficientes cupos")
        return

    hora_inicio, hora_fin = bloques_horarios[bloque_idx]
    reserva = Reserva(reserva_id_counter, curso, fecha, hora_inicio, hora_fin)
    try:
        lab.agregar_reserva(reserva, cupos)
        print("✅ Reserva agregada correctamente")
        reserva_id_counter += 1
    except Exception as e:
        print(f"⚠️ {e}")

# Menú principal
def menu():
    print("==== Sistema de Reservas ====")
    enc = None
    while not enc:
        enc = login()

    while True:
        print("\nOpciones:")
        print("1. Crear reserva")
        print("2. Ver reservas")
        print("3. Ver reporte del día")
        print("4. Ver bloques de horarios")
        print("5. Salir")
        opcion = input("Elige opción: ")

        if opcion == "1":
            fecha = input("Fecha de reserva (YYYY-MM-DD): ")

            print("\nBloques disponibles:")
            for i, b in enumerate(bloques_texto):
                print(f"{i+1}. {b}")
            bloque_idx = int(input("Elige bloque (número): ")) - 1

            # Mostrar laboratorios con cupos disponibles para ese bloque y fecha
            print("\nLaboratorios disponibles:")
            for i, lab in enumerate(laboratorios):
                disponibles = lab.cupos_disponibles(fecha, *bloques_horarios[bloque_idx])
                print(f"{i+1}. {lab.nombre_lab} (Cupos disponibles: {disponibles}/{lab.capacidad_total})")

            lab_idx = int(input("Elige laboratorio (número): ")) - 1
            crear_reserva(laboratorios[lab_idx], fecha, bloque_idx)

        elif opcion == "2":
            for lab in laboratorios:
                print(f"\n{lab}")
                for r in lab.reservas:
                    print(r)

        elif opcion == "3":
            fecha = input("Fecha del reporte (YYYY-MM-DD): ")
            reservas_del_dia = []
            for lab in laboratorios:
                reservas_del_dia += [r for r in lab.reservas if r.fecha_reserva == fecha]
            reporte = Reporte(fecha, reservas_del_dia, laboratorios)
            print("\n" + reporte.generar_resumen())

        elif opcion == "4":
            print("\n=== Bloques de horarios disponibles ===")
            for i, b in enumerate(bloques_texto):
                print(f"{i+1}. {b}")

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción inválida")


# Ejecutar el menú
if __name__ == "__main__":
    menu()
