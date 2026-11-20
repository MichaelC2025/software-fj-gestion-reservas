"""
reserva.py
Gestión del ciclo de vida de reservas en Software FJ sin base de datos.
Autor: Sebastian Aguirre Vallejo
"""

from entidad import EntidadSistema  # Clase abstracta base del sistema
from cliente import Cliente  # Clase Cliente para validar tipo de dato
from servicios import Servicio, AlquilerEquipo  # Clases de servicios para polimorfismo y control de stock
from excepciones import (  # Excepciones personalizadas del proyecto
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    CalculoCostoError,
)
from logger import registrar_info, registrar_error  # Registro en software_fj.log


class Reserva(EntidadSistema):
    """Representa una reserva que vincula un Cliente con un Servicio durante un tiempo determinado."""

    # Estados válidos del ciclo de vida de una reserva
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_PROCESADA = "PROCESADA"

    def __init__(self, id_reserva, cliente, servicio, duracion, impuesto=0.19, descuento=0.0):
        super().__init__(id_reserva)  # Inicializa id_entidad y fecha_creacion en la clase padre
        self.__cliente = None  # Atributo privado para el objeto Cliente
        self.__servicio = None  # Atributo privado para el objeto Servicio
        self.__duracion = 0  # Atributo privado para la duración en horas/días
        self.__estado = self.ESTADO_PENDIENTE  # Toda reserva inicia en estado PENDIENTE
        self.__costo_total = 0.0  # Almacena el costo calculado de la reserva

        # Validaciones mediante setters
        self.cliente = cliente  # Valida que sea instancia de Cliente
        self.servicio = servicio  # Valida que sea instancia de Servicio y esté disponible
        self.duracion = duracion  # Valida que la duración sea positiva

        # Calcula el costo inicial aprovechando el polimorfismo de Servicio
        self.__costo_total = self.__servicio.calcular_costo(
            self.__duracion, impuesto=impuesto, descuento=descuento
        )
        self.validar_datos()  # Ejecuta validación integral de la entidad

    @property
    def cliente(self):
        """Getter del cliente asociado a la reserva."""
        return self.__cliente  # Retorna objeto Cliente

    @cliente.setter
    def cliente(self, valor):
        """Valida que el cliente asignado sea un objeto Cliente válido."""
        if valor is None:  # Verifica parámetro obligatorio
            raise ParametroFaltanteError("cliente")  # Lanza FJ-004
        if not isinstance(valor, Cliente):  # Verifica tipo de instancia
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Cliente.")  # Lanza FJ-003
        self.__cliente = valor  # Guarda cliente validado

    @property
    def servicio(self):
        """Getter del servicio reservado."""
        return self.__servicio  # Retorna objeto Servicio

    @servicio.setter
    def servicio(self, valor):
        """Valida que el servicio exista y se encuentre disponible."""
        if valor is None:  # Verifica parámetro obligatorio
            raise ParametroFaltanteError("servicio")  # Lanza FJ-004
        if not isinstance(valor, Servicio):  # Verifica tipo de instancia
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Servicio.")  # Lanza FJ-003
        if not valor.disponible:  # Verifica disponibilidad del servicio
            raise ServicioNoDisponibleError(f"El servicio '{valor.nombre}' no está disponible actualmente.")
        self.__servicio = valor  # Guarda servicio validado

    @property
    def duracion(self):
        """Getter de la duración de la reserva."""
        return self.__duracion  # Retorna duración

    @duracion.setter
    def duracion(self, valor):
        """Valida que la duración sea un número mayor a cero."""
        if valor is None:  # Verifica parámetro obligatorio
            raise ParametroFaltanteError("duracion")  # Lanza FJ-004
        try:
            duracion_num = float(valor)  # Convierte a número
        except (ValueError, TypeError) as e:
            raise ReservaInvalidaError(f"La duración '{valor}' no es un número válido.") from e
        if duracion_num <= 0:  # Impide duraciones nulas o negativas
            raise ReservaInvalidaError("La duración de la reserva debe ser mayor a cero.")  # Lanza FJ-003
        self.__duracion = duracion_num  # Almacena duración validada

    @property
    def estado(self):
        """Getter del estado actual de la reserva."""
        return self.__estado  # Retorna estado actual

    @property
    def costo_total(self):
        """Getter del costo total calculado."""
        return self.__costo_total  # Retorna costo total

    def confirmar(self):
        """Cambia el estado de la reserva a CONFIRMADA si está PENDIENTE."""
        if self.__estado != self.ESTADO_PENDIENTE:  # Solo se confirman reservas pendientes
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva '{self.id_entidad}' en estado {self.__estado}."
            )
        if not self.__servicio.disponible:  # Verifica nuevamente disponibilidad antes de confirmar
            raise ServicioNoDisponibleError(f"El servicio '{self.__servicio.nombre}' dejó de estar disponible.")
        # Si es un alquiler de equipo, descuenta una unidad del stock disponible
        if isinstance(self.__servicio, AlquilerEquipo):
            self.__servicio.cantidad_disponible -= 1  # Reduce inventario en 1 unidad
        self.__estado = self.ESTADO_CONFIRMADA  # Actualiza estado a CONFIRMADA
        registrar_info(f"Reserva confirmada: {self}")  # Registra evento en software_fj.log

    def cancelar(self):
        """Cancela una reserva siempre que no haya sido cancelada ni procesada previamente."""
        if self.__estado == self.ESTADO_CANCELADA:  # Evita doble cancelación
            raise OperacionNoPermitidaError(f"La reserva '{self.id_entidad}' ya se encuentra cancelada.")
        if self.__estado == self.ESTADO_PROCESADA:  # Impide cancelar servicios ya ejecutados
            raise OperacionNoPermitidaError(f"No se puede cancelar la reserva '{self.id_entidad}' porque ya fue procesada.")
        # Si estaba confirmada y era alquiler de equipo, devuelve la unidad al inventario
        if self.__estado == self.ESTADO_CONFIRMADA and isinstance(self.__servicio, AlquilerEquipo):
            self.__servicio.cantidad_disponible += 1  # Restaura stock en 1 unidad
        self.__estado = self.ESTADO_CANCELADA  # Actualiza estado a CANCELADA
        registrar_info(f"Reserva cancelada: {self}")  # Registra evento en software_fj.log

    def procesar(self):
        """Ejecuta y finaliza una reserva que previamente haya sido CONFIRMADA."""
        if self.__estado != self.ESTADO_CONFIRMADA:  # Exige confirmación previa
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: {self.__estado})."
            )
        self.__estado = self.ESTADO_PROCESADA  # Marca la reserva como PROCESADA
        registrar_info(f"Reserva procesada y finalizada: {self}")  # Registra evento en software_fj.log

    def validar_datos(self):
        """Implementación del método abstracto de EntidadSistema para validar consistencia."""
        if not all([self.__cliente, self.__servicio]) or self.__duracion <= 0 or self.__costo_total <= 0:
            raise ReservaInvalidaError("La reserva contiene datos o cálculos inconsistentes.")
        return True  # Validación exitosa

    def obtener_resumen(self):
        """Implementación del método abstracto que resume la reserva."""
        return (
            f"Reserva de {self.__cliente.nombre} -> {self.__servicio.nombre} "
            f"({self.__duracion}h) | Total: ${self.__costo_total:,.2f} | Estado: {self.__estado}"
        )


