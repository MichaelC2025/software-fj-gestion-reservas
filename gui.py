"""
gui.py
Interfaz gráfica opcional con Tkinter para el sistema Software FJ.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from cliente import GestorClientes
from servicios import GestorServicios, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import GestorReservas
from excepciones import ErrorSistemaFJ

class AppSoftwareFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión Integral de Clientes y Reservas")
        self.root.geometry("800x600")

        # Instancias de los gestores en memoria
        self.gestor_clientes = GestorClientes()
        self.gestor_servicios = GestorServicios()
        self.gestor_reservas = GestorReservas()

        # Crear componentes visuales (Pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.crear_pestana_clientes()
        self.crear_pestana_servicios()
        self.crear_pestana_reservas()

    def crear_pestana_clientes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clientes")

        # Ejemplo de etiqueta y campo de texto para registrar cliente
        ttk.Label(frame, text="Registro de Clientes", font=("Arial", 14, "bold")).pack(pady=10)

        # Contenedor para el formulario de entrada de datos
        form_frame = ttk.LabelFrame(frame, text="Datos del Cliente")
        form_frame.pack(fill="x", padx=20, pady=10)

        # Campos de entrada
        ttk.Label(form_frame, text="ID Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id_cliente = ttk.Entry(form_frame)
        self.entry_id_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = ttk.Entry(form_frame)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Correo:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_correo = ttk.Entry(form_frame)
        self.entry_correo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_telefono = ttk.Entry(form_frame)
        self.entry_telefono.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Botón para registrar (vinculado a la lógica de excepciones)
        btn_registrar = ttk.Button(form_frame, text="Registrar Cliente", command=self.accion_registrar_cliente)
        btn_registrar.grid(row=4, column=0, columnspan=2, pady=10)

        # Tabla (Treeview) para visualizar los clientes registrados en memoria
        tabla_frame = ttk.LabelFrame(frame, text="Clientes Registrados")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree_clientes = ttk.Treeview(tabla_frame, columns=("ID", "Nombre", "Correo", "Teléfono"), show="headings")
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Correo", text="Correo")
        self.tree_clientes.heading("Teléfono", text="Teléfono")
        self.tree_clientes.pack(fill="both", expand=True, padx=5, pady=5)

    def accion_registrar_cliente(self):
        """Método de ejemplo para capturar los datos y manejar excepciones visualmente."""
        try:
            # Captura los valores de los campos de texto
            id_c = self.entry_id_cliente.get()
            nombre = self.entry_nombre.get()
            correo = self.entry_correo.get()
            telefono = self.entry_telefono.get()

            # Intenta registrar usando tu gestor (lanza excepciones personalizadas si falla)
            self.gestor_clientes.registrar_cliente(id_c, nombre, correo, telefono)
            
            # Actualiza la tabla visual
            self.tree_clientes.insert("", "end", values=(id_c, nombre, correo, telefono))
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            
        except ErrorSistemaFJ as e:
            # Captura errores personalizados (como FJ-001 o FJ-004) y muestra alerta
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")

    def crear_pestana_servicios(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Servicios")

        ttk.Label(frame, text="Gestión de Catálogo de Servicios", font=("Arial", 14, "bold")).pack(pady=10)

        form_frame = ttk.LabelFrame(frame, text="Nuevo Servicio")
        form_frame.pack(fill="x", padx=20, pady=10)

        # Campos comunes
        ttk.Label(form_frame, text="ID Servicio:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id_serv = ttk.Entry(form_frame)
        self.entry_id_serv.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nom_serv = ttk.Entry(form_frame)
        self.entry_nom_serv.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Tarifa Base ($):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_tarifa = ttk.Entry(form_frame)
        self.entry_tarifa.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Tipo de Servicio:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.combo_tipo_serv = ttk.Combobox(form_frame, values=["Sala", "Equipo", "Asesoria"], state="readonly")
        self.combo_tipo_serv.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.combo_tipo_serv.current(0)

        # Campo adicional variable (ej. Capacidad / Stock / Nivel)
        ttk.Label(form_frame, text="Dato Extra (Cap/Stock/Nivel):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_extra = ttk.Entry(form_frame)
        self.entry_extra.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        btn_reg_serv = ttk.Button(form_frame, text="Registrar Servicio", command=self.accion_registrar_servicio)
        btn_reg_serv.grid(row=5, column=0, columnspan=2, pady=10)

        # Tabla de servicios
        tabla_frame = ttk.LabelFrame(frame, text="Servicios Disponibles")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree_servicios = ttk.Treeview(tabla_frame, columns=("ID", "Nombre", "Tarifa", "Detalle"), show="headings")
        self.tree_servicios.heading("ID", text="ID")
        self.tree_servicios.heading("Nombre", text="Nombre")
        self.tree_servicios.heading("Tarifa", text="Tarifa Base")
        self.tree_servicios.heading("Detalle", text="Detalle Específico")
        self.tree_servicios.pack(fill="both", expand=True, padx=5, pady=5)

    def accion_registrar_servicio(self):
        try:
            id_s = self.entry_id_serv.get()
            nombre = self.entry_nom_serv.get()
            tarifa = self.entry_tarifa.get()
            tipo = self.combo_tipo_serv.get()
            extra = self.entry_extra.get()

            # Polimorfismo según el tipo de servicio seleccionado
            if tipo == "Sala":
                servicio = ReservaSala(id_s, nombre, tarifa, capacidad_personas=int(extra))
            elif tipo == "Equipo":
                servicio = AlquilerEquipo(id_s, nombre, tarifa, tipo_equipo="Tecnológico", cantidad_disponible=int(extra))
            else:
                servicio = AsesoriaEspecializada(id_s, nombre, tarifa, especialidad="Sistemas", nivel_consultor=extra if extra else "Senior")

            self.gestor_servicios.registrar_servicio(servicio)
            self.tree_servicios.insert("", "end", values=(id_s, nombre, f"${float(tarifa):,.2f}", servicio.describir_servicio()))
            messagebox.showinfo("Éxito", "Servicio registrado correctamente.")
        except ErrorSistemaFJ as e:
            messagebox.showerror("Error de Validación (Servicio)", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")

    def crear_pestana_reservas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Reservas")

        ttk.Label(frame, text="Gestión de Reservas y Ciclo de Vida", font=("Arial", 14, "bold")).pack(pady=10)

        form_frame = ttk.LabelFrame(frame, text="Crear Nueva Reserva")
        form_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(form_frame, text="ID Reserva:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id_res = ttk.Entry(form_frame)
        self.entry_id_res.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="ID Cliente Existente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_res_cliente = ttk.Entry(form_frame)
        self.entry_res_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="ID Servicio Existente:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_res_servicio = ttk.Entry(form_frame)
        self.entry_res_servicio.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Duración (horas):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_duracion = ttk.Entry(form_frame)
        self.entry_duracion.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        btn_reg_res = ttk.Button(form_frame, text="Crear Reserva (PENDIENTE)", command=self.accion_crear_reserva)
        btn_reg_res.grid(row=4, column=0, columnspan=2, pady=10)

        # Botones de cambio de estado rápido
        acciones_frame = ttk.LabelFrame(frame, text="Acciones sobre Reserva Seleccionada")
        acciones_frame.pack(fill="x", padx=20, pady=5)

        ttk.Button(acciones_frame, text="Confirmar", command=lambda: self.accion_cambiar_estado("confirmar")).pack(side="left", padx=10, pady=5)
        ttk.Button(acciones_frame, text="Procesar", command=lambda: self.accion_cambiar_estado("procesar")).pack(side="left", padx=10, pady=5)
        ttk.Button(acciones_frame, text="Cancelar", command=lambda: self.accion_cambiar_estado("cancelar")).pack(side="left", padx=10, pady=5)

        # Tabla de reservas
        tabla_frame = ttk.LabelFrame(frame, text="Listado de Reservas")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree_reservas = ttk.Treeview(tabla_frame, columns=("ID", "Cliente", "Servicio", "Total", "Estado"), show="headings")
        self.tree_reservas.heading("ID", text="ID")
        self.tree_reservas.heading("Cliente", text="Cliente")
        self.tree_reservas.heading("Servicio", text="Servicio")
        self.tree_reservas.heading("Total", text="Costo Total")
        self.tree_reservas.heading("Estado", text="Estado")
        self.tree_reservas.pack(fill="both", expand=True, padx=5, pady=5)

    def accion_crear_reserva(self):
        try:
            id_r = self.entry_id_res.get()
            id_c = self.entry_res_cliente.get()
            id_s = self.entry_res_servicio.get()
            duracion = self.entry_duracion.get()

            # Busca los objetos reales en los gestores en memoria
            cliente_obj = self.gestor_clientes.buscar_cliente(id_c)
            servicio_obj = self.gestor_servicios.buscar_servicio(id_s)

            reserva = self.gestor_reservas.crear_reserva(id_r, cliente_obj, servicio_obj, duracion)
            
            self.tree_reservas.insert("", "end", iid=id_r, values=(id_r, cliente_obj.nombre, servicio_obj.nombre, f"${reserva.costo_total:,.2f}", reserva.estado))
            messagebox.showinfo("Éxito", f"Reserva creada con éxito. Total: ${reserva.costo_total:,.2f}")
        except ErrorSistemaFJ as e:
            messagebox.showerror("Error de Reserva", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la reserva: {e}")

    def accion_cambiar_estado(self, accion):
        try:
            seleccion = self.tree_reservas.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona una reserva de la tabla.")
                return
            id_r = seleccion[0]
            
            # Ejecuta la acción y captura excepciones personalizadas (como FJ-006 si ya está procesada)
            reserva_actualizada = self.gestor_reservas.ejecutar_accion(id_r, accion)
            
            # Actualiza el estado visual en la tabla
            self.tree_reservas.item(id_r, values=(
                id_r, 
                reserva_actualizada.cliente.nombre, 
                reserva_actualizada.servicio.nombre, 
                f"${reserva_actualizada.costo_total:,.2f}", 
                reserva_actualizada.estado
            ))
            messagebox.showinfo("Actualizado", f"La reserva pasó a estado: {reserva_actualizada.estado}")
        except ErrorSistemaFJ as e:
            messagebox.showerror("Operación No Permitida", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()