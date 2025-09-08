# login.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.usuarios_bd import autenticar_usuario, registrar_usuario
from gui.reservas_int import VentanaPrincipal
from models.usuarios import Encargado

class VentanaLogin:
    def __init__(self):
        # Crear ventana principal de login
        self.ventana = tk.Tk()
        self.ventana.title("Login - Sistema de Reservas")
        
        # Establecer tamaño mínimo para que la ventana no se vea demasiado pequeña
        self.ventana.minsize(350, 300)

        # Etiqueta y campo para el usuario
        tk.Label(self.ventana, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_usuario.pack(pady=5)

        # Etiqueta y campo para la contraseña
        tk.Label(self.ventana, text="Contraseña:").pack(pady=5)
        self.entry_contrasena = tk.Entry(self.ventana, show="*")
        self.entry_contrasena.pack(pady=5)

        # Botón para iniciar sesión
        tk.Button(self.ventana, text="Ingresar", command=self._login).pack(pady=10)
        # Botón para abrir la ventana de registro de usuario
        tk.Button(self.ventana, text="Registrar nuevo usuario", command=self._abrir_registro).pack(pady=5)

        # Iniciar bucle principal de la interfaz gráfica
        self.ventana.mainloop()

    def _login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        user_data = autenticar_usuario(usuario, contrasena)
        if user_data:
            user_id, nombre, rol = user_data
            encargado = Encargado(nombre, usuario, user_id, contrasena)
            self.ventana.destroy()
            VentanaPrincipal(encargado)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def _abrir_registro(self):
        """Abre una ventana emergente para registrar un nuevo usuario."""
        registro = tk.Toplevel(self.ventana)
        registro.title("Registrar Usuario")
        registro.minsize(350, 300)  # Asegurar tamaño mínimo también para esta ventana

        # Campos de registro
        tk.Label(registro, text="Nombre completo:").pack(pady=5)
        entry_nombre = tk.Entry(registro)
        entry_nombre.pack(pady=5)

        tk.Label(registro, text="Usuario:").pack(pady=5)
        entry_usuario = tk.Entry(registro)
        entry_usuario.pack(pady=5)

        tk.Label(registro, text="Contraseña:").pack(pady=5)
        entry_contrasena = tk.Entry(registro, show="*")
        entry_contrasena.pack(pady=5)

        # Selección de rol con un combobox
        tk.Label(registro, text="Rol:").pack(pady=5)
        combo_rol = ttk.Combobox(registro, values=["admin"], state="readonly")  
        combo_rol.pack(pady=5)

        # Función para guardar el usuario
        def guardar_usuario():
            nombre = entry_nombre.get().strip()
            usuario = entry_usuario.get().strip()
            contrasena = entry_contrasena.get().strip()
            rol = combo_rol.get()

            # Validar que no haya campos vacíos
            if not (nombre and usuario and contrasena):
                messagebox.showwarning("Campos vacíos", "Completa todos los campos")
                return

            # Intentar registrar el usuario en la base de datos
            if registrar_usuario(nombre, usuario, contrasena, rol):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                registro.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario (¿usuario repetido?)")

        # Botón para guardar el usuario
        tk.Button(registro, text="Guardar", command=guardar_usuario).pack(pady=10)