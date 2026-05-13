

from datetime import datetime
from clases.cliente import Cliente
from clases.servicio import Servicio
from excepciones.excepciones import (
    ErrorReserva,
    ErrorReservaInvalida,
    ErrorOperacionNoPermitida,
    ErrorParametroFaltante,
    ErrorServicioNoDisponible,
    ErrorCalculoInconsistente,
)

class Reserva:
    """
    la clase que representa una reserva.
    """
    ESTADOS_VALIDOS = ["pendiente", "confirmada", "cancelada", "procesada"]
    _contador_reservas: int = 0
    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
        **kwargs
    ):
        """
        se va a crear una nueva reserva.
        """
        from logger.logger import Logger
        self._logger = Logger()
        try:
            self._validar_parametros(cliente, servicio, duracion)
            Reserva._contador_reservas += 1
            self.__id: int = Reserva._contador_reservas
            self.__cliente: Cliente = cliente
            self.__servicio: Servicio = servicio
            self.__duracion: float = duracion
            self.__kwargs: dict = kwargs
            self.__estado: str = "pendiente"
            self.__fecha_creacion: datetime = datetime.now()
            self.__fecha_confirmacion: datetime = None
            self.__costo_total: float = 0.0
            cliente.agregar_reserva(self)
            self._logger.info(
                f"Reserva Nº{self.__id} generada | "
                f"Cliente: {cliente.nombre} | "
                f"Servicio: {servicio.nombre} | "
                f"Duración: {duracion}h"
            )
        except (ErrorParametroFaltante, ErrorReservaInvalida, ErrorServicioNoDisponible):
            raise
        except Exception as e:
            raise ErrorReservaInvalida(
                f"Error inesperado al crear la reserva: {e}"
            ) from e
    @staticmethod
    def _validar_parametros(
        cliente: Cliente,
        servicio: Servicio,
        duracion: float
    ) -> None:
        try:
            if cliente is None:
                raise ErrorParametroFaltante("cliente")
            if servicio is None:
                raise ErrorParametroFaltante("servicio")
            if duracion is None:
                raise ErrorParametroFaltante("duracion")
            if not isinstance(cliente, Cliente):
                raise ErrorReservaInvalida("El parámetro 'cliente' no es instancia de Cliente")
            if not isinstance(servicio, Servicio):
                raise ErrorReservaInvalida("El parámetro 'servicio' no es instancia de Servicio")
            if not isinstance(duracion, (int, float)) or duracion <= 0:
                raise ErrorReservaInvalida(
                    f"La duración debe ser mayor a 0, recibido: {duracion}"
                )
            if not cliente.activo:
                raise ErrorReservaInvalida(
                    f"Cliente '{cliente.nombre}' inactivo"
                )
            if not servicio.disponible:
                raise ErrorServicioNoDisponible(servicio.nombre)
        except (ErrorParametroFaltante, ErrorReservaInvalida, ErrorServicioNoDisponible):
            raise
        except Exception as e:
            raise ErrorReservaInvalida(
                f"Error inesperado en validación de reserva: {e}"
            ) from e
    @property
    def id(self) -> int:
        return self.__id
    @property
    def cliente(self) -> Cliente:
        return self.__cliente
    @property
    def servicio(self) -> Servicio:
        return self.__servicio
    @property
    def duracion(self) -> float:
        return self.__duracion
    @property
    def estado(self) -> str:
        return self.__estado
    @property
    def costo_total(self) -> float:
        return self.__costo_total
    @property
    def fecha_creacion(self) -> datetime:
        return self.__fecha_creacion
    def confirmar(self) -> str:
        """
        Confirma la reserva y calcula el costo total.
        """
        try:
            if self.__estado != "pendiente":
                raise ErrorOperacionNoPermitida(
                    "confirmar",
                    f"la reserva se encuentra en estado '{self.__estado}'"
                )
            self.__costo_total = self.__servicio.calcular_costo(
                self.__duracion, **self.__kwargs
            )
            if self.__costo_total <= 0:
                raise ErrorCalculoInconsistente(
                    f"El costo calculado es inválido: {self.__costo_total}"
                )
        except (ErrorOperacionNoPermitida, ErrorCalculoInconsistente, ErrorServicioNoDisponible):
            self._logger.error(
                f"Error confirmando Reserva #{self.__id}: "
                f"{self.__estado}"
            )
            raise
        except Exception as e:
            raise ErrorReserva(
                f"Error inesperado al confirmar reserva #{self.__id}: {e}"
            ) from e
        else:
            self.__estado = "confirmada"
            self.__fecha_confirmacion = datetime.now()
            mensaje = (
                f"Reserva Nº{self.__id} confirmada | "
                f"Cliente: {self.__cliente.nombre} | "
                f"Total: ${self.__costo_total:,.2f}"
            )
            self._logger.info(mensaje)
            return mensaje
    def cancelar(self, motivo: str = "Sin motivo especificado") -> str:
        """
        Cancela la reserva.
        """
        try:
            if self.__estado in ["cancelada", "procesada"]:
                raise ErrorOperacionNoPermitida(
                    "cancelar",
                    f"la reserva ya está en estado '{self.__estado}'"
                )
        except ErrorOperacionNoPermitida:
            self._logger.error(
                f"Intento de cancelación inválido en Reserva #{self.__id}: "
                f"estado actual '{self.__estado}'"
            )
            raise
        except Exception as e:
            raise ErrorReserva(
                f"Error inesperado al cancelar reserva #{self.__id}: {e}"
            ) from e
        else:
            self.__estado = "cancelada"
            mensaje = (
                f"Reserva Nº{self.__id} cancelada | "
                f"Cliente: {self.__cliente.nombre} | "
                f"Motivo: {motivo}"
            )
            self._logger.info(mensaje)
            return mensaje
    def procesar(self) -> str:
        """
        Procesa la reserva.
        """
        try:
            if self.__estado != "confirmada":
                raise ErrorOperacionNoPermitida(
                    "procesar",
                    f"solo se puede procesar reservas confirmadas, estado actual: '{self.__estado}'"
                )
        except ErrorOperacionNoPermitida:
            self._logger.error(
                f"Intento de procesamiento inválido en Reserva #{self.__id}: "
                f"estado actual '{self.__estado}'"
            )
            raise
        except Exception as e:
            raise ErrorReserva(
                f"Error inesperado al procesar reserva #{self.__id}: {e}"
            ) from e
        else:
            self.__estado = "procesada"
            mensaje = (
                f"Reserva Nº{self.__id} procesada | "
                f"Cliente: {self.__cliente.nombre} | "
                f"Servicio: {self.__servicio.nombre} | "
                f"Duración: {self.__duracion}h | "
                f"Total pagado: ${self.__costo_total:,.2f}"
            )
            self._logger.info(mensaje)
            return mensaje
    def describir(self) -> str:
        """Retorna una descripción completa del estado de la reserva."""
        fecha_str = self.__fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        confirmacion_str = (
            self.__fecha_confirmacion.strftime("%Y-%m-%d %H:%M:%S")
            if self.__fecha_confirmacion else "Aún no confirmada"
        )
        return (
            f"Reserva #{self.__id}\n"
            f"  Cliente       : {self.__cliente.nombre}\n"
            f"  Servicio      : {self.__servicio.nombre}\n"
            f"  Duración      : {self.__duracion}h\n"
            f"  Estado        : {self.__estado.upper()}\n"
            f"  Total pagado  : ${self.__costo_total:,.2f}\n"
            f"  Creada el     : {fecha_str}\n"
            f"  Confirmación  : {confirmacion_str}"
        )
    def __str__(self) -> str:
        return (
            f"[Reserva #{self.__id}] "
            f"{self.__cliente.nombre} -> {self.__servicio.nombre} | "
            f"{self.__duracion}h | Estado: {self.__estado.upper()}"
        )

"""
Módulo con la clase Reserva.
Autores: Jose Yislamer y Ruben Dario

"""