from utils.persona import Encargado
from utils.laboratorios import Laboratorio

encargados = [
    Encargado("administrador", "admin", 999, "admin"),
    Encargado("administrador2", "admin2", 998, "admin2")
]

reserva_id_counter = 1

bloques_horarios = [
    (8, 9.5),
    (9.75, 11.25),
    (11.5, 13),
    (14.5, 16),
    (16.25, 17.75)
]

bloques_texto = [
    "08:00 - 09:30",
    "09:45 - 11:15",
    "11:30 - 13:00",
    "14:30 - 16:00",
    "16:15 - 17:45"
]

laboratorios = [
    Laboratorio(1, "Lab Computación"),
    Laboratorio(2, "Lab Electrónica"),
    Laboratorio(3, "Lab Física")
]
