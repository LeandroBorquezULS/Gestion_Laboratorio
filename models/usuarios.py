# models/usuarios.py
from core import usuarios_bd

class Persona:
    def __init__(self, nombre, usuario):
        self._nombre = nombre
        self._usuario = usuario

    def mostrar_info(self):
        return f"Persona: {self._nombre}, Usuario: {self._usuario}"


class Encargado(Persona):
    def __init__(self, nombre, usuario, id_encargado=None, contrasena=None):
        super().__init__(nombre, usuario)
        self.id_encargado = id_encargado
        self.__contrasena = contrasena

    @classmethod
    def registrar(cls, nombre, usuario, contrasena):
        if usuarios_bd.registrar_usuario(nombre, usuario, contrasena, rol="docente"):
            return cls(nombre, usuario, contrasena=contrasena)
        return None

    @classmethod
    def login(cls, usuario, contrasena):
        data = usuarios_bd.autenticar_usuario(usuario, contrasena)
        if data:  # (id, nombre, rol)
            return cls(nombre=data[1], usuario=usuario, id_encargado=data[0], contrasena=contrasena)
        return None

    def mostrar_info(self):
        return f"Encargado: {self._nombre}, Usuario: {self._usuario}, ID: {self.id_encargado}"
