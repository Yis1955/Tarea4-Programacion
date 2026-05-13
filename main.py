"""

Este archivo orquesta la simulación de operaciones 

Autores:
    Jose Yislamer y Ruben Dario
"""

from logger.logger import Logger
from clases.cliente import Cliente
from clases.reserva import Reserva
from clases.servicios.reserva_sala import ReservaSala
from clases.servicios.alquiler_equipos import AlquilerEquipos
from clases.servicios.asesoria_especializada import AsesoriaEspecializada
from excepciones.excepciones import (
    ErrorSistema, ErrorValidacion, ErrorParametroFaltante, ErrorCliente,
    ErrorServicio, ErrorReserva, ErrorOperacionNoPermitida,
    ErrorCalculoInconsistente, ErrorServicioNoDisponible,
)
from interfaz import InterfazSoftwareFJ

# Inicialización del logger principal para el registro de eventos y errores
logger = Logger()

def separador(titulo: str) -> None:
    """
    Imprime un separador visual y un título para diferenciar secciones

    """
    print("\n" + "-"*60)
    print(f"{titulo:^60}")
    print("-"*60)

def ejecutar_operaciones():
    """
    Ejecuta y simula operaciones representativas"""
    clientes = {}
    servicios = {}

    separador("OP 1 — Registro correcto: cliente natural")
    try:
        c1 = Cliente(
            nombre="Lucía Fernández",
            documento="CC123456789",
            correo="lucia.fernandez@softwarefj.com",
            telefono="3101112233"
        )
        clientes["lucia"] = c1
        print(f"Cliente registrado: {c1}")
        logger.info(f"OP1: Cliente registrado -> {c1.nombre}")
    except ErrorSistema as e:
        print(f"Error: {e}")
        logger.error(f"OP1: {e}")

    separador("OP 2 — Registro fallido: correo inválido")
    try:
        Cliente(
            nombre="Manuel Robles",
            documento="CC11223344",
            correo="correo-malformato",
            telefono="3202233455"
        )
    except ErrorValidacion as e:
        print(f"Validación fallida (esperada): {e}")
        logger.error(f"OP2: {e}")
    except ErrorSistema as e:
        print(f"Error: {e}")
        logger.error(f"OP2: {e}")

    separador("OP 3 — Registro fallido: documento ausente")
    try:
        Cliente(
            nombre="Gabriela Soto",
            documento="",
            correo="gabriela.soto@softwarefj.com",
            telefono="3153334455"
        )
    except ErrorValidacion as e:
        print(f"Validación fallida (esperada): {e}")
        logger.error(f"OP3: {e}")
    except ErrorSistema as e:
        print(f"Error: {e}")
        logger.error(f"OP3: {e}")


    separador("OP 4 — Registro correcto: cliente empresa")
    try:
        c4 = Cliente(
            nombre="Innovatec Ltda.",
            documento="NIT900123456-2",
            correo="contacto@innovatec.com",
            telefono="6014567777"
        )
        clientes["innovatec"] = c4
        print(f"Cliente registrado: {c4}")
        logger.info(f"OP4: Cliente registrado -> {c4.nombre}")
    except ErrorSistema as e:
        print(f"Error: {e}")
        logger.error(f"OP4: {e}")


    separador("OP 5 — Servicios creados: tres instancias")
    try:
        sala = ReservaSala(
            nombre="Sala Transformación Digital",
            precio_base=110000,
            capacidad_maxima=12,
            tiene_proyector=True
        )
        servicios["sala"] = sala
        print(f"{sala}")

        equipo = AlquilerEquipos(
            nombre="Alquiler Video Beam",
            precio_base=60000,
            tipo_equipo="Video Beam XGA",
            unidades_disponibles=4,
            requiere_deposito=True
        )
        servicios["equipo"] = equipo
        print(f"{equipo}")

        asesoria = AsesoriaEspecializada(
            nombre="Asesoría Seguridad Informática",
            precio_base=150000,
            area_especializacion="Seguridad Digital",
            nivel="senior",
            duracion_minima=3.0
        )
        servicios["asesoria"] = asesoria
        print(f"{asesoria}")

        logger.info("OP5: Tres servicios creados")
    except ErrorServicio as e:
        print(f"Error en servicio: {e}")
        logger.error(f"OP5: {e}")

    separador("OP 6 — Falló creación de asesoría: nivel no válido")
    try:
        AsesoriaEspecializada(
            nombre="Asesoría Bases de Datos",
            precio_base=90000,
            area_especializacion="Bases de Datos",
            nivel="maestro"  # Nivel inválido
        )
    except ErrorServicio as e:
        print(f"Error en servicio (esperado): {e}")
        logger.error(f"OP6: {e}")


    separador("SIMULACIÓN LISTA — Lanzando interfaz gráfica")
    logger.info("Simulación completada. Lanzando GUI.")

if __name__ == "__main__":
    ejecutar_operaciones()
    app = InterfazSoftwareFJ()
    app.mainloop()

"""

Este archivo orquesta la simulación de operaciones 

Autores:
    Jose Yislamer y Ruben Dario
"""
