"""
cliente.py
Gestión y encapsulación de clientes del sistema Software FJ sin uso de bases de datos.
Autor: Juan Camilo Murillo Idarraga
"""

from entidad import EntidadSistema  # Importa la clase abstracta base
from excepciones import ClienteInvalidoError, ParametroFaltanteError, OperacionNoPermitidaError  # Excepciones del sistema
from logger import registrar_info, registrar_error  # Funciones para registrar eventos en software_fj.log

class Cliente(EntidadSistema):
    """Clase que representa a un cliente de Software FJ con encapsulación y validaciones estrictas."""

def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)  # Inicializa id_entidad y fecha_creacion en la clase padre
