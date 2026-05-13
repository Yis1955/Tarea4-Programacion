

from clases.servicio import Servicio
from excepciones.excepciones import (
    ErrorServicio,
    ErrorCalculoInconsistente,
    ErrorParametroFaltante,
    ErrorServicioNoDisponible,
)

class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría técnica
    """

    TARIFAS_NIVEL: dict = {
        "junior": 1.0,
        "senior": 1.5,
        "experto": 2.0,
    }
    NIVELES_VALIDOS = list(TARIFAS_NIVEL.keys())

    def __init__(
        self,
        nombre: str,
        precio_base: float,
        area_especializacion: str,
        nivel: str = "junior",
        duracion_minima: float = 1.0,
        disponible: bool = True
    ):
        """
        se crea un servicio de asesoría
        """
        super().__init__(nombre, precio_base, disponible)
        nivel = nivel.strip().lower()
        if nivel not in self.NIVELES_VALIDOS:
            raise ErrorServicio(
                f"Nivel '{nivel}' no válido. Opciones: {self.NIVELES_VALIDOS}"
            )
        if not area_especializacion or not isinstance(area_especializacion, str):
            raise ErrorServicio("El área de especialización no puede estar vacía")
        if not isinstance(duracion_minima, (int, float)) or duracion_minima <= 0:
            raise ErrorServicio(
                f"La duración mínima debe ser mayor a 0, se recibió: {duracion_minima}"
            )
        self.__area_especializacion: str = area_especializacion.strip()
        self.__nivel: str = nivel
        self.__duracion_minima: float = duracion_minima
        self.validar()

    @property
    def area_especializacion(self) -> str:
        return self.__area_especializacion
    @property
    def nivel(self) -> str:
        return self.__nivel
    @property
    def duracion_minima(self) -> float:
        return self.__duracion_minima

    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """
        Calcula el costo de la asesoría según la duracion
        """
        try:
            if duracion is None:
                raise ErrorParametroFaltante("duracion")
            if not isinstance(duracion, (int, float)) or duracion <= 0:
                raise ErrorCalculoInconsistente(
                    f"La duración debe ser mayor a 0, se recibió: {duracion}"
                )
            if duracion < self.__duracion_minima:
                raise ErrorCalculoInconsistente(
                    f"La duración mínima para este servicio es {self.__duracion_minima}h, se solicitó {duracion}h"
                )
            if not self._disponible:
                raise ErrorServicioNoDisponible(self._nombre)
            multiplicador = self.TARIFAS_NIVEL[self.__nivel]
            costo = self._precio_base * multiplicador * duracion
            urgente = kwargs.get("urgente", False)
            if urgente:
                costo *= 1.20
        except (ErrorParametroFaltante, ErrorCalculoInconsistente, ErrorServicioNoDisponible):
            raise
        except Exception as e:
            raise ErrorServicio(
                f"Error inesperado al calcular costo de asesoría: {e}"
            ) from e
        else:
            return round(costo, 2)
        finally:
            pass

    def describir(self) -> str:
        """Retorna descripción completa del servicio de asesoría."""
        multiplicador = self.TARIFAS_NIVEL[self.__nivel]
        precio_real = self._precio_base * multiplicador
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"Servicio: Asesoría Especializada\n"
            f"  Nombre            : {self._nombre}\n"
            f"  Área              : {self.__area_especializacion}\n"
            f"  Nivel asesor      : {self.__nivel.capitalize()}\n"
            f"  Precio real/hora  : ${precio_real:,.2f}\n"
            f"  Duración mínima   : {self.__duracion_minima}h\n"
            f"  Estado            : {estado}"
        )

    def validar(self) -> bool:
        """Valida los datos propios de la asesoría además de los del servicio."""
        try:
            super().validar()
            if self.__nivel not in self.NIVELES_VALIDOS:
                raise ErrorServicio(f"Nivel de asesor inválido: {self.__nivel}")
            if self.__duracion_minima <= 0:
                raise ErrorServicio("La duración mínima debe ser mayor a 0")
        except ErrorServicio:
            raise
        except Exception as e:
            raise ErrorServicio(f"Error al validar AsesoriaEspecializada: {e}") from e
        else:
            return True
        finally:
            pass

    def __str__(self) -> str:
        return (
            f"[AsesoriaEspecializada] {self.__area_especializacion} | "
            f"Nivel: {self.__nivel.capitalize()} | "
            f"${self._precio_base:,.2f}/h base"
        )

"""
Módulo con el servicio de Asesoría Especializada.
Autores: Jose Yislamer y Ruben Dario

"""