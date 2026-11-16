"""
servicios.py
Definición de la jerarquía de servicios y gestión en memoria para Software FJ.
Autor: Sebastian Aguirre Vallejo
"""

from abc import abstractmethod  # Decorador para definir métodos abstractos en Servicio
from entidad import EntidadSistema  # Clase abstracta base del sistema
from excepciones import (  # Excepciones personalizadas definidas en excepciones.py
    ServicioNoDisponibleError,
    ParametroFaltanteError,
    CalculoCostoError,
    OperacionNoPermitidaError,
)
from logger import registrar_info, registrar_error  # Funciones de registro en software_fj.log


class Servicio(EntidadSistema):
    """Clase abstracta que representa un servicio genérico ofrecido por Software FJ."""

    def __init__(self, id_servicio, nombre, tarifa_base, disponible=True):
        super().__init__(id_servicio)  # Inicializa id_entidad y fecha_creacion en EntidadSistema
        self.__nombre = None  # Atributo privado para el nombre del servicio
        self.__tarifa_base = 0.0  # Atributo privado para el valor base por hora o unidad
        self.__disponible = True  # Atributo privado que indica si el servicio está activo

        # Asigna los valores mediante setters para ejecutar las validaciones
        self.nombre = nombre  # Valida y asigna el nombre del servicio
        self.tarifa_base = tarifa_base  # Valida y asigna la tarifa base
        self.disponible = disponible  # Valida y asigna el estado de disponibilidad

    @property
    def nombre(self):
        """Getter del nombre del servicio."""
        return self.__nombre  # Retorna el nombre encapsulado

    @nombre.setter
    def nombre(self, valor):
        """Setter del nombre con validación de parámetro obligatorio."""
        if valor is None or str(valor).strip() == "":  # Verifica que el nombre no esté vacío
            raise ParametroFaltanteError("nombre")  # Lanza FJ-004 si falta el nombre
        self.__nombre = str(valor).strip()  # Guarda el nombre limpio

    @property
    def tarifa_base(self):
        """Getter de la tarifa base del servicio."""
        return self.__tarifa_base  # Retorna la tarifa base encapsulada

    @tarifa_base.setter
    def tarifa_base(self, valor):
        """Setter de la tarifa base asegurando que sea un número positivo."""
        if valor is None:  # Verifica si el parámetro fue omitido
            raise ParametroFaltanteError("tarifa_base")  # Lanza FJ-004
        try:
            tarifa_num = float(valor)  # Intenta convertir el valor a número decimal
        except (ValueError, TypeError) as e:
            # Encadenamiento de excepción si el dato no es numérico
            raise CalculoCostoError(f"La tarifa base '{valor}' debe ser numérica.") from e
        if tarifa_num <= 0:  # La tarifa no puede ser cero ni negativa
            raise CalculoCostoError("La tarifa base debe ser mayor a cero.")  # Lanza FJ-005
        self.__tarifa_base = tarifa_num  # Almacena la tarifa validada

    @property
    def disponible(self):
        """Getter del estado de disponibilidad del servicio."""
        return self.__disponible  # Retorna True si está disponible, False si no

    @disponible.setter
    def disponible(self, valor):
        """Setter de disponibilidad validando tipo booleano."""
        if not isinstance(valor, bool):  # Verifica que el valor sea True o False
            raise ServicioNoDisponibleError("El estado de disponibilidad debe ser booleano (True/False).")
        self.__disponible = valor  # Actualiza el estado de disponibilidad

    def _aplicar_ajustes_costo(self, subtotal, impuesto=0.19, descuento=0.0, recargo_extra=0.0):
        """Método auxiliar sobrecargado por parámetros opcionales para calcular impuestos, descuentos y recargos."""
        # Valida que los porcentajes y recargos estén dentro de rangos lógicos
        if not (0 <= impuesto <= 1):  # El impuesto debe estar entre 0 % (0.0) y 100 % (1.0)
            raise CalculoCostoError(f"Porcentaje de impuesto inválido: {impuesto}.")  # Lanza FJ-005
        if not (0 <= descuento <= 1):  # El descuento debe estar entre 0 % y 100 %
            raise CalculoCostoError(f"Porcentaje de descuento inválido: {descuento}.")  # Lanza FJ-005
        if recargo_extra < 0:  # No se permiten recargos negativos
            raise CalculoCostoError("El recargo extra no puede ser negativo.")  # Lanza FJ-005

        monto_descuento = subtotal * descuento  # Calcula el valor a descontar
        base_gravable = (subtotal - monto_descuento) + recargo_extra  # Resta descuento y suma recargo
        monto_impuesto = base_gravable * impuesto  # Calcula el impuesto sobre la base gravable
        return round(base_gravable + monto_impuesto, 2)  # Retorna el total redondeado a 2 decimales

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo_extra=0.0):
        """Método abstracto polimórfico para calcular el costo según la duración y parámetros opcionales."""
        pass  # Cada servicio especializado implementará su propia fórmula

    @abstractmethod
    def describir_servicio(self):
        """Método abstracto polimórfico que detalla las características técnicas del servicio."""
        pass  # Cada clase hija devolverá su descripción específica

    def obtener_resumen(self):
        """Implementación del método de EntidadSistema usando polimorfismo con describir_servicio."""
        estado = "Disponible" if self.__disponible else "No disponible"  # Traduce booleano a texto
        return f"{self.describir_servicio()} | Tarifa: ${self.__tarifa_base:,.2f} | Estado: {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(self, id_servicio, nombre, tarifa_base, capacidad_personas, tiene_proyector=True, disponible=True):
        self.__capacidad_personas = 0  # Inicializa capacidad privada
        self.__tiene_proyector = False  # Inicializa indicador de proyector
        super().__init__(id_servicio, nombre, tarifa_base, disponible)  # Llama al constructor de Servicio
        self.capacidad_personas = capacidad_personas  # Valida y asigna capacidad
        self.tiene_proyector = bool(tiene_proyector)  # Asigna disponibilidad de proyector
        self.validar_datos()  # Ejecuta validación integral

    @property
    def capacidad_personas(self):
        """Getter de la capacidad máxima de la sala."""
        return self.__capacidad_personas  # Retorna el número de personas

    @capacidad_personas.setter
    def capacidad_personas(self, valor):
        """Setter de capacidad asegurando que sea un entero positivo."""
        if valor is None:  # Verifica que el parámetro exista
            raise ParametroFaltanteError("capacidad_personas")  # Lanza FJ-004
        if not isinstance(valor, int) or valor <= 0:  # Debe ser entero mayor a cero
            raise ServicioNoDisponibleError("La capacidad de la sala debe ser un entero mayor a cero.")
        self.__capacidad_personas = valor  # Almacena la capacidad validada

    def validar_datos(self):
        """Valida los atributos específicos de la sala."""
        if self.__capacidad_personas <= 0 or self.tarifa_base <= 0:  # Comprueba consistencia
            raise ServicioNoDisponibleError("Datos inconsistentes en la configuración de la sala.")
        return True  # Validación exitosa

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo_extra=0.0):
        """Calcula el costo de la sala por hora; aplica descuento automático del 10 % si dura 5 o más horas."""
        if duracion is None or duracion <= 0:  # Valida duración positiva
            raise CalculoCostoError("La duración de reserva de sala debe ser mayor a cero.")  # Lanza FJ-005
        subtotal = self.tarifa_base * duracion  # Costo base por horas
        if self.__tiene_proyector:  # Suma tarifa fija de uso de proyector si aplica
            subtotal += 15000.0  # Cargo fijo por equipamiento audiovisual
        descuento_efectivo = max(descuento, 0.10) if duracion >= 5 else descuento  # Aplica promo por jornada larga
        return self._aplicar_ajustes_costo(subtotal, impuesto, descuento_efectivo, recargo_extra)  # Calcula total

    def describir_servicio(self):
        """Sobrescribe la descripción para mostrar datos propios de la sala."""
        proyector_txt = "con proyector" if self.__tiene_proyector else "sin proyector"  # Texto descriptivo
        return f"Sala '{self.nombre}' (Capacidad: {self.__capacidad_personas} pers., {proyector_txt})"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos (portátiles, servidores, etc.)."""

    def __init__(self, id_servicio, nombre, tarifa_base, tipo_equipo, cantidad_disponible, disponible=True):
        self.__tipo_equipo = None  # Inicializa tipo de equipo
        self.__cantidad_disponible = 0  # Inicializa inventario disponible
        super().__init__(id_servicio, nombre, tarifa_base, disponible)  # Inicializa clase padre
        self.tipo_equipo = tipo_equipo  # Valida y asigna tipo de equipo
        self.cantidad_disponible = cantidad_disponible  # Valida y asigna stock
        self.validar_datos()  # Ejecuta validación integral

    @property
    def cantidad_disponible(self):
        """Getter de las unidades disponibles del equipo."""
        return self.__cantidad_disponible  # Retorna unidades en inventario

    @cantidad_disponible.setter
    def cantidad_disponible(self, valor):
        """Setter de unidades disponibles."""
        if valor is None:  # Verifica parámetro obligatorio
            raise ParametroFaltanteError("cantidad_disponible")  # Lanza FJ-004
        if not isinstance(valor, int) or valor < 0:  # No permite stock negativo
            raise ServicioNoDisponibleError("La cantidad disponible de equipos no puede ser negativa.")
        self.__cantidad_disponible = valor  # Guarda cantidad
        if self.__cantidad_disponible == 0:  # Si no quedan equipos, marca como no disponible
            self.disponible = False  # Actualiza estado

    @property
    def tipo_equipo(self):
        """Getter del tipo de equipo."""
        return self.__tipo_equipo  # Retorna categoría del equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        """Setter del tipo de equipo."""
        if valor is None or str(valor).strip() == "":  # Verifica que no sea vacío
            raise ParametroFaltanteError("tipo_equipo")  # Lanza FJ-004
        self.__tipo_equipo = str(valor).strip()  # Guarda tipo limpio

    def validar_datos(self):
        """Valida que el equipo tenga categoría y stock coherente."""
        if not self.__tipo_equipo or self.__cantidad_disponible < 0:  # Comprueba atributos
            raise ServicioNoDisponibleError("Datos inválidos para el alquiler de equipo.")
        return True  # Validación exitosa

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo_extra=0.0):
        """Calcula el costo de alquiler incluyendo póliza de seguro obligatorio del 5 % sobre el subtotal."""
        if duracion is None or duracion <= 0:  # Valida duración positiva
            raise CalculoCostoError("La duración del alquiler debe ser mayor a cero.")  # Lanza FJ-005
        subtotal = self.tarifa_base * duracion  # Costo base por tiempo de uso
        seguro_equipo = subtotal * 0.05  # Calcula seguro obligatorio del 5 %
        return self._aplicar_ajustes_costo(subtotal, impuesto, descuento, recargo_extra + seguro_equipo)

    def describir_servicio(self):
        """Sobrescribe la descripción con detalles del equipo tecnológico."""
        return f"Equipo '{self.nombre}' [Tipo: {self.__tipo_equipo} | Stock: {self.__cantidad_disponible}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría y asesoría técnica por expertos."""

    def __init__(self, id_servicio, nombre, tarifa_base, especialidad, nivel_consultor="Senior", disponible=True):
        self.__especialidad = None  # Inicializa área de especialidad
        self.__nivel_consultor = None  # Inicializa nivel del consultor
        super().__init__(id_servicio, nombre, tarifa_base, disponible)  # Inicializa clase padre
        self.especialidad = especialidad  # Valida y asigna especialidad
        self.nivel_consultor = nivel_consultor  # Valida y asigna nivel
        self.validar_datos()  # Ejecuta validación integral

    @property
    def especialidad(self):
        """Getter del área de especialidad."""
        return self.__especialidad  # Retorna especialidad

    @especialidad.setter
    def especialidad(self, valor):
        """Setter de especialidad."""
        if valor is None or str(valor).strip() == "":  # Verifica que no esté vacía
            raise ParametroFaltanteError("especialidad")  # Lanza FJ-004
        self.__especialidad = str(valor).strip()  # Guarda especialidad limpia

    @property
    def nivel_consultor(self):
        """Getter del nivel del consultor."""
        return self.__nivel_consultor  # Retorna nivel

    @nivel_consultor.setter
    def nivel_consultor(self, valor):
        """Setter que valida que el nivel sea Junior, Semi-Senior o Senior."""
        niveles_validos = ("Junior", "Semi-Senior", "Senior")  # Niveles permitidos en Software FJ
        if valor not in niveles_validos:  # Verifica pertenencia a la tupla
            raise ServicioNoDisponibleError(f"Nivel de consultor inválido. Use: {niveles_validos}.")
        self.__nivel_consultor = valor  # Guarda nivel validado

    def validar_datos(self):
        """Valida los parámetros propios de la asesoría."""
        if not self.__especialidad or not self.__nivel_consultor:  # Comprueba campos obligatorios
            raise ServicioNoDisponibleError("La asesoría requiere especialidad y nivel de consultor.")
        return True  # Validación exitosa

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, recargo_extra=0.0):
        """Calcula el costo aplicando un multiplicador según la experiencia del consultor."""
        if duracion is None or duracion <= 0:  # Valida duración positiva
            raise CalculoCostoError("La duración de la asesoría debe ser mayor a cero.")  # Lanza FJ-005
        factores = {"Junior": 1.0, "Semi-Senior": 1.25, "Senior": 1.5}  # Factor multiplicador por nivel
        subtotal = (self.tarifa_base * factores[self.__nivel_consultor]) * duracion  # Aplica tarifa ajustada
        return self._aplicar_ajustes_costo(subtotal, impuesto, descuento, recargo_extra)  # Calcula total

    def describir_servicio(self):
        """Sobrescribe la descripción con la especialidad y nivel del consultor."""
        return f"Asesoría '{self.nombre}' [Área: {self.__especialidad} | Consultor: {self.__nivel_consultor}]"


