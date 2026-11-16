"""
main.py
Punto de entrada principal y simulación de operaciones del sistema Software FJ.
Integra gestión de clientes, servicios y reservas en memoria con manejo avanzado de excepciones.
Autor: [Nombre del Integrante / Equipo]
"""

from cliente import GestorClientes  # Importa el gestor en memoria de clientes
from servicios import (  # Importa los servicios especializados y su gestor
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    GestorServicios,
)
from reserva import GestorReservas  # Importa el gestor del ciclo de vida de reservas
from excepciones import ErrorSistemaFJ  # Importa la excepción base para captura polimórfica
from logger import registrar_info, registrar_error, ARCHIVO_LOG  # Funciones y ruta del log


def ejecutar_paso_simulado(numero_op, descripcion, funcion_operacion):
    """Ejecuta una operación controlada usando try/except/else/finally sin interrumpir el sistema."""
    print(f"\n--- Operación #{numero_op}: {descripcion} ---")  # Muestra cabecera de la operación
    try:
        resultado = funcion_operacion()  # Ejecuta la acción pasada como función lambda
    except ErrorSistemaFJ as e:
        # Captura cualquier excepción personalizada del sistema (FJ-001 a FJ-006)
        print(f"[ERROR CONTROLADO] {e} -> El sistema continúa operando.")
    except Exception as e:
        # Captura cualquier error imprevisto de Python para evitar cierre abrupto
        registrar_error(f"Error crítico no esperado en Op #{numero_op}: {e}")
        print(f"[ERROR INESPERADO] {e} -> El sistema continúa operando.")
    else:
        # Se ejecuta únicamente si la operación finalizó sin excepciones
        print(f"[ÉXITO] {resultado}")  # Muestra el resumen del objeto o acción completada
    finally:
        # Se ejecuta siempre para cerrar visualmente la transacción
        print(f"Fin de validación Op #{numero_op}.")


