

import logging
import os
from datetime import datetime

class Logger:
    """
    Sistema de logging centralizado.
    """
    _instancia = None
    _inicializado = False
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    def __init__(self):
        if Logger._inicializado:
            return
        Logger._inicializado = True
        os.makedirs("logs", exist_ok=True)
        nombre_archivo = "logs/sistema.log"
        self._logger = logging.getLogger("PlataformaNueva")
        self._logger.setLevel(logging.DEBUG)
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        manejador_archivo = logging.FileHandler(
            nombre_archivo, encoding="utf-8"
        )
        manejador_archivo.setLevel(logging.DEBUG)
        manejador_archivo.setFormatter(formato)
        manejador_consola = logging.StreamHandler()
        manejador_consola.setLevel(logging.INFO)
        manejador_consola.setFormatter(formato)
        self._logger.addHandler(manejador_archivo)
        self._logger.addHandler(manejador_consola)
        self._logger.info(" " * 60)
        self._logger.info("Plataforma Nueva: sistema iniciado")
        self._logger.info(
            f"Inicio de sesión: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._logger.info(" " * 60)
    def info(self, mensaje: str) -> None:
        try:
            self._logger.info(mensaje)
        except Exception as e:
            print(f"[Logger] Fallo registrando INFO: {e}")
    def warning(self, mensaje: str) -> None:
        try:
            self._logger.warning(mensaje)
        except Exception as e:
            print(f"[Logger] Fallo registrando WARNING: {e}")
    def error(self, mensaje: str) -> None:
        try:
            self._logger.error(mensaje)
        except Exception as e:
            print(f"[Logger] Fallo registrando ERROR: {e}")
    def critico(self, mensaje: str) -> None:
        try:
            self._logger.critical(mensaje)
        except Exception as e:
            print(f"[Logger] Fallo registrando CRITICAL: {e}")
    def registrar_excepcion(self, excepcion: Exception, contexto: str = "") -> None:
        try:
            prefijo = f"[{contexto}] " if contexto else ""
            self._logger.error(
                f"{prefijo}{type(excepcion).__name__}: {excepcion}",
                exc_info=True
            )
        except Exception as e:
            print(f"[Logger] Fallo registrando excepción: {e}")

"""
Módulo del sistema de logs.
Autores: Jose Yislamer y Ruben Dario

"""