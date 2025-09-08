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