class GestorServicios:
    """Administra en memoria el catálogo de servicios de Software FJ sin base de datos."""

    def __init__(self):
        self.__servicios = []  # Lista interna encapsulada de objetos Servicio

    @property
    def servicios(self):
        """Retorna una copia de la lista de servicios para evitar alteraciones externas."""
        return list(self.__servicios)  # Devuelve copia segura

    def registrar_servicio(self, servicio):
        """Agrega un objeto Servicio validado a la lista en memoria y registra el evento en el log."""
        try:
            if not isinstance(servicio, Servicio):  # Verifica que sea una instancia derivada de Servicio
                raise ServicioNoDisponibleError("El objeto proporcionado no es un Servicio válido.")
            # Evita IDs duplicados en el catálogo en memoria
            if any(s.id_entidad == servicio.id_entidad for s in self.__servicios):
                raise OperacionNoPermitidaError(f"Ya existe un servicio con el ID '{servicio.id_entidad}'.")
        except (ServicioNoDisponibleError, OperacionNoPermitidaError, ParametroFaltanteError, CalculoCostoError) as e:
            registrar_error(e)  # Registra el error controlado en software_fj.log
            raise  # Relanza la excepción al flujo principal
        except Exception as e:
            # Encadenamiento de excepciones ante fallos imprevistos
            error_encadenado = ServicioNoDisponibleError(f"Fallo inesperado al registrar servicio: {e}")
            registrar_error(error_encadenado)  # Guarda traza en el log
            raise error_encadenado from e  # Preserva la excepción original
        else:
            self.__servicios.append(servicio)  # Añade el servicio a la lista interna
            registrar_info(f"Servicio registrado: {servicio}")  # Registra éxito en el log
            return servicio  # Retorna el servicio registrado
        finally:
            pass  # Cierre controlado de la operación

    def buscar_servicio(self, id_servicio):
        """Busca un servicio por su identificador; lanza excepción si no existe."""
        id_limpio = str(id_servicio).strip()  # Limpia espacios
        for servicio in self.__servicios:  # Recorre la lista interna
            if servicio.id_entidad == id_limpio:  # Compara identificadores
                return servicio  # Retorna el objeto encontrado
        error = ServicioNoDisponibleError(f"No se encontró ningún servicio con ID '{id_servicio}'.")
        registrar_error(error)  # Registra el fallo de búsqueda
        raise error  # Lanza excepción FJ-002