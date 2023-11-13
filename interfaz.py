import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from customtkinter import *
import openpyxl
import os
from datetime import datetime


# Variables globales
productos = []
ventas = []
tipo_usuario = None
dinero_inicial_caja = 0

# Funciones para interactuar con Excel
def guardar_productos():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Nombre", "Precio de Venta", "Cantidad en Inventario"])
    for producto in productos:
        sheet.append([producto["nombre"], producto["precio"], producto["cantidad"]])
    workbook.save("productos.xlsx")

def cargar_productos():
    try:
        workbook = openpyxl.load_workbook("productos.xlsx")
        sheet = workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            productos.append({"nombre": row[0], "precio": row[1], "cantidad": row[2]})
    except FileNotFoundError:
        pass

def guardar_venta(venta):
    archivo_ventas = "ventas_totales.xlsx"
    if not os.path.exists(archivo_ventas):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Fecha", "ID Venta", "Productos", "Total Venta", "Método de Pago"])
    else:
        workbook = openpyxl.load_workbook(archivo_ventas)
        sheet = workbook.active
    sheet.append(venta)
    workbook.save(archivo_ventas)

# Inicio de Sesión
def iniciar_sesion(usuario, contrasena):
    global tipo_usuario
    if usuario == "admin" and contrasena == "adminpass":
        tipo_usuario = "admin"
    elif usuario == "empleado" and contrasena == "empleadopass":
        tipo_usuario = "empleado"
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")
        return

    # Establecer dinero inicial en caja
    global dinero_inicial_caja
    dinero_inicial_caja = float(simpledialog.askstring("Dinero Inicial", "Por favor, ingresa el efectivo inicial en caja: $"))

    # Mostrar ventana principal
    mostrar_ventana_principal()

# Ventana de Inicio de Sesión
# Inicio de Sesión
def iniciar_sesion(usuario, contrasena, ventana_login):
    global tipo_usuario
    if usuario == "admin" and contrasena == "adminpass":
        tipo_usuario = "admin"
    elif usuario == "empleado" and contrasena == "empleadopass":
        tipo_usuario = "empleado"
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")
        return

    # Establecer dinero inicial en caja
    global dinero_inicial_caja
    dinero_inicial_caja = float(simpledialog.askstring("Dinero Inicial", "Por favor, ingresa el efectivo inicial en caja: $", parent=ventana_login))

    ventana_login.destroy()  # Cierra la ventana de inicio de sesión después de establecer el dinero inicial
    mostrar_ventana_principal()