def ejecutar_simulacion_integral():
    """Simula 12 operaciones completas (válidas e inválidas) en Software FJ sin base de datos."""
    print("=" * 75)
    print("INICIANDO SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ (SIN BASE DE DATOS)")
    print("=" * 75)
    registrar_info("=== INICIO DE SIMULACIÓN INTEGRAL SOFTWARE FJ ===")

    # Instancia los tres gestores que mantienen las listas internas en memoria
    gestor_clientes = GestorClientes()
    gestor_servicios = GestorServicios()
    gestor_reservas = GestorReservas()

    # -------------------------------------------------------------------------
    # BLOQUE 1: GESTIÓN DE CLIENTES (OPERACIONES 1 A 3)
    # -------------------------------------------------------------------------
    # Op 1 (Válida): Registro de cliente corporativo
    ejecutar_paso_simulado(
        1,
        "Registro válido de cliente (Ana María Gómez)",
        lambda: gestor_clientes.registrar_cliente("CLI-01", "Ana María Gómez", "ana.gomez@empresa.com", "3104567890"),
    )

    # Op 2 (Válida): Registro de segundo cliente
    ejecutar_paso_simulado(
        2,
        "Registro válido de cliente (Carlos Andrés Ruiz)",
        lambda: gestor_clientes.registrar_cliente("CLI-02", "Carlos Andrés Ruiz", "cruiz@techcol.co", "3209876543"),
    )

    # Op 3 (Inválida): Correo sin '@' y teléfono muy corto -> dispara ClienteInvalidoError [FJ-001]
    ejecutar_paso_simulado(
        3,
        "Registro inválido de cliente (correo mal formado)",
        lambda: gestor_clientes.registrar_cliente("CLI-03", "Luis Pérez", "luisperez_sin_arroba.com", "123"),
    )

    # -------------------------------------------------------------------------
    # BLOQUE 2: CATÁLOGO DE SERVICIOS ESPECIALIZADOS (OPERACIONES 4 A 7)
    # -------------------------------------------------------------------------
    # Op 4 (Válida): Creación de servicio tipo ReservaSala
    ejecutar_paso_simulado(
        4,
        "Creación válida de servicio: Sala de Juntas Ejecutiva",
        lambda: gestor_servicios.registrar_servicio(
            ReservaSala("SRV-01", "Sala Innovación Norte", 80000, capacidad_personas=12, tiene_proyector=True)
        ),
    )

    # Op 5 (Válida): Creación de servicio tipo AlquilerEquipo
    ejecutar_paso_simulado(
        5,
        "Creación válida de servicio: Alquiler Workstation Dell",
        lambda: gestor_servicios.registrar_servicio(
            AlquilerEquipo("SRV-02", "Workstation Precision 5570", 45000, tipo_equipo="Portátil", cantidad_disponible=2)
        ),
    )

    # Op 6 (Válida): Creación de servicio tipo AsesoriaEspecializada
    ejecutar_paso_simulado(
        6,
        "Creación válida de servicio: Asesoría en Arquitectura Cloud",
        lambda: gestor_servicios.registrar_servicio(
            AsesoriaEspecializada("SRV-03", "Consultoría Cloud AWS", 120000, especialidad="Cloud", nivel_consultor="Senior")
        ),
    )

    # Op 7 (Inválida): Tarifa base negativa -> dispara CalculoCostoError [FJ-005]
    ejecutar_paso_simulado(
        7,
        "Creación inválida de servicio (tarifa negativa)",
        lambda: gestor_servicios.registrar_servicio(
            ReservaSala("SRV-99", "Sala Defectuosa", -50000, capacidad_personas=5)
        ),
    )

    # -------------------------------------------------------------------------
    # BLOQUE 3: RESERVAS, POLIMORFISMO Y CICLO DE ESTADOS (OPERACIONES 8 A 12)
    # -------------------------------------------------------------------------
    # Recupera referencias válidas desde las listas en memoria para operar sobre ellas
    cliente_1 = gestor_clientes.buscar_cliente("CLI-01")
    cliente_2 = gestor_clientes.buscar_cliente("CLI-02")
    sala_1 = gestor_servicios.buscar_servicio("SRV-01")
    equipo_1 = gestor_servicios.buscar_servicio("SRV-02")
    asesoria_1 = gestor_servicios.buscar_servicio("SRV-03")

    # Op 8 (Válida): Reserva de sala por 6 horas (aplica descuento automático del 10 %) + confirmación + procesamiento
    def flujo_reserva_completa():
        res = gestor_reservas.crear_reserva("RES-01", cliente_1, sala_1, duracion=6, impuesto=0.19)
        gestor_reservas.ejecutar_accion("RES-01", "confirmar")  # Pasa a CONFIRMADA
        gestor_reservas.ejecutar_accion("RES-01", "procesar")   # Pasa a PROCESADA
        return res

    ejecutar_paso_simulado(
        8,
        "Reserva válida de sala (6h con descuento automático), confirmación y procesamiento",
        flujo_reserva_completa,
    )

    # Op 9 (Válida): Reserva de equipo, confirmación (descuenta stock) y cancelación (restaura stock)
    def flujo_reserva_y_cancelacion():
        res = gestor_reservas.crear_reserva("RES-02", cliente_2, equipo_1, duracion=4, impuesto=0.19, descuento=0.05)
        gestor_reservas.ejecutar_accion("RES-02", "confirmar")  # Stock baja de 2 a 1
        gestor_reservas.ejecutar_accion("RES-02", "cancelar")   # Stock vuelve a 2
        return res

    ejecutar_paso_simulado(
        9,
        "Reserva válida de equipo con descuento del 5 %, confirmación y posterior cancelación",
        flujo_reserva_y_cancelacion,
    )

    # Op 10 (Inválida): Intento de reserva con duración negativa -> dispara ReservaInvalidaError [FJ-003]
    ejecutar_paso_simulado(
        10,
        "Intento de reserva inválido (duración <= 0)",
        lambda: gestor_reservas.crear_reserva("RES-03", cliente_1, asesoria_1, duracion=-2),
    )

    # Op 11 (Inválida): Intento de reserva sobre un servicio marcado como no disponible -> ServicioNoDisponibleError [FJ-002]
    def flujo_servicio_inactivo():
        asesoria_1.disponible = False  # Deshabilita temporalmente el servicio
        return gestor_reservas.crear_reserva("RES-04", cliente_2, asesoria_1, duracion=3)

    ejecutar_paso_simulado(
        11,
        "Intento de reserva inválido (servicio no disponible)",
        flujo_servicio_inactivo,
    )

    # Op 12 (Inválida): Intento de cancelar una reserva ya PROCESADA -> OperacionNoPermitidaError [FJ-006]
    ejecutar_paso_simulado(
        12,
        "Operación no permitida (cancelar la reserva RES-01 que ya fue PROCESADA)",
        lambda: gestor_reservas.ejecutar_accion("RES-01", "cancelar"),
    )

    # -------------------------------------------------------------------------
    # RESUMEN FINAL EN MEMORIA Y TRAZABILIDAD DEL LOG
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("RESUMEN FINAL DEL ESTADO EN MEMORIA (SOFTWARE FJ)")
    print("=" * 75)
    print(f"Total Clientes válidos registrados : {len(gestor_clientes.clientes)}")
    for c in gestor_clientes.clientes:
        print(f"  - {c}")

    print(f"\nTotal Servicios válidos en catálogo : {len(gestor_servicios.servicios)}")
    for s in gestor_servicios.servicios:
        print(f"  - {s}")

    print(f"\nTotal Reservas registradas en memoria: {len(gestor_reservas.reservas)}")
    for r in gestor_reservas.reservas:
        print(f"  - {r}")

    registrar_info("=== FIN DE SIMULACIÓN INTEGRAL SOFTWARE FJ ===")
    print(f"\nTodos los eventos y errores quedaron auditados en: '{ARCHIVO_LOG}'")


# Punto de entrada estándar de Python
if __name__ == "__main__":
    ejecutar_simulacion_integral()