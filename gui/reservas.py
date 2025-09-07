import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime
from core.reservas import cupos_disponibles, crear_reserva

class VentanaPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Reserva de Laboratorio')
        self._crear_widgets()
        self._cargar_disponibilidad()
        self.ventana.mainloop()

    def _crear_widgets(self):
        self.frame_principal = tk.Frame(self.ventana, bg="#f5f5f5")
        self.frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # -------- Panel izquierdo --------
        self.frame_izquierdo = tk.Frame(self.frame_principal, bg="#f5f5f5")
        self.frame_izquierdo.grid(row=0, column=0, sticky="n")

        tk.Label(self.frame_izquierdo, text="Selecciona una fecha:", bg="#f5f5f5").pack(pady=10)
        self.fecha = DateEntry(
            self.frame_izquierdo,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/yyyy",
            mindate=datetime.today()
        )
        self.fecha.pack(pady=5)

        # Guardamos la fecha inicial válida
        self.fecha_valida = self.fecha.get_date()
        self.fecha.bind("<<DateEntrySelected>>", self._validar_fecha)

        tk.Label(self.frame_izquierdo, text="Selecciona un bloque:", bg="#f5f5f5").pack(pady=10)
        bloques = [
            "08:00 - 09:30",
            "09:45 - 11:15",
            "11:30 - 13:00",
            "14:30 - 16:00",
            "16:15 - 17:45",
            "18:00 - 19:30"
        ]

        self.botones_bloques = []
        for bloque in bloques:
            btn = tk.Button(self.frame_izquierdo, text=bloque, width=20,
                            command=lambda b=bloque: self._seleccionar_bloque(b))
            btn.pack(pady=5)
            self.botones_bloques.append(btn)

        # -------- Panel derecho --------
        self.frame_derecho = tk.Frame(self.frame_principal, bg="#ffffff", relief="solid", bd=1)
        self.frame_derecho.grid(row=0, column=1, padx=20, sticky="n")

        tk.Label(self.frame_derecho, text="Información del bloque:", bg="#ffffff",
                 font=("Arial", 10, "bold")).pack(pady=10)
        self.info_label = tk.Label(self.frame_derecho,
                                   text="Selecciona un bloque para ver más detalles.",
                                   bg="#ffffff", wraplength=200, justify="left")
        self.info_label.pack(pady=10)

        # Entrada para el nombre del curso
        tk.Label(self.frame_derecho, text="Nombre del curso:", bg="#ffffff").pack(pady=5)
        self.entry_curso = tk.Entry(self.frame_derecho, width=25)
        self.entry_curso.pack(pady=5)

        # Botón para reservar
        self.btn_reservar = tk.Button(self.frame_derecho, text="Reservar", state="disabled",
                                      command=self._reservar)
        self.btn_reservar.pack(pady=10)

    def _validar_fecha(self, event=None):
        fecha_seleccionada = self.fecha.get_date()
        if fecha_seleccionada.weekday() >= 5:
            self.fecha.set_date(self.fecha_valida)
        else:
            self.fecha_valida = fecha_seleccionada
            self._cargar_disponibilidad()

    def _cargar_disponibilidad(self):
        fecha_str = self.fecha.get_date().strftime("%Y-%m-%d")
        cupos = cupos_disponibles(fecha_str)

        for i, btn in enumerate(self.botones_bloques):
            estado = cupos[i]["estado"]
            if estado == "ocupado":
                btn.config(bg="#ffcccc", state="normal")
            else:
                btn.config(bg="SystemButtonFace", state="normal")

        self.cupos_actuales = cupos

    def _seleccionar_bloque(self, bloque):
        fecha_str = self.fecha.get_date().strftime("%Y-%m-%d")
        bloque_info = next((c for c in self.cupos_actuales if c["bloque"] == bloque), None)

        if bloque_info["estado"] == "ocupado":
            self.info_label.config(
                text=f"Bloque ocupado:\n"
                     f"Fecha: {fecha_str}\n"
                     f"Horario: {bloque}\n"
                     f"Clase: {bloque_info['clase']}\n"
                     f"Encargado: {bloque_info['encargado']}"
            )
            self.btn_reservar.config(state="disabled")
        else:
            self.info_label.config(
                text=f"Bloque disponible:\n"
                     f"Fecha: {fecha_str}\n"
                     f"Horario: {bloque}"
            )
            self.bloque_seleccionado = bloque_info["id"]
            self.btn_reservar.config(state="normal")

    def _reservar(self):
        fecha_str = self.fecha.get_date().strftime("%Y-%m-%d")
        clase = self.entry_curso.get().strip()
        if not clase:
            self.info_label.config(text="Por favor, ingresa el nombre del curso.")
            return

        encargado = "Usuario demo"  # Placeholder hasta implementar login
        exito = crear_reserva(fecha_str, self.bloque_seleccionado, clase, encargado)

        if exito:
            self.info_label.config(text="Reserva creada con éxito.")
            self.entry_curso.delete(0, tk.END)
            self._cargar_disponibilidad()
        else:
            self.info_label.config(text="Error: el bloque ya está reservado.")
