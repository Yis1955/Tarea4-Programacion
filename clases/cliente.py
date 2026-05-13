

import re
from clases.entidad import Entidad
from excepciones.excepciones import (
    ErrorCliente,
    ErrorValidacion,
    ErrorParametroFaltante,
)

class Cliente(Entidad):
    """
    Clase que representa un cliente registrado.

    """

    def __init__(
        self,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str
    ):
        """
        Crea un nuevo cliente tras validar todos sus datos.

        """
        self._validar_parametros_iniciales(nombre, documento, correo, telefono)
        nombre = self._validar_nombre(nombre)
        documento = self._validar_documento(documento)
        correo = self._validar_correo(correo)
        telefono = self._validar_telefono(telefono)
        super().__init__(nombre)
        self.__documento: str = documento
        self.__correo: str = correo
        self.__telefono: str = telefono
        self.__activo: bool = True
        self.__reservas: list = []
        self.validar()

    def _validar_parametros_iniciales(self, nombre: str, documento: str, correo: str, telefono: str) -> None:
        """Valida que ningún dato crítico"""
        campos = {
            "nombre": nombre,
            "documento": documento,
            "correo": correo,
            "telefono": telefono,
        }
        for campo, valor in campos.items():
            if valor is None:
                raise ErrorParametroFaltante(campo)
            if not isinstance(valor, str) or valor.strip() == "":
                raise ErrorValidacion(campo, "no puede estar vacío")


    @property
    def documento(self) -> str:
        return self.__documento
    @property
    def correo(self) -> str:
        return self.__correo
    @property
    def telefono(self) -> str:
        return self.__telefono
    @property
    def activo(self) -> bool:
        return self.__activo
    @property
    def reservas(self) -> list:
        """Retorna copia de la lista de reservas para proteger los datos."""
        return list(self.__reservas)
    @documento.setter
    def documento(self, valor: str) -> None:
        self.__documento = self._validar_documento(valor)
    @correo.setter
    def correo(self, valor: str) -> None:
        self.__correo = self._validar_correo(valor)
    @telefono.setter
    def telefono(self, valor: str) -> None:
        self.__telefono = self._validar_telefono(valor)


    @staticmethod
    def _validar_nombre(nombre: str) -> str:
        """
        Valida que el nombre no esté vacío, tenga al menos 3 letras y sólo contenga caracteres apropiados.
        """
        if not nombre or not isinstance(nombre, str):
            raise ErrorValidacion("nombre", "debe ser texto")
        nombre = " ".join(nombre.strip().split())
        if len(nombre) < 3:
            raise ErrorValidacion("nombre", "debe tener al menos 3 caracteres")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$", nombre):
            raise ErrorValidacion("nombre", "solo puede contener letras y espacios")
        return nombre

    @staticmethod
    def _validar_documento(documento: str) -> str:
        """
        Valida que el documento de identidad tenga entre 6 y 15 dígitos.
        """
        if not documento or not isinstance(documento, str):
            raise ErrorValidacion("documento", "debe ser texto")
        documento = documento.strip()
        if not documento.isdigit():
            raise ErrorValidacion("documento", "debe contener únicamente dígitos")
        if not (6 <= len(documento) <= 15):
            raise ErrorValidacion("documento", "longitud esperada 6-15 dígitos")
        return documento

    @staticmethod
    def _validar_correo(correo: str) -> str:
        """
        Valida formato estándar de correo (usuario@dominio.ext)
        """
        if not correo or not isinstance(correo, str):
            raise ErrorValidacion("correo", "debe ser texto")
        correo = correo.strip().lower()
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, correo):
            raise ErrorValidacion("correo", f"'{correo}' tiene formato inválido")
        return correo

    @staticmethod
    def _validar_telefono(telefono: str) -> str:
        """
        Valida que el teléfono tenga entre 7 y 15 dígitos (acepta + al inicio).
        """
        if not telefono or not isinstance(telefono, str):
            raise ErrorValidacion("telefono", "debe ser texto")
        telefono = telefono.strip().replace(" ", "").replace("-", "")
        patron = r"^\+?\d{7,15}$"
        if not re.match(patron, telefono):
            raise ErrorValidacion("telefono", "formato inválido (7–15 dígitos)")
        return telefono

    # --- Métodos abstractos y sobrescritos ---
    def validar(self) -> bool:
        """
        Valida todos los datos actuales del cliente. Lanza excepción si algo es inválido.
        """
        self._validar_nombre(self._nombre)
        self._validar_documento(self.__documento)
        self._validar_correo(self.__correo)
        self._validar_telefono(self.__telefono)
        return True

    def describir(self) -> str:
        """
        Retorna una descripción completa del cliente y su estado actual.
        """
        estado = "Activo" if self.__activo else "Inactivo"
        return (
            f"Cliente #{self._id}\n"
            f"  Nombre   : {self._nombre}\n"
            f"  Documento: {self.__documento}\n"
            f"  Correo   : {self.__correo}\n"
            f"  Teléfono : {self.__telefono}\n"
            f"  Estado   : {estado}\n"
            f"  Reservas : {len(self.__reservas)}"
        )


    def agregar_reserva(self, reserva) -> None:
        """Agrega una reserva al historial del cliente."""
        if not self.__activo:
            raise ErrorCliente(f"Cliente '{self._nombre}' inactivo: no puede reservar")
        if reserva is None:
            raise ErrorParametroFaltante("reserva")
        self.__reservas.append(reserva)
    def desactivar(self) -> None:
        """Desactiva el cliente en el sistema."""
        self.__activo = False
    def activar(self) -> None:
        """Reactiva el cliente en el sistema."""
        self.__activo = True
    def __str__(self) -> str:
        return (
            f"[Cliente] {self._nombre} | "
            f"Doc: {self.__documento} | "
            f"Correo: {self.__correo} | "
            f"Tel: {self.__telefono}"
        )


"""
Módulo con la clase Cliente para Software FJ.


Autores:
    Jose Yislamer y Ruben Dario
"""