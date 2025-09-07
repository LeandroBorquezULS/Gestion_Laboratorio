# main.py
from gui.reservas import VentanaPrincipal
from core.database import inicializar_bd
from gui.reservas import VentanaPrincipal

if __name__ == "__main__":
    inicializar_bd()  # <-- crea tablas y bloques si no existen
    VentanaPrincipal()