"""
entidad.py
Clase abstracta base que representa las entidades generales del sistema Software FJ.
Autor: Juan Camilo Murillo Idarraga
"""

from abc import ABC, abstractmethod  # Módulo estándar para definir clases y métodos abstractos
from datetime import datetime  # Módulo para registrar la fecha y hora de creación de la entidad
from excepciones import ParametroFaltanteError  # Excepción personalizada para parámetros obligatorios

class EntidadSistema(ABC):
    """Clase abstracta base para todas las entidades del sistema (Clientes, Servicios, Reservas)."""

    def __init__(self, id_entidad):
        # Valida que el identificador de la entidad no esté vacío ni sea None
        if id_entidad is None or str(id_entidad).strip() == "":
            raise ParametroFaltanteError("id_entidad")  # Lanza error FJ-004 si falta el ID

        self.__id_entidad = str(id_entidad).strip()  # Encapsula el ID como atributo privado
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Guarda fecha de creación

    @property
    def id_entidad(self):
        """Getter que permite consultar el identificador único de la entidad."""
        return self.__id_entidad  # Retorna el ID encapsulado de solo lectura

    @property
    def fecha_creacion(self):
        """Getter que permite consultar la fecha y hora en que se creó la entidad."""
        return self.__fecha_creacion  # Retorna la marca de tiempo de creación

    @abstractmethod
    def validar_datos(self):
        """Método abstracto que obliga a las clases hijas a validar sus propios atributos."""
        pass  # Cada clase derivada debe implementar su lógica de validación

    @abstractmethod
    def obtener_resumen(self):
        """Método abstracto que obliga a las clases hijas a retornar una descripción legible."""
        pass  # Cada clase derivada debe definir cómo se presenta su información

    def __str__(self):
        """Representación en cadena estándar de cualquier entidad del sistema."""
        return f"[{self.__id_entidad}] {self.obtener_resumen()} (Creado: {self.__fecha_creacion})"
