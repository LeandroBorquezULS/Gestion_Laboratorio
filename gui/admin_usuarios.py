# gui/admin_usuarios.py
import tkinter as tk
from tkinter import messagebox, ttk
from core.usuarios_bd import ver_usuarios_registrados, quitar_usuario

class VentanaAdminUsuarios:
    def __init__(self, admin_nombre):
        self.admin_nombre = admin_nombre
        self.ventana = tk.Tk()
        self.ventana.title(f"Administración de Usuarios - {self.admin_nombre}")

        tk.Label(self.ventana, text=f"Administrador: {self.admin_nombre}", font=("Arial", 10, "bold")).pack(pady=5)

        # Lista de usuarios
        self.tree = ttk.Treeview(self.ventana, columns=("ID", "Nombre", "Usuario", "Rol"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Rol", text="Rol")
        self.tree.pack(padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(self.ventana)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Actualizar lista", command=self._cargar_usuarios).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Quitar usuario", command=self._quitar_usuario).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Cerrar", command=self.ventana.destroy).grid(row=0, column=2, padx=5)

        self._cargar_usuarios()
        self.ventana.mainloop()

    def _cargar_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        usuarios = ver_usuarios_registrados()
        for u in usuarios:
            self.tree.insert("", tk.END, values=(u["id"], u["nombre"], u["usuario"], u["rol"]))

    def _quitar_usuario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona usuario", "Debes seleccionar un usuario")
            return

        usuario_id = self.tree.item(seleccionado[0])["values"][0]
        if quitar_usuario(usuario_id):
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
            self._cargar_usuarios()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario")