"""
main.py
Punto de entrada principal y simulación de operaciones del sistema Software FJ.
Integra gestión de clientes, servicios y reservas en memoria con manejo avanzado de excepciones.
Autor: Grupo 213023_348
"""

from cliente import GestorClientes  # Importa el gestor en memoria de clientes
from servicios import GestorServicios  # Gestor y fábrica de servicios especializados
from reserva import GestorReservas  # Importa el gestor del ciclo de vida de reservas
from excepciones import ErrorSistemaFJ  # Importa la excepción base para captura polimórfica
from logger import registrar_info, registrar_error, ARCHIVO_LOG  # Funciones y ruta del log


def ejecutar_paso_simulado(numero_op, descripcion, funcion_operacion):
    """Ejecuta una operación controlada usando try/except/else/finally sin interrumpir el sistema."""
    print(f"\n--- Operación #{numero_op}: {descripcion} ---")  # Muestra cabecera de la operación
    exito = False  # Indica si la operación terminó correctamente
    try:
        resultado = funcion_operacion()  # Ejecuta la acción pasada como función
    except ErrorSistemaFJ as e:
        # Captura cualquier excepción personalizada del sistema (FJ-001 a FJ-006).
        # Los gestores ya la registraron en el log, aquí solo se informa al usuario.
        print(f"[ERROR CONTROLADO] {e} -> El sistema continúa operando.")
        if e.__cause__ is not None:  # Muestra la causa si hubo encadenamiento de excepciones
            print(f"    Causa original: {type(e.__cause__).__name__}: {e.__cause__}")
    except Exception as e:
        # Captura cualquier error imprevisto de Python para evitar cierre abrupto
        registrar_error(f"Error crítico no esperado en Op #{numero_op}: {type(e).__name__}: {e}")
        print(f"[ERROR INESPERADO] {e} -> El sistema continúa operando.")
    else:
        # Se ejecuta únicamente si la operación finalizó sin excepciones
        exito = True
        print(f"[ÉXITO] {resultado}")  # Muestra el resumen del objeto o acción completada
    finally:
        # Se ejecuta siempre para cerrar la transacción y dejar trazabilidad en el log
        registrar_info(f"Op #{numero_op} '{descripcion}' -> {'ÉXITO' if exito else 'FALLIDA'}")
        print(f"Fin de validación Op #{numero_op}.")
    return exito


def obtener_seguro(funcion_busqueda):
    """Busca un objeto en memoria; si no existe retorna None en lugar de detener el programa."""
    try:
        return funcion_busqueda()
    except ErrorSistemaFJ as e:  # El gestor ya registró el error en el log
        print(f"[AVISO] {e}")
        return None


