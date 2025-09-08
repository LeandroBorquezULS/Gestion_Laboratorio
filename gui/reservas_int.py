# gui/reservas.py
import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime
from core.reservas_bd import cupos_disponibles, crear_reserva
from gui.admin_usuarios import VentanaAdminUsuarios
from core.reportes_bd import generar_reporte_reservas_pdf
from tkinter import messagebox
from models.usuarios import Encargado


class VentanaPrincipal:
    def __init__(self, encargado):
        self.encargado = encargado
        self.usuario = encargado._nombre
        self.rol = "admin" if isinstance(encargado, Encargado) and encargado.id_encargado == 1 else "docente"


        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Reservas")

        # barra superior
        frame_top = tk.Frame(self.ventana, bg="#ddd")
        frame_top.pack(fill="x")
        tk.Label(frame_top, text=f"Conectado: {self.usuario} ({self.rol})",
                 bg="#ddd", font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=5)
        tk.Button(frame_top, text="Cerrar sesión", command=self._cerrar_sesion).pack(side="right", padx=10, pady=5)

        # botón admin
        if self.rol == "admin":
            tk.Button(frame_top, text="Ver usuarios registrados", command=self._ver_usuarios).pack(side="right", padx=10, pady=5)

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

        # Selección de curso
        tk.Label(self.frame_derecho, text="Curso:", bg="#ffffff").pack(pady=5)
        self.entry_curso = tk.Entry(self.frame_derecho, width=25)
        self.entry_curso.pack(pady=5)

        # Botón para reservar
        self.btn_reservar = tk.Button(self.frame_derecho, text="Reservar", state="disabled",
                                      command=self._reservar)
        self.btn_reservar.pack(pady=10)
        # boton de quitar reserva
        self.btn_quitar = tk.Button(self.frame_derecho, text="Quitar Reserva", state="disabled",
                            command=self._quitar_reserva)
        self.btn_quitar.pack(pady=5)

        tk.Button(self.frame_derecho, text="Generar Reporte PDF", command=self._generar_reporte_pdf).pack(pady=5)

    def _ver_usuarios(self):
        VentanaAdminUsuarios(admin_nombre=self.usuario)

    
    def _cerrar_sesion(self):
        self.ventana.destroy()
        # Importamos aquí para evitar bucles circulares
        from gui.login import VentanaLogin
        VentanaLogin()

    def _validar_fecha(self, event=None):
        fecha_seleccionada = self.fecha.get_date()
        if fecha_seleccionada.weekday() >= 5:  # 5 y 6 son sábado y domingo
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

        # Guardamos el id del bloque seleccionado siempre
        self.bloque_seleccionado = bloque_info["id"] if bloque_info else None

        if bloque_info["estado"] == "ocupado":
            self.info_label.config(
                text=f"Bloque ocupado:\n"
                    f"Fecha: {fecha_str}\n"
                    f"Horario: {bloque}\n"
                    f"Clase: {bloque_info['clase']}\n"
                    f"Encargado: {bloque_info['encargado']}"
            )
            self.btn_reservar.config(state="disabled")
            # Solo permitir quitar si el usuario es el encargado
            if bloque_info["encargado"] == self.usuario:
                self.btn_quitar.config(state="normal")
            else:
                self.btn_quitar.config(state="disabled")
        else:
            self.info_label.config(
                text=f"Bloque disponible:\n"
                    f"Fecha: {fecha_str}\n"
                    f"Horario: {bloque}"
            )
            self.btn_reservar.config(state="normal")
            self.btn_quitar.config(state="disabled")

    def _reservar(self):
        fecha_str = self.fecha.get_date().strftime("%Y-%m-%d")
        clase = self.entry_curso.get().strip()   # 🔹 ahora toma el texto escrito
        if not clase:
            self.info_label.config(text="Por favor, ingresa el nombre del curso.")
            return

        encargado = self.usuario  # El usuario actual
        exito = crear_reserva(fecha_str, self.bloque_seleccionado, clase, encargado)

        if exito:
            self.info_label.config(text="Reserva creada con éxito.")
            self.entry_curso.delete(0, tk.END)   # Limpiar campo después de reservar
            self._cargar_disponibilidad()
        else:
            self.info_label.config(text="Error: el bloque ya está reservado.")

    def _quitar_reserva(self):
        bloque_info = next((c for c in self.cupos_actuales if c["id"] == self.bloque_seleccionado), None)
        if not bloque_info or bloque_info["estado"] != "ocupado":
            self.info_label.config(text="No hay reserva que quitar en este bloque.")
            return

        if bloque_info["encargado"] != self.usuario:
            self.info_label.config(text="Solo puedes quitar tus propias reservas.")
            return

        from core.reservas_bd import eliminar_reserva
        fecha_str = self.fecha.get_date().strftime("%Y-%m-%d")
        exito = eliminar_reserva(self.bloque_seleccionado, fecha_str)

        if exito:
            self.info_label.config(text="Reserva eliminada con éxito.")
            self._cargar_disponibilidad()
            self.btn_reservar.config(state="disabled")
            self.btn_quitar.config(state="disabled")
        else:
            self.info_label.config(text="Error al eliminar la reserva.")

    def _generar_reporte_pdf(self):
        fecha_str = self.fecha.get_date().strftime("%Y-%m-%d")
        ruta = generar_reporte_reservas_pdf(fecha_str)
        messagebox.showinfo("Reporte generado", f"El reporte PDF se guardó en:\n{ruta}")

