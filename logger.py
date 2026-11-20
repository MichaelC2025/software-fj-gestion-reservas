"""
logger.py
Registro de eventos y errores del sistema Software FJ en un archivo de logs.
Autor: Michael Steven Calderon
"""

import logging  # Librería estándar para registrar eventos
import os  # Para ubicar el archivo de log junto al código fuente

# Archivo donde se guardan los registros (siempre en la carpeta del proyecto,
# sin importar desde qué directorio se ejecute el programa)
ARCHIVO_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "software_fj.log")

_logger = logging.getLogger("SoftwareFJ")  # Logger interno del sistema
_logger.setLevel(logging.INFO)  # Registra eventos informativos y errores
_logger.propagate = False  # Evita duplicar mensajes en el logger raíz

if not _logger.handlers:  # Evita agregar el manejador dos veces si el módulo se recarga
    _manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Soporta tildes y ñ
    _manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )
    _logger.addHandler(_manejador)


def registrar_info(mensaje):
    """Registra un evento normal (ej. cliente creado, reserva confirmada)."""
    _logger.info(mensaje)


def registrar_error(error):
    """Registra un error; acepta una excepción o un texto.
    Si la excepción fue encadenada (raise ... from ...), también registra la causa original."""
    mensaje = str(error)  # Usa el formato [código] mensaje de las excepciones
    causa = getattr(error, "__cause__", None)  # Excepción original del encadenamiento
    if causa is not None:
        mensaje += f" | Causa original: {type(causa).__name__}: {causa}"
    _logger.error(mensaje)


# Prueba rápida: solo se ejecuta al correr este archivo directamente
if __name__ == "__main__":
    from excepciones import ReservaInvalidaError

    registrar_info("Prueba de registro informativo")
    try:
        raise ReservaInvalidaError("La duración de la reserva debe ser mayor a cero")
    except ReservaInvalidaError as e:
        registrar_error(e)
        print("Error registrado:", e)
    print(f"Revisa el archivo {ARCHIVO_LOG}")