# Ventana de Inicio de Sesión
def mostrar_ventana_login():
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")

    # Establecer un estilo
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 10), padding=5)

    # Usar Frame para una mejor organización
    frame = ttk.Frame(ventana_login, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Nombre de usuario:").grid(column=0, row=0, sticky=tk.W)
    entry_usuario = ttk.Entry(frame)
    entry_usuario.grid(column=1, row=0, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Contraseña:").grid(column=0, row=1, sticky=tk.W)
    entry_contrasena = ttk.Entry(frame, show="*")
    entry_contrasena.grid(column=1, row=1, sticky=(tk.W, tk.E))

    ttk.Button(frame, text="Iniciar sesión", command=lambda: iniciar_sesion(entry_usuario.get(), entry_contrasena.get(), ventana_login)).grid(column=1, row=2, sticky=tk.E)

    # Configurar el espaciado y expansión de la cuadrícula
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    ventana_login.columnconfigure(0, weight=1)
    ventana_login.rowconfigure(0, weight=1)

    ventana_login.mainloop()


# Ventana Principal
def mostrar_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de Gestión")

    # Establecer un estilo
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=5)

    # Usar Frame para una mejor organización
    frame = ttk.Frame(ventana_principal, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    if tipo_usuario == "admin":
        ttk.Button(frame, text="Agregar Producto", command=agregar_producto).grid(column=0, row=0, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Eliminar Producto", command=eliminar_producto).grid(column=1, row=0, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Modificar Producto", command=modificar_producto).grid(column=2, row=0, sticky=(tk.W, tk.E))

    ttk.Button(frame, text="Caja de Cobro", command=lambda: caja_de_cobro(ventana_principal)).grid(column=0, row=1, sticky=(tk.W, tk.E))
    ttk.Button(frame, text="Salir", command=ventana_principal.destroy).grid(column=2, row=1, sticky=tk.E)

    # Configurar el espaciado y expansión de la cuadrícula
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    ventana_principal.mainloop()

# Función para agregar producto
def agregar_producto():
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Producto")

    frame = ttk.Frame(ventana_agregar, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Nombre del producto:").grid(column=0, row=0, sticky=tk.W)
    entry_nombre = ttk.Entry(frame)
    entry_nombre.grid(column=1, row=0, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Precio de venta:").grid(column=0, row=1, sticky=tk.W)
    entry_precio = ttk.Entry(frame)
    entry_precio.grid(column=1, row=1, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Cantidad en inventario:").grid(column=0, row=2, sticky=tk.W)
    entry_cantidad = ttk.Entry(frame)
    entry_cantidad.grid(column=1, row=2, sticky=(tk.W, tk.E))

    ttk.Button(frame, text="Agregar", command=lambda: guardar_nuevo_producto()).grid(column=1, row=3, sticky=tk.E)

    # Función interna para guardar el nuevo producto
    def guardar_nuevo_producto():
        nombre = entry_nombre.get()
        precio = float(entry_precio.get())
        cantidad = int(entry_cantidad.get())
        productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
        ventana_agregar.destroy()
        guardar_productos()

    # Configurar el espaciado y expansión de la cuadrícula
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)


# Función para eliminar producto
def actualizar_combobox_productos(event):
    busqueda = entry_buscar.get().lower()
    productos_filtrados = [producto["nombre"] for producto in productos if busqueda in producto["nombre"].lower()]
    combo_productos['values'] = productos_filtrados
    if productos_filtrados:
        combo_productos.set(productos_filtrados[0])
    else:
        combo_productos.set('')

def eliminar():
    producto_seleccionado = combo_productos.get()
    indice_a_eliminar = None
    for indice, producto in enumerate(productos):
        if producto["nombre"] == producto_seleccionado:
            indice_a_eliminar = indice
            break

    if indice_a_eliminar is not None:
        del productos[indice_a_eliminar]
        guardar_productos()
        actualizar_combobox_productos(None)
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un producto")

def eliminar_producto():
    global entry_buscar, combo_productos
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Producto")

    frame = ttk.Frame(ventana_eliminar, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Buscar Producto:").grid(column=0, row=0, sticky=tk.W)
    entry_buscar = ttk.Entry(frame)
    entry_buscar.grid(column=1, row=0, sticky=(tk.W, tk.E))
    entry_buscar.bind('<KeyRelease>', actualizar_combobox_productos)

    combo_productos = ttk.Combobox(frame)
    combo_productos.grid(column=1, row=1, sticky=(tk.W, tk.E))

    ttk.Button(frame, text="Eliminar", command=eliminar).grid(column=1, row=2, sticky=tk.E)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

# Función para modificar producto
def modificar_producto():
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Producto")

    frame = ttk.Frame(ventana_modificar, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Buscar Producto:").grid(column=0, row=0, sticky=tk.W)
    entry_buscar = ttk.Entry(frame)
    entry_buscar.grid(column=1, row=0, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Selecciona un producto:").grid(column=0, row=1, sticky=tk.W)
    combo_productos = ttk.Combobox(frame)
    combo_productos.grid(column=1, row=1, sticky=(tk.W, tk.E))

    def actualizar_combobox_productos(event):
        busqueda = entry_buscar.get().lower()
        productos_filtrados = [producto["nombre"] for producto in productos if busqueda in producto["nombre"].lower()]
        combo_productos['values'] = productos_filtrados
        if productos_filtrados:
            combo_productos.set(productos_filtrados[0])
        else:
            combo_productos.set('')

    entry_buscar.bind('<KeyRelease>', actualizar_combobox_productos)

    ttk.Label(frame, text="Nombre del producto:").grid(column=0, row=2, sticky=tk.W)
    entry_nombre = ttk.Entry(frame)
    entry_nombre.grid(column=1, row=2, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Precio de venta:").grid(column=0, row=3, sticky=tk.W)
    entry_precio = ttk.Entry(frame)
    entry_precio.grid(column=1, row=3, sticky=(tk.W, tk.E))

    ttk.Label(frame, text="Cantidad en inventario:").grid(column=0, row=4, sticky=tk.W)
    entry_cantidad = ttk.Entry(frame)
    entry_cantidad.grid(column=1, row=4, sticky=(tk.W, tk.E))

    def cargar_producto_para_modificar():
        producto_seleccionado = combo_productos.get()
        for producto in productos:
            if producto["nombre"] == producto_seleccionado:
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, producto["nombre"])
                entry_precio.delete(0, tk.END)
                entry_precio.insert(0, producto["precio"])
                entry_cantidad.delete(0, tk.END)
                entry_cantidad.insert(0, producto["cantidad"])
                break

    def guardar_cambios():
        indice_a_modificar = None
        for indice, producto in enumerate(productos):
            if producto["nombre"] == combo_productos.get():
                indice_a_modificar = indice
                break

        if indice_a_modificar is not None:
            productos[indice_a_modificar] = {
                "nombre": entry_nombre.get(),
                "precio": float(entry_precio.get()),
                "cantidad": int(entry_cantidad.get())
            }
            guardar_productos()
            actualizar_combobox_productos(None)  # Actualiza el combobox con los productos actualizados
            messagebox.showinfo("Éxito", "Producto modificado con éxito")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto válido")

    ttk.Button(frame, text="Cargar Producto", command=cargar_producto_para_modificar).grid(column=0, row=5, sticky=tk.W)
    ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios).grid(column=1, row=5, sticky=tk.E)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    actualizar_combobox_productos(None)  # Inicializa el combobox al abrir la ventana

# Función para la caja de cobro
def caja_de_cobro(ventana_padre):
    caja = []
    ventana_cobro = tk.Toplevel(ventana_padre)
    ventana_cobro.title("Caja de Cobro")

    frame = ttk.Frame(ventana_cobro, padding="10 10 10 10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Buscador de Productos
    ttk.Label(frame, text="Buscar Producto:").grid(column=0, row=0, sticky=tk.W)
    entry_buscar = ttk.Entry(frame)
    entry_buscar.grid(column=1, row=0, sticky=(tk.W, tk.E))

    # Implementación de la función actualizar_lista_productos
    def actualizar_lista_productos(event):
        busqueda = entry_buscar.get().lower()
        productos_filtrados = [producto for producto in productos if busqueda in producto["nombre"].lower()]
        lista_productos.delete(0, tk.END)
        for producto in productos_filtrados:
            lista_productos.insert(tk.END, producto["nombre"])

    entry_buscar.bind('<KeyRelease>', actualizar_lista_productos)

    lista_productos = tk.Listbox(frame)
    lista_productos.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Etiqueta para mostrar el costo total
    etiqueta_costo_total = ttk.Label(frame, text="Costo Total: $0.00")
    etiqueta_costo_total.grid(column=0, row=2, sticky=tk.W)

    # Lista de Productos en Caja con Enumeración
    lista_caja = tk.Listbox(frame)
    lista_caja.grid(column=0, row=3, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Función para agregar productos a la caja
    def agregar_a_caja():
        seleccion = lista_productos.curselection()
        if seleccion:
            producto_seleccionado = productos[seleccion[0]]
            caja.append(producto_seleccionado)
            actualizar_lista_caja()
            actualizar_costo_total()

    ttk.Button(frame, text="Agregar a Caja", command=agregar_a_caja).grid(column=1, row=4, sticky=tk.E)

    # Función para actualizar el costo total
    def actualizar_costo_total():
        total = sum(p["precio"] for p in caja)
        etiqueta_costo_total.config(text=f"Costo Total: ${total:.2f}")

    # Función para actualizar la lista de productos en caja
    def actualizar_lista_caja():
        lista_caja.delete(0, tk.END)
        for indice, producto in enumerate(caja, start=1):
            lista_caja.insert(tk.END, f"{indice}. {producto['nombre']}")

    # Funciones de Método de Pago
    def realizar_cobro(metodo_pago):
        total = sum(p["precio"] for p in caja)
        if metodo_pago == "efectivo":
            pago_cliente = simpledialog.askfloat("Pago en Efectivo", "Cliente paga con: $", minvalue=total)
            if pago_cliente:
                cambio = pago_cliente - total
                messagebox.showinfo("Cambio", f"Cambio: ${cambio:.2f}")
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        guardar_venta([fecha_actual, len(ventas)+1, ", ".join(p["nombre"] for p in caja), total, metodo_pago])
        caja.clear()
        actualizar_lista_caja()

    ttk.Button(frame, text="Pagar con Efectivo", command=lambda: realizar_cobro("efectivo")).grid(column=0, row=5, sticky=(tk.W, tk.E))
    ttk.Button(frame, text="Pagar con Tarjeta", command=lambda: realizar_cobro("tarjeta")).grid(column=1, row=5, sticky=(tk.W, tk.E))

    # Función para el corte de caja
    def corte_de_caja():
        try:
            workbook = openpyxl.load_workbook("ventas_totales.xlsx")
            sheet = workbook.active

            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_efectivo = 0
            total_tarjeta = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                fecha_venta, _, _, total_venta, metodo_pago = row
                if fecha_venta == fecha_actual:
                    if metodo_pago == "efectivo":
                        total_efectivo += total_venta
                    elif metodo_pago == "tarjeta":
                        total_tarjeta += total_venta

            total_caja = dinero_inicial_caja + total_efectivo
            messagebox.showinfo("Corte de Caja", f"Total Efectivo: ${total_efectivo:.2f}\nTotal Tarjeta: ${total_tarjeta:.2f}\nTotal en Caja: ${total_caja:.2f}")

        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de ventas no encontrado.")

    ttk.Button(frame, text="Corte de Caja", command=corte_de_caja).grid(column=1, row=6, sticky=tk.E)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    ventana_cobro.columnconfigure(0, weight=1)
    ventana_cobro.rowconfigure(1, weight=1)


# Inicio del programa
if __name__ == "__main__":
    cargar_productos()
    mostrar_ventana_login()
