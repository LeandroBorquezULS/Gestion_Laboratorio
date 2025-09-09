class Persona:
  

    def __init__(self, nombre, usuario):
    
        #Inicializa una persona con su nombre y usuario.
        
        self._nombre = nombre
        self._usuario = usuario

    def mostrar_info(self):

        return f"Persona: {self._nombre}, Usuario: {self._usuario}"

class Encargado(Persona):
    """
    Clase que representa a un encargado del sistema.
    
    Hereda de Persona e incluye autenticación.
    """

    def __init__(self, nombre, usuario, id_encargado, contrasena):

        #Inicializa un encargado con su ID y contraseña.
        
        super().__init__(nombre, usuario)
        self.id_encargado = id_encargado
        self.__contrasena = contrasena  # Atributo privado

    def verificar_login(self, usuario, contrasena):

        return self._usuario == usuario and self.__contrasena == contrasena

    def mostrar_info(self):
  
        return f"Encargado: {self._nombre}, Usuario: {self._usuario}"
