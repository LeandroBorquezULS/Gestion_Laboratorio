# main.py
from core.database import inicializar_bd
from gui.login import VentanaLogin

if __name__ == "__main__":
    inicializar_bd()   # crea las tablas si no existen
    VentanaLogin()     # abrir ventana de login.