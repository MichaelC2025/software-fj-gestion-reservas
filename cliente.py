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
        self.__nombre = None  # Inicializa atributo privado para el nombre completo
        self.__correo = None  # Inicializa atributo privado para el correo electrónico
        self.__telefono = None  # Inicializa atributo privado para el número telefónico

        # Asigna los valores usando los setters para ejecutar todas las validaciones
        self.nombre = nombre  # Valida y encapsula el nombre
        self.correo = correo  # Valida y encapsula el correo
        self.telefono = telefono  # Valida y encapsula el teléfono

        self.validar_datos()  # Ejecuta la validación integral implementada de la clase abstracta

    @property
    def nombre(self):
        """Getter del nombre del cliente."""
        return self.__nombre  # Retorna el nombre privado

    @nombre.setter
    def nombre(self, valor):
        """Setter del nombre con validación de parámetro obligatorio y longitud mínima."""
        if valor is None or str(valor).strip() == "":  # Verifica si el dato viene vacío
            raise ParametroFaltanteError("nombre")  # Lanza excepción FJ-004
        nombre_limpio = str(valor).strip()  # Elimina espacios innecesarios en los extremos
        if len(nombre_limpio) < 3 or any(char.isdigit() for char in nombre_limpio):  # Evita nombres muy cortos o con números
            raise ClienteInvalidoError("El nombre debe tener al menos 3 letras y no contener números.")  # Lanza FJ-001
        self.__nombre = nombre_limpio  # Almacena el nombre validado

    @property
    def correo(self):
        """Getter del correo electrónico del cliente."""
        return self.__correo  # Retorna el correo privado

    @correo.setter
    def correo(self, valor):
        """Setter del correo con validación de formato estándar."""
        if valor is None or str(valor).strip() == "":  # Verifica si el dato viene vacío
            raise ParametroFaltanteError("correo")  # Lanza excepción FJ-004
        correo_limpio = str(valor).strip().lower()  # Normaliza el correo a minúsculas sin espacios
        if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:  # Verifica presencia de '@' y dominio con '.'
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")  # Lanza FJ-001
        self.__correo = correo_limpio  # Almacena el correo validado

    @property
    def telefono(self):
        """Getter del teléfono del cliente."""
        return self.__telefono  # Retorna el teléfono privado

    @telefono.setter
    def telefono(self, valor):
        """Setter del teléfono con validación numérica y de longitud."""
        if valor is None or str(valor).strip() == "":  # Verifica si el dato viene vacío
            raise ParametroFaltanteError("telefono")  # Lanza excepción FJ-004
        telefono_limpio = str(valor).strip()  # Convierte a texto y limpia espacios
        if not telefono_limpio.isdigit() or not (7 <= len(telefono_limpio) <= 15):  # Verifica solo dígitos y longitud válida
            raise ClienteInvalidoError(f"El teléfono '{valor}' debe contener entre 7 y 15 dígitos numéricos.")  # Lanza FJ-001
        self.__telefono = telefono_limpio  # Almacena el teléfono validado

    def validar_datos(self):
        """Implementación del método abstracto para confirmar que todos los datos estén completos."""
        if not all([self.id_entidad, self.__nombre, self.__correo, self.__telefono]):  # Comprueba que ningún campo sea None
            raise ClienteInvalidoError("El cliente tiene atributos incompletos tras su inicialización.")  # Lanza FJ-001
        return True  # Confirma que la validación fue exitosa

    def obtener_resumen(self):
        """Implementación del método abstracto que devuelve los datos principales del cliente."""
        return f"Cliente: {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"  # Cadena descriptiva


