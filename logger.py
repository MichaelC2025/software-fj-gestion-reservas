"""
logger.py
Registro de eventos y errores del sistema Software FJ en un archivo de logs.
Autor: Michael Steven Calderon
"""

import logging  # Librería estándar para registrar eventos

ARCHIVO_LOG = "software_fj.log"  # Archivo donde se guardan los registros

logging.basicConfig(
    filename=ARCHIVO_LOG,  # Archivo de destino
    level=logging.INFO,  # Registra eventos informativos y errores
    format="%(asctime)s | %(levelname)s | %(message)s",  # fecha | nivel | mensaje
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato de fecha y hora
    encoding="utf-8",  # Soporta tildes y ñ
)

_logger = logging.getLogger("SoftwareFJ")  # Logger interno del sistema


def registrar_info(mensaje):
    """Registra un evento normal (ej. cliente creado, reserva confirmada)."""
    _logger.info(mensaje)


def registrar_error(error):
    """Registra un error; acepta una excepción o un texto."""
    _logger.error(str(error))  # Usa el formato [código] mensaje de las excepciones


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