class GestorReservas:
    """Administra las reservas en memoria sin base de datos y registra operaciones en el log."""

    def __init__(self):
        self.__reservas = []  # Lista interna encapsulada para almacenar objetos Reserva

    @property
    def reservas(self):
        """Retorna una copia de la lista de reservas registradas."""
        return list(self.__reservas)  # Protege la lista interna

    def crear_reserva(self, id_reserva, cliente, servicio, duracion, impuesto=0.19, descuento=0.0):
        """Crea y almacena una nueva reserva con bloques try/except/else/finally y encadenamiento."""
        nueva_reserva = None  # Variable temporal para la instancia
        try:
            if any(r.id_entidad == str(id_reserva).strip() for r in self.__reservas):  # Verifica ID único
                raise OperacionNoPermitidaError(f"Ya existe una reserva con el ID '{id_reserva}'.")
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion, impuesto, descuento)
        except (
            ParametroFaltanteError,
            ReservaInvalidaError,
            ServicioNoDisponibleError,
            OperacionNoPermitidaError,
            CalculoCostoError,
        ) as e:
            registrar_error(e)  # Registra el error controlado en software_fj.log
            raise  # Relanza la excepción al flujo llamador
        except Exception as e:
            # Encadena cualquier error inesperado dentro de ReservaInvalidaError
            error_encadenado = ReservaInvalidaError(f"Error inesperado al crear reserva: {e}")
            registrar_error(error_encadenado)  # Guarda error en el log
            raise error_encadenado from e  # Conserva la causa original
        else:
            self.__reservas.append(nueva_reserva)  # Guarda la reserva válida en la lista en memoria
            registrar_info(f"Reserva creada en estado PENDIENTE: {nueva_reserva}")  # Registra en log
            return nueva_reserva  # Retorna la reserva creada
        finally:
            registrar_info(f"Intento de creación de reserva '{id_reserva}' finalizado.")  # Se ejecuta siempre

    def ejecutar_accion(self, id_reserva, accion):
        """Permite confirmar, cancelar o procesar una reserva existente por su ID."""
        try:
            reserva = next((r for r in self.__reservas if r.id_entidad == str(id_reserva).strip()), None)
            if reserva is None:  # Verifica existencia en la lista interna
                raise ReservaInvalidaError(f"No existe ninguna reserva con el ID '{id_reserva}'.")

            if accion == "confirmar":  # Ejecuta confirmación
                reserva.confirmar()
            elif accion == "cancelar":  # Ejecuta cancelación
                reserva.cancelar()
            elif accion == "procesar":  # Ejecuta procesamiento final
                reserva.procesar()
            else:  # Acción desconocida
                raise OperacionNoPermitidaError(f"Acción '{accion}' no reconocida para reservas.")
        except (ReservaInvalidaError, ServicioNoDisponibleError, OperacionNoPermitidaError) as e:
            registrar_error(e)  # Registra error en software_fj.log
            raise  # Relanza al programa principal
        except Exception as e:
            # Encadenamiento ante cualquier fallo inesperado durante el cambio de estado
            error_encadenado = OperacionNoPermitidaError(f"Error inesperado al '{accion}' la reserva '{id_reserva}': {e}")
            registrar_error(error_encadenado)
            raise error_encadenado from e
        else:
            return reserva  # Retorna la reserva actualizada si no hubo errores
        finally:
            registrar_info(f"Acción '{accion}' sobre reserva '{id_reserva}' finalizada.")  # Se ejecuta siempre