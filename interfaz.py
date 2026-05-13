

import re
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from logger.logger import Logger
from clases.cliente import Cliente
from clases.reserva import Reserva
from clases.servicios.reserva_sala import ReservaSala
from clases.servicios.alquiler_equipos import AlquilerEquipos
from clases.servicios.asesoria_especializada import AsesoriaEspecializada
from excepciones.excepciones import ErrorSistema, ErrorValidacion

class InterfazSoftwareFJ(tk.Tk):
    """Ventana principal """

    COLOR_FONDO = "#111827"
    COLOR_PANEL = "#1f2937"
    COLOR_ACENTO = "#f59e0b"
    COLOR_TEXTO = "#f8fafc"
    COLOR_EXITO = "#10b981"
    COLOR_ERROR = "#f97316"
    COLOR_ENTRADA = "#374151"

    NAME_PATTERN = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñÜü]+)*$")
    SIMPLE_TEXT_PATTERN = re.compile(r"^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñÜü]+(?:[ A-Za-z0-9ÁÉÍÓÚáéíóúÑñÜü\-]*[A-Za-z0-9ÁÉÍÓÚáéíóúÑñÜü])?$")
    EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}$")
    DECIMAL_PATTERN = re.compile(r"^\d+(?:\.\d+)?$")
    INTEGER_PATTERN = re.compile(r"^\d+$")
    PHONE_PATTERN = re.compile(r"^(?!([0-9])\1+$)\d{10,15}$")

    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self._clientes: list[Cliente] = []
        self._servicios: list = []
        self._reservas: list[Reserva] = []
        self._configurar_ventana()
        self._construir_ui()

"""
Módulo de interfaz gráfica Tkinter 

Autores:
    Jose Yislamer y Ruben Dario
Fecha:
    2026-05-12
"""