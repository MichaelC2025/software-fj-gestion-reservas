# software-fj-gestion-reservas
Sistema de gestión de clientes, servicios y reservas — Programación 213023_348

Sistema orientado a objetos para la empresa **Software FJ**, que gestiona clientes, servicios
(reserva de salas, alquiler de equipos y asesorías especializadas) y reservas **sin base de datos**:
toda la información vive en objetos y listas en memoria, y solo se usa un archivo para el
registro de eventos y errores (`software_fj.log`).

## Ejecución

Requiere Python 3.9 o superior (solo librería estándar).

```bash
python main.py   # Simulación de 18 operaciones válidas e inválidas (consola)
python gui.py    # Interfaz gráfica opcional (Tkinter)
```

Al terminar, revise `software_fj.log` (se crea en la carpeta del proyecto).

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`ErrorSistemaFJ` y derivadas FJ-001 a FJ-006). |
| `logger.py` | Registro de eventos (INFO) y errores (ERROR) en `software_fj.log`, incluida la causa de las excepciones encadenadas. |
| `entidad.py` | `EntidadSistema`: clase abstracta base de todas las entidades (ID, fecha de creación, `validar_datos()` y `obtener_resumen()` abstractos). |
| `cliente.py` | `Cliente` (datos personales encapsulados y validados con propiedades) y `GestorClientes` (lista interna). |
| `servicios.py` | `Servicio` abstracto; `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`; `GestorServicios` con fábrica `crear_servicio()`. |
| `reserva.py` | `Reserva` (cliente + servicio + duración + estado; confirmar, cancelar, procesar) y `GestorReservas`. |
| `main.py` | Simulación integral de operaciones. |
| `gui.py` | Interfaz gráfica Tkinter que usa los mismos gestores. |

## Cumplimiento de requisitos

| Requisito | Dónde |
|---|---|
| Clase abstracta de entidades generales | `entidad.EntidadSistema` (ABC) |
| Cliente con validaciones y encapsulación | `cliente.Cliente`: atributos privados (`__nombre`, `__correo`, `__telefono`) con getters/setters validados |
| Servicio abstracto + 3 especializados | `servicios.Servicio` → `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| Polimorfismo / métodos sobrescritos | `calcular_costo()`, `describir_servicio()`, `validar_datos()` en cada servicio |
| Reserva con confirmación, cancelación y procesamiento | `reserva.Reserva.confirmar() / cancelar() / procesar()` con máquina de estados PENDIENTE → CONFIRMADA → PROCESADA / CANCELADA |
| Métodos sobrecargados | `Servicio.cotizar()` con 4 variantes declaradas con `typing.overload` (solo duración; con impuesto; con impuesto y descuento; exento de impuesto) y `calcular_costo()` con parámetros opcionales |
| Excepciones personalizadas | `excepciones.py` (FJ-001 a FJ-006) |
| `try/except`, `try/except/else`, `try/except/finally` | Gestores (`registrar_cliente`, `crear_servicio`, `registrar_servicio`, `crear_reserva`, `ejecutar_accion`) y `main.ejecutar_paso_simulado` |
| Encadenamiento de excepciones | `raise ... from e` en setters numéricos, fábrica de servicios y gestores; la causa queda en el log |
| Archivo de logs | `logger.py` → `software_fj.log` |
| Listas internas, sin base de datos | `GestorClientes`, `GestorServicios`, `GestorReservas` |
| ≥ 10 operaciones simuladas | `main.py`: 18 operaciones (8 exitosas, 10 fallidas de forma controlada) |

## Códigos de error

| Código | Excepción | Caso |
|---|---|---|
| FJ-001 | `ClienteInvalidoError` | Datos de cliente inválidos (correo, teléfono, nombre) |
| FJ-002 | `ServicioNoDisponibleError` | Servicio inexistente, deshabilitado o sin stock; datos de servicio inválidos |
| FJ-003 | `ReservaInvalidaError` | Reserva con datos inválidos (duración, cliente o servicio incorrecto) |
| FJ-004 | `ParametroFaltanteError` | Parámetro obligatorio faltante |
| FJ-005 | `CalculoCostoError` | Tarifa, impuesto, descuento o duración inconsistentes |
| FJ-006 | `OperacionNoPermitidaError` | IDs duplicados, transiciones de estado no permitidas |
