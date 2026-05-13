# Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto académico de Programación Orientada a Objetos - Python  
Universidad Nacional Abierta y a Distancia (UNAD)  
Curso: Programación | Código: 213023

---

## Descripción General

Este sistema es una solución modular para la gestión de clientes, servicios y reservas, desarrollada completamente en Python con Programación Orientada a Objetos (POO).

El sistema ofrece tres tipos de servicios principales:
- Reserva de salas de reuniones y conferencias.
- Alquiler de equipos tecnológicos.
- Asesorías profesionales especializadas.

---

## Equipo de Desarrollo

| Integrante     | Rol principal              |
|----------------|---------------------------|
| Jose Yislamer  | Coautor y Arquitecto      |
| Ruben Dario    | Coautor y Desarrollador   |

---

## Estructura del Proyecto

```
Tarea4-Programacion/
├── clases/
│   ├── __init__.py
│   ├── entidad.py
│   ├── servicio.py
│   ├── cliente.py
│   ├── reserva.py
│   └── servicios/
│       ├── __init__.py
│       ├── reserva_sala.py
│       ├── alquiler_equipos.py
│       └── asesoria_especializada.py
├── excepciones/
│   ├── __init__.py
│   └── excepciones.py
├── logger/
│   ├── __init__.py
│   └── logger.py
├── logs/
│   └── sistema.log
├── interfaz.py
├── main.py
├── .gitignore
└── README.md
```

---

## Principios de POO Aplicados
- **Abstracción**: Las clases base y servicios emplean métodos abstractos con distintas implementaciones.
- **Herencia**: Jerarquía clara entre entidades, servicios y reservas.
- **Polimorfismo**: Cada tipo de servicio implementa sus propias reglas para el cálculo de costo y descripción.
- **Encapsulación**: Acceso controlado a los atributos mediante propiedades.
- **Manejo avanzado de excepciones**: Jerarquía propia para errores de cliente, servicio y reserva.

---

## Flujo de Estados y Manejo de Operaciones

Las reservas pasan por los siguientes estados:
- **pendiente**
- **confirmada**
- **procesada**
- **cancelada**

Cada operación cuenta con validación estricta y registro en el sistema de logs tanto en consola como en archivo.

---

## Instalación y Ejecución

**Requisitos:**
- Python 3.10 o superior (incluye Tkinter)
- No requiere librerías adicionales de terceros

**Pasos:**
1. Clonar el repositorio:
   ```
   git clone https://github.com/Yis1955/Tarea4-Programacion.git
   ```
2. Acceder a la carpeta del proyecto:
   ```
   cd Tarea4-Programacion
   ```
3. Ejecutar el sistema:
   ```
   python main.py
   ```

Al ejecutar `main.py`:
- Se simulan varias operaciones automáticas en consola/documentación.
- Se crea o actualiza el archivo de logs (`logs/sistema.log`).
- Se abre la interfaz gráfica (Tkinter).

---

## Sistema de Logs
Todos los eventos y errores relevantes se registran en el archivo `logs/sistema.log`, facilitando la trazabilidad y la solución de incidencias.

---

## Licencia
Repositorio académico creado como parte del curso de Programación (213023) de la Universidad Nacional Abierta y a Distancia - UNAD.

Autores: Jose Yislam y Ruben Dario
