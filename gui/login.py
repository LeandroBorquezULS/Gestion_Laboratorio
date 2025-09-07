#login.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.usuarios_bd import autenticar_usuario, registrar_usuario
from gui.reservas import VentanaPrincipal

class VentanaLogin:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login - Sistema de Reservas")

        tk.Label(self.ventana, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_usuario.pack(pady=5)

        tk.Label(self.ventana, text="Contraseña:").pack(pady=5)
        self.entry_contrasena = tk.Entry(self.ventana, show="*")
        self.entry_contrasena.pack(pady=5)

        tk.Button(self.ventana, text="Ingresar", command=self._login).pack(pady=10)
        tk.Button(self.ventana, text="Registrar nuevo usuario", command=self._abrir_registro).pack(pady=5)

        self.ventana.mainloop()

    def _login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        user_data = autenticar_usuario(usuario, contrasena)
        if user_data:
            user_id, nombre, rol = user_data
            self.ventana.destroy()  # cerrar login
            VentanaPrincipal(usuario=nombre, rol=rol)  # abrir reservas con datos del usuario
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def _abrir_registro(self):
        registro = tk.Toplevel(self.ventana)
        registro.title("Registrar Usuario")

        tk.Label(registro, text="Nombre completo:").pack(pady=5)
        entry_nombre = tk.Entry(registro)
        entry_nombre.pack(pady=5)

        tk.Label(registro, text="Usuario:").pack(pady=5)
        entry_usuario = tk.Entry(registro)
        entry_usuario.pack(pady=5)

        tk.Label(registro, text="Contraseña:").pack(pady=5)
        entry_contrasena = tk.Entry(registro, show="*")
        entry_contrasena.pack(pady=5)

        tk.Label(registro, text="Rol:").pack(pady=5)
        combo_rol = ttk.Combobox(registro, values=["admin", "docente"], state="readonly")
        combo_rol.set("docente")
        combo_rol.pack(pady=5)

        def guardar_usuario():
            nombre = entry_nombre.get().strip()
            usuario = entry_usuario.get().strip()
            contrasena = entry_contrasena.get().strip()
            rol = combo_rol.get()

            if not (nombre and usuario and contrasena):
                messagebox.showwarning("Campos vacíos", "Completa todos los campos")
                return

            if registrar_usuario(nombre, usuario, contrasena, rol):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                registro.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario (¿usuario repetido?)")

        tk.Button(registro, text="Guardar", command=guardar_usuario).pack(pady=10)
