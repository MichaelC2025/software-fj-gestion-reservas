"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Autor: Michael Steven Calderon
"""


class ErrorSistemaFJ(Exception):
    """Excepción base del sistema. Todas las demás heredan de esta."""

    codigo = "FJ-000"  # Código por defecto del error

    def __init__(self, mensaje):
        super().__init__(mensaje)  # Guarda el mensaje en la clase Exception
        self.mensaje = mensaje  # Guarda el mensaje como atributo propio

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"  # Formato: [código] mensaje


class ClienteInvalidoError(ErrorSistemaFJ):
    """Datos del cliente incorrectos o incompletos."""
    codigo = "FJ-001"


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """El servicio no existe o no está disponible."""
    codigo = "FJ-002"


class ReservaInvalidaError(ErrorSistemaFJ):
    """La reserva tiene datos o un estado no válido."""
    codigo = "FJ-003"


class ParametroFaltanteError(ErrorSistemaFJ):
    """Falta un parámetro obligatorio."""
    codigo = "FJ-004"

    def __init__(self, parametro):
        super().__init__(f"Falta el parámetro obligatorio: '{parametro}'")  # Arma el mensaje con el nombre del parámetro


class CalculoCostoError(ErrorSistemaFJ):
    """Costo, impuesto o descuento con valor inválido."""
    codigo = "FJ-005"


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Operación no permitida, como cancelar una reserva ya cancelada."""
    codigo = "FJ-006"


# Prueba rápida: solo se ejecuta al correr este archivo directamente
if __name__ == "__main__":
    try:
        raise ClienteInvalidoError("El correo del cliente no es válido")  # Provoca el error a propósito
    except ErrorSistemaFJ as e:  # Lo captura con la clase padre (herencia)
        print(e)  # Muestra: [FJ-001] El correo del cliente no es válido