def ejecutar_simulacion_integral():
    """Simula 18 operaciones completas (válidas e inválidas) en Software FJ sin base de datos."""
    print("=" * 75)
    print("INICIANDO SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ (SIN BASE DE DATOS)")
    print("=" * 75)
    registrar_info("=== INICIO DE SIMULACIÓN INTEGRAL SOFTWARE FJ ===")

    # Instancia los tres gestores que mantienen las listas internas en memoria
    gestor_clientes = GestorClientes()
    gestor_servicios = GestorServicios()
    gestor_reservas = GestorReservas()
    resultados = []  # Guarda True/False por operación para el resumen final

    # -------------------------------------------------------------------------
    # BLOQUE 1: GESTIÓN DE CLIENTES (OPERACIONES 1 A 4)
    # -------------------------------------------------------------------------
    # Op 1 (Válida): Registro de cliente corporativo
    resultados.append(ejecutar_paso_simulado(
        1,
        "Registro válido de cliente (Ana María Gómez)",
        lambda: gestor_clientes.registrar_cliente("CLI-01", "Ana María Gómez", "ana.gomez@empresa.com", "3104567890"),
    ))

    # Op 2 (Válida): Registro de segundo cliente
    resultados.append(ejecutar_paso_simulado(
        2,
        "Registro válido de cliente (Carlos Andrés Ruiz)",
        lambda: gestor_clientes.registrar_cliente("CLI-02", "Carlos Andrés Ruiz", "cruiz@techcol.co", "3209876543"),
    ))

    # Op 3 (Inválida): Correo sin '@' -> dispara ClienteInvalidoError [FJ-001]
    resultados.append(ejecutar_paso_simulado(
        3,
        "Registro inválido de cliente (correo mal formado)",
        lambda: gestor_clientes.registrar_cliente("CLI-03", "Luis Pérez", "luisperez_sin_arroba.com", "3001112233"),
    ))

    # Op 4 (Inválida): Nombre vacío -> dispara ParametroFaltanteError [FJ-004]
    resultados.append(ejecutar_paso_simulado(
        4,
        "Registro inválido de cliente (parámetro obligatorio 'nombre' faltante)",
        lambda: gestor_clientes.registrar_cliente("CLI-04", "   ", "sofia@correo.com", "3005556677"),
    ))

    # Op 5 (Inválida): ID duplicado -> dispara OperacionNoPermitidaError [FJ-006]
    resultados.append(ejecutar_paso_simulado(
        5,
        "Registro inválido de cliente (ID 'CLI-01' duplicado)",
        lambda: gestor_clientes.registrar_cliente("CLI-01", "Pedro Rojas", "projas@correo.com", "3014445566"),
    ))

    # -------------------------------------------------------------------------
    # BLOQUE 2: CATÁLOGO DE SERVICIOS ESPECIALIZADOS (OPERACIONES 6 A 10)
    # -------------------------------------------------------------------------
    # Op 6 (Válida): Creación de servicio tipo ReservaSala
    resultados.append(ejecutar_paso_simulado(
        6,
        "Creación válida de servicio: Sala de Juntas con proyector",
        lambda: gestor_servicios.crear_servicio(
            "sala", id_servicio="SRV-01", nombre="Sala Innovación Norte", tarifa_base=80000,
            capacidad_personas=12, tiene_proyector=True,
        ),
    ))

    # Op 7 (Válida): Creación de servicio tipo AlquilerEquipo (solo 1 unidad en stock)
    resultados.append(ejecutar_paso_simulado(
        7,
        "Creación válida de servicio: Alquiler Workstation Dell (stock 1)",
        lambda: gestor_servicios.crear_servicio(
            "equipo", id_servicio="SRV-02", nombre="Workstation Precision 5570", tarifa_base=45000,
            tipo_equipo="Portátil", cantidad_disponible=1,
        ),
    ))

    # Op 8 (Válida): Creación de servicio tipo AsesoriaEspecializada
    resultados.append(ejecutar_paso_simulado(
        8,
        "Creación válida de servicio: Asesoría en Arquitectura Cloud",
        lambda: gestor_servicios.crear_servicio(
            "asesoria", id_servicio="SRV-03", nombre="Consultoría Cloud AWS", tarifa_base=120000,
            especialidad="Cloud", nivel_consultor="Senior",
        ),
    ))

    # Op 9 (Inválida): Tarifa base negativa -> dispara CalculoCostoError [FJ-005]
    resultados.append(ejecutar_paso_simulado(
        9,
        "Creación inválida de servicio (tarifa negativa)",
        lambda: gestor_servicios.crear_servicio(
            "sala", id_servicio="SRV-98", nombre="Sala Defectuosa", tarifa_base=-50000, capacidad_personas=5,
        ),
    ))

    # Op 10 (Inválida): Tarifa no numérica -> ValueError encadenado en CalculoCostoError [FJ-005]
    resultados.append(ejecutar_paso_simulado(
        10,
        "Creación inválida de servicio (tarifa 'cien mil' no numérica, excepción encadenada)",
        lambda: gestor_servicios.crear_servicio(
            "asesoria", id_servicio="SRV-99", nombre="Asesoría Legal", tarifa_base="cien mil",
            especialidad="Legal",
        ),
    ))

    # -------------------------------------------------------------------------
    # BLOQUE 3: RESERVAS, POLIMORFISMO, SOBRECARGA Y CICLO DE ESTADOS (OP. 11 A 17)
    # -------------------------------------------------------------------------
    # Recupera referencias desde las listas en memoria sin detener el programa si alguna falta
    cliente_1 = obtener_seguro(lambda: gestor_clientes.buscar_cliente("CLI-01"))
    cliente_2 = obtener_seguro(lambda: gestor_clientes.buscar_cliente("CLI-02"))
    sala_1 = obtener_seguro(lambda: gestor_servicios.buscar_servicio("SRV-01"))
    equipo_1 = obtener_seguro(lambda: gestor_servicios.buscar_servicio("SRV-02"))
    asesoria_1 = obtener_seguro(lambda: gestor_servicios.buscar_servicio("SRV-03"))

    # Op 11 (Válida): Polimorfismo + método sobrecargado cotizar() con sus cuatro variantes
    def flujo_cotizaciones():
        lineas = []
        for servicio in gestor_servicios.servicios:  # Mismo mensaje, distinto comportamiento (polimorfismo)
            lineas.append(
                f"\n    {servicio.describir_servicio()}"
                f"\n      cotizar(2)                 = ${servicio.cotizar(2):,.2f}"
                f"\n      cotizar(2, 0.05)           = ${servicio.cotizar(2, 0.05):,.2f}"
                f"\n      cotizar(2, 0.19, 0.10)     = ${servicio.cotizar(2, 0.19, 0.10):,.2f}"
                f"\n      cotizar(2, sin_impuesto)   = ${servicio.cotizar(2, sin_impuesto=True):,.2f}"
            )
        return "Cotizaciones generadas:" + "".join(lineas)

    resultados.append(ejecutar_paso_simulado(
        11,
        "Cotización polimórfica con el método sobrecargado cotizar()",
        flujo_cotizaciones,
    ))

    # Op 12 (Válida): Reserva de sala por 6 horas (descuento automático del 10 %) + confirmación + procesamiento
    def flujo_reserva_completa():
        res = gestor_reservas.crear_reserva("RES-01", cliente_1, sala_1, duracion=6, impuesto=0.19)
        gestor_reservas.ejecutar_accion("RES-01", "confirmar")  # Pasa a CONFIRMADA
        gestor_reservas.ejecutar_accion("RES-01", "procesar")   # Pasa a PROCESADA
        return res

    resultados.append(ejecutar_paso_simulado(
        12,
        "Reserva válida de sala (6h con descuento automático), confirmación y procesamiento",
        flujo_reserva_completa,
    ))

    # Op 13 (Válida + Inválida): El único equipo se reserva; un segundo intento falla por stock agotado [FJ-002];
    # al cancelar la primera reserva el stock se repone y el servicio vuelve a estar disponible.
    def flujo_stock_equipo():
        gestor_reservas.crear_reserva("RES-02", cliente_2, equipo_1, duracion=4, impuesto=0.19, descuento=0.05)
        gestor_reservas.ejecutar_accion("RES-02", "confirmar")  # Stock baja de 1 a 0 -> no disponible
        try:
            gestor_reservas.crear_reserva("RES-03", cliente_1, equipo_1, duracion=2)
        except ErrorSistemaFJ as e:
            print(f"    Segundo intento rechazado como se esperaba: {e}")
        gestor_reservas.ejecutar_accion("RES-02", "cancelar")  # Stock vuelve a 1 -> disponible
        return f"{equipo_1.describir_servicio()} | Disponible: {equipo_1.disponible}"

    resultados.append(ejecutar_paso_simulado(
        13,
        "Reserva de equipo, agotamiento de stock, intento fallido y cancelación con reposición",
        flujo_stock_equipo,
    ))

    # Op 14 (Inválida): Duración negativa -> dispara ReservaInvalidaError [FJ-003]
    resultados.append(ejecutar_paso_simulado(
        14,
        "Intento de reserva inválido (duración <= 0)",
        lambda: gestor_reservas.crear_reserva("RES-04", cliente_1, asesoria_1, duracion=-2),
    ))

    # Op 15 (Inválida): Descuento de 150 % -> cálculo inconsistente, dispara CalculoCostoError [FJ-005]
    resultados.append(ejecutar_paso_simulado(
        15,
        "Intento de reserva inválido (cálculo inconsistente: descuento del 150 %)",
        lambda: gestor_reservas.crear_reserva("RES-05", cliente_2, asesoria_1, duracion=3, descuento=1.5),
    ))

    # Op 16 (Inválida): Servicio marcado como no disponible -> ServicioNoDisponibleError [FJ-002]
    def flujo_servicio_inactivo():
        asesoria_1.disponible = False  # Deshabilita temporalmente el servicio
        try:
            return gestor_reservas.crear_reserva("RES-06", cliente_2, asesoria_1, duracion=3)
        finally:
            asesoria_1.disponible = True  # Se rehabilita siempre, ocurra o no el error

    resultados.append(ejecutar_paso_simulado(
        16,
        "Intento de reserva inválido (servicio no disponible)",
        flujo_servicio_inactivo,
    ))

    # Op 17 (Inválida): Cancelar una reserva ya PROCESADA -> OperacionNoPermitidaError [FJ-006]
    resultados.append(ejecutar_paso_simulado(
        17,
        "Operación no permitida (cancelar la reserva RES-01 que ya fue PROCESADA)",
        lambda: gestor_reservas.ejecutar_accion("RES-01", "cancelar"),
    ))

    # Op 18 (Inválida): Cliente que no es un objeto Cliente -> error de tipo [FJ-003]
    resultados.append(ejecutar_paso_simulado(
        18,
        "Intento de reserva inválido (cliente no es una instancia de Cliente)",
        lambda: gestor_reservas.crear_reserva("RES-07", "CLI-02", sala_1, duracion=1),
    ))

    # -------------------------------------------------------------------------
    # RESUMEN FINAL EN MEMORIA Y TRAZABILIDAD DEL LOG
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("RESUMEN FINAL DEL ESTADO EN MEMORIA (SOFTWARE FJ)")
    print("=" * 75)
    print(f"Operaciones ejecutadas: {len(resultados)} | Exitosas: {resultados.count(True)} "
          f"| Fallidas controladas: {resultados.count(False)}")

    print(f"\nTotal Clientes válidos registrados : {len(gestor_clientes.clientes)}")
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