class GestorClientes:
    """Administra la lista interna de clientes en memoria sin utilizar bases de datos."""

    def __init__(self):
        self.__clientes = []  # Lista interna encapsulada para almacenar los objetos Cliente

    @property
    def clientes(self):
        """Retorna una copia de la lista de clientes registrados."""
        return list(self.__clientes)  # Evita modificaciones externas directas sobre la lista privada

    def registrar_cliente(self, id_cliente, nombre, correo, telefono):
        """Crea y registra un nuevo cliente manejando excepciones y registrando en el log."""
        nuevo_cliente = None  # Variable auxiliar para almacenar el cliente si se crea con éxito
        try:
            # Verifica que no exista ya un cliente con el mismo ID en la lista interna
            if any(c.id_entidad == str(id_cliente).strip() for c in self.__clientes):
                raise OperacionNoPermitidaError(f"Ya existe un cliente registrado con el ID '{id_cliente}'.")  # Lanza FJ-006

            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)  # Intenta instanciar el objeto Cliente
        except (ParametroFaltanteError, ClienteInvalidoError, OperacionNoPermitidaError) as e:
            registrar_error(e)  # Guarda el error en software_fj.log usando logger.py
            raise  # Relanza la excepción para que main.py sepa que la operación falló de forma controlada
        except Exception as e:
            # Encadenamiento de excepciones ante cualquier fallo inesperado del sistema
            error_encadenado = ClienteInvalidoError(f"Error inesperado al registrar cliente: {e}")
            registrar_error(error_encadenado)  # Registra el error encadenado en el log
            raise error_encadenado from e  # Mantiene la traza original del error
        else:
            # Bloque else: se ejecuta únicamente si no ocurrió ninguna excepción en el try
            self.__clientes.append(nuevo_cliente)  # Agrega el cliente válido a la lista en memoria
            registrar_info(f"Cliente registrado exitosamente: {nuevo_cliente}")  # Registra evento en el log
            return nuevo_cliente  # Retorna el objeto creado
        finally:
            # Bloque finally: siempre se ejecuta para garantizar trazabilidad de la operación
            registrar_info(f"Intento de registro de cliente '{id_cliente}' finalizado.")

    def buscar_cliente(self, id_cliente):
        """Busca un cliente por su identificador dentro de la lista en memoria."""
        if not id_cliente or str(id_cliente).strip() == "":  # Valida que se envíe un ID para buscar
            error = ParametroFaltanteError("id_cliente")  # Prepara excepción FJ-004
            registrar_error(error)  # Registra el fallo en el log
            raise error  # Lanza la excepción

        for cliente in self.__clientes:  # Recorre la lista interna de clientes
            if cliente.id_entidad == str(id_cliente).strip():  # Compara el identificador
                return cliente  # Retorna el objeto Cliente encontrado

        # Si termina el ciclo sin encontrarlo, lanza excepción personalizada y la registra
        error_no_encontrado = ClienteInvalidoError(f"No se encontró ningún cliente con el ID '{id_cliente}'.")
        registrar_error(error_no_encontrado)  # Guarda el error en software_fj.log
        raise error_no_encontrado  # Lanza FJ-001


# Prueba rápida: solo se ejecuta al correr este archivo directamente
if __name__ == "__main__":
    gestor = GestorClientes()  # Crea el gestor en memoria

    # Prueba 1: Registro válido
    try:
        c1 = gestor.registrar_cliente("CLI-01", "Laura Gómez", "laura@correo.com", "3001234567")
        print("Registro exitoso:", c1)
    except Exception as err:
        print("Fallo inesperado:", err)

    # Prueba 2: Registro inválido (correo sin @) para verificar captura y log
    try:
        gestor.registrar_cliente("CLI-02", "Carlos Ruiz", "carlos_sin_arroba.com", "3109876543")
    except ClienteInvalidoError as err:
        print("Excepción capturada correctamente:", err)

    # Prueba 3: Parámetro faltante (nombre vacío)
    try:
        gestor.registrar_cliente("CLI-03", "", "ana@correo.com", "3205554433")
    except ParametroFaltanteError as err:
        print("Excepción capturada correctamente:", err)
