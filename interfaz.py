import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import customtkinter as ctk
import openpyxl
import os
from datetime import datetime


# Variables globales
productos = []
ventas = []
tipo_usuario = None
dinero_inicial_caja = 0
entry_buscar = None  # Definir aquí para que sea accesible en todo el código
combo_productos = None  # Definir aquí para que sea accesible en todo el código

#funcion para centrar las ventanas
def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    x_pos = ventana.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_pos = ventana.winfo_screenheight() // 2 - alto_ventana // 2
    ventana.geometry(f"+{x_pos}+{y_pos}")


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
        print("Archivo de productos no encontrado.")
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
    ventana_login = ctk.CTk()
    ventana_login.title("Inicio de Sesión")
    centrar_ventana(ventana_login)

    # Usar CTkFrame sin el argumento padding
    frame = ctk.CTkFrame(ventana_login)
    frame.grid(row=0, column=0, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    ctk.CTkLabel(frame, text="Nombre de usuario:").grid(column=0, row=0, sticky=ctk.W)
    entry_usuario = ctk.CTkEntry(frame)
    entry_usuario.grid(column=1, row=0, sticky=(ctk.W, ctk.E))

    ctk.CTkLabel(frame, text="Contraseña:").grid(column=0, row=1, sticky=ctk.W)
    entry_contrasena = ctk.CTkEntry(frame, show="*")
    entry_contrasena.grid(column=1, row=1, sticky=(ctk.W, ctk.E))

    ctk.CTkButton(frame, text="Iniciar sesión", command=lambda: iniciar_sesion(entry_usuario.get(), entry_contrasena.get(), ventana_login)).grid(column=1, row=2, sticky=ctk.E)

    ventana_login.mainloop()


# Ventana Principal
def mostrar_ventana_principal():
    ventana_principal = ctk.CTk()
    ventana_principal.title("Sistema de Gestión")
    centrar_ventana(ventana_principal)

    frame = ctk.CTkFrame(ventana_principal)
    frame.grid(row=0, column=0, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    if tipo_usuario == "admin":
        ctk.CTkButton(frame, text="Agregar Producto", command=agregar_producto).grid(column=0, row=0, sticky=(ctk.W, ctk.E))
        ctk.CTkButton(frame, text="Eliminar Producto", command=eliminar_producto).grid(column=1, row=0, sticky=(ctk.W, ctk.E))
        ctk.CTkButton(frame, text="Modificar Producto", command=modificar_producto).grid(column=2, row=0, sticky=(ctk.W, ctk.E))

    ctk.CTkButton(frame, text="Caja de Cobro", command=lambda: caja_de_cobro(ventana_principal)).grid(column=0, row=1, sticky=(ctk.W, ctk.E))
    ctk.CTkButton(frame, text="Salir", command=ventana_principal.destroy).grid(column=2, row=1, sticky=ctk.E)

    ventana_principal.mainloop()

# Función para agregar producto
def agregar_producto():
    ventana_agregar = ctk.CTkToplevel()
    ventana_agregar.title("Agregar Producto")
    centrar_ventana(ventana_agregar)

    frame = ctk.CTkFrame(ventana_agregar)
    frame.grid(row=0, column=0, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    ctk.CTkLabel(frame, text="Nombre del producto:").grid(column=0, row=0, sticky=ctk.W)
    entry_nombre = ctk.CTkEntry(frame)
    entry_nombre.grid(column=1, row=0, sticky=(ctk.W, ctk.E))

    ctk.CTkLabel(frame, text="Precio de venta:").grid(column=0, row=1, sticky=ctk.W)
    entry_precio = ctk.CTkEntry(frame)
    entry_precio.grid(column=1, row=1, sticky=(ctk.W, ctk.E))

    ctk.CTkLabel(frame, text="Cantidad en inventario:").grid(column=0, row=2, sticky=ctk.W)
    entry_cantidad = ctk.CTkEntry(frame)
    entry_cantidad.grid(column=1, row=2, sticky=(ctk.W, ctk.E))

    ctk.CTkButton(frame, text="Agregar", command=lambda: guardar_nuevo_producto()).grid(column=1, row=3, sticky=ctk.E)

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
def actualizar_option_menu(event=None):
    global combo_productos, entry_buscar, frame
    busqueda = entry_buscar.get().lower() if entry_buscar and entry_buscar.get() else ""
    productos_filtrados = [producto["nombre"] for producto in productos if busqueda in producto["nombre"].lower()]

    # Destruir el CTkOptionMenu anterior
    if combo_productos:
        combo_productos.destroy()

    # Crear un nuevo CTkOptionMenu con los productos filtrados
    combo_productos = ctk.CTkOptionMenu(frame, variable=tk.StringVar(), values=productos_filtrados)
    combo_productos.grid(column=1, row=1, sticky=(ctk.W, ctk.E))

    # Establecer el primer producto filtrado como seleccionado, si hay alguno
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
        actualizar_option_menu(None)
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un producto")

def eliminar_producto():
    global entry_buscar, combo_productos, frame
    ventana_eliminar = ctk.CTkToplevel()
    ventana_eliminar.title("Eliminar Producto")
    centrar_ventana(ventana_eliminar)

    frame = ctk.CTkFrame(ventana_eliminar)
    frame.grid(row=0, column=0, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    ctk.CTkLabel(frame, text="Buscar Producto:").grid(column=0, row=0, sticky=ctk.W)
    entry_buscar = ctk.CTkEntry(frame)
    entry_buscar.grid(column=1, row=0, sticky=(ctk.W, ctk.E))
    entry_buscar.bind('<KeyRelease>', actualizar_option_menu)

    # Crear el CTkOptionMenu inicial con todos los productos
    combo_productos = ctk.CTkOptionMenu(frame, variable=tk.StringVar(), values=[producto["nombre"] for producto in productos])
    combo_productos.grid(column=1, row=1, sticky=(ctk.W, ctk.E))
    if productos:
        combo_productos.set(productos[0]["nombre"])

    ctk.CTkButton(frame, text="Eliminar", command=eliminar).grid(column=1, row=2, sticky=ctk.E)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)


# Función para actualizar el OptionMenu
def actualizar_option_menu_modificar(event=None):
    global combo_productos_modificar, entry_buscar_modificar, frame_modificar
    busqueda = entry_buscar_modificar.get().lower() if entry_buscar_modificar and entry_buscar_modificar.get() else ""
    productos_filtrados = [producto["nombre"] for producto in productos if busqueda in producto["nombre"].lower()]

    if combo_productos_modificar:
        combo_productos_modificar.destroy()

    combo_productos_modificar = ctk.CTkOptionMenu(frame_modificar, variable=tk.StringVar(), values=productos_filtrados)
    combo_productos_modificar.grid(column=1, row=1, sticky=(ctk.W, ctk.E))

    if productos_filtrados:
        combo_productos_modificar.set(productos_filtrados[0])
    else:
        combo_productos_modificar.set('')

# Función para cargar los detalles del producto para modificar
def cargar_producto_para_modificar():
    producto_seleccionado = combo_productos_modificar.get()
    for producto in productos:
        if producto["nombre"] == producto_seleccionado:
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, producto["nombre"])
            entry_precio.delete(0, tk.END)
            entry_precio.insert(0, producto["precio"])
            entry_cantidad.delete(0, tk.END)
            entry_cantidad.insert(0, producto["cantidad"])
            break

# Función para guardar los cambios del producto
def guardar_cambios_producto():
    producto_seleccionado = combo_productos_modificar.get()
    for producto in productos:
        if producto["nombre"] == producto_seleccionado:
            producto["nombre"] = entry_nombre.get()
            producto["precio"] = float(entry_precio.get())
            producto["cantidad"] = int(entry_cantidad.get())
            break
    actualizar_option_menu_modificar()  # Actualizar el OptionMenu
    messagebox.showinfo("Éxito", "Producto modificado con éxito")

# Función para modificar producto
def modificar_producto():
    global entry_buscar_modificar, combo_productos_modificar, frame_modificar, entry_nombre, entry_precio, entry_cantidad
    ventana_modificar = ctk.CTkToplevel()
    ventana_modificar.title("Modificar Producto")
    centrar_ventana(ventana_modificar)

    frame_modificar = ctk.CTkFrame(ventana_modificar)
    frame_modificar.grid(row=0, column=0, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    ctk.CTkLabel(frame_modificar, text="Buscar Producto:").grid(column=0, row=0, sticky=ctk.W)
    entry_buscar_modificar = ctk.CTkEntry(frame_modificar)
    entry_buscar_modificar.grid(column=1, row=0, sticky=(ctk.W, ctk.E))
    entry_buscar_modificar.bind('<KeyRelease>', actualizar_option_menu_modificar)

    combo_productos_modificar = ctk.CTkOptionMenu(frame_modificar, variable=tk.StringVar(), values=[producto["nombre"] for producto in productos])
    combo_productos_modificar.grid(column=1, row=1, sticky=(ctk.W, ctk.E))
    if productos:
        combo_productos_modificar.set(productos[0]["nombre"])

    ctk.CTkLabel(frame_modificar, text="Nombre del producto:").grid(column=0, row=2, sticky=ctk.W)
    entry_nombre = ctk.CTkEntry(frame_modificar)
    entry_nombre.grid(column=1, row=2, sticky=(ctk.W, ctk.E))

    ctk.CTkLabel(frame_modificar, text="Precio de venta:").grid(column=0, row=3, sticky=ctk.W)
    entry_precio = ctk.CTkEntry(frame_modificar)
    entry_precio.grid(column=1, row=3, sticky=(ctk.W, ctk.E))

    ctk.CTkLabel(frame_modificar, text="Cantidad en inventario:").grid(column=0, row=4, sticky=ctk.W)
    entry_cantidad = ctk.CTkEntry(frame_modificar)
    entry_cantidad.grid(column=1, row=4, sticky=(ctk.W, ctk.E))

    ctk.CTkButton(frame_modificar, text="Cargar Producto", command=cargar_producto_para_modificar).grid(column=0, row=5, sticky=ctk.W)
    ctk.CTkButton(frame_modificar, text="Guardar Cambios", command=guardar_cambios_producto).grid(column=1, row=5, sticky=ctk.E)

    for child in frame_modificar.winfo_children():
        child.grid_configure(padx=5, pady=5)

    actualizar_option_menu_modificar()

# Función para la caja de cobro
def caja_de_cobro(ventana_padre):
    caja = []
    ventana_cobro = ctk.CTkToplevel(ventana_padre)
    ventana_cobro.title("Caja de Cobro")
    centrar_ventana(ventana_cobro)

    frame = ctk.CTkFrame(ventana_cobro)
    frame.grid(row=0, column=0, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    # Buscador de Productos
    ctk.CTkLabel(frame, text="Buscar Producto:").grid(column=0, row=0, sticky=ctk.W)
    entry_buscar = ttk.Entry(frame)
    entry_buscar.grid(column=1, row=0, sticky=(ctk.W, ctk.E))

    # Implementación de la función actualizar_lista_productos
    def actualizar_lista_productos(event):
        busqueda = entry_buscar.get().lower()
        productos_filtrados = [producto for producto in productos if busqueda in producto["nombre"].lower()]
        lista_productos.delete(0, ctk.END)
        for producto in productos_filtrados:
            lista_productos.insert(ctk.END, producto["nombre"])

    entry_buscar.bind('<KeyRelease>', actualizar_lista_productos)

    lista_productos = tk.Listbox(frame)
    lista_productos.grid(column=0, row=1, columnspan=2, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    # Etiqueta para mostrar el costo total
    etiqueta_costo_total = ctk.CTkLabel(frame, text="Costo Total: $0.00")
    etiqueta_costo_total.grid(column=0, row=2, sticky=ctk.W)

    # Lista de Productos en Caja con Enumeración
    lista_caja = tk.Listbox(frame)
    lista_caja.grid(column=0, row=3, columnspan=2, sticky=(ctk.W, ctk.E, ctk.N, ctk.S))

    # Función para agregar productos a la caja
    def agregar_a_caja():
        seleccion = lista_productos.curselection()
        if seleccion:
            nombre_producto_seleccionado = lista_productos.get(seleccion[0])
            producto_seleccionado = next((producto for producto in productos if producto["nombre"] == nombre_producto_seleccionado), None)
            if producto_seleccionado:
                caja.append(producto_seleccionado)
                actualizar_lista_caja()
                actualizar_costo_total()

    ctk.CTkButton(frame, text="Agregar a Caja", command=agregar_a_caja).grid(column=0, row=4, sticky=ctk.E)
    #funcion para eliminar productos de la caja
    def eliminar_de_caja():
        seleccion = lista_caja.curselection()
        if seleccion:
            del caja[seleccion[0]]
            actualizar_lista_caja()
            actualizar_costo_total()

    ctk.CTkButton(frame, text="Eliminar de Caja", command=eliminar_de_caja).grid(column=1, row=4, sticky=ctk.E)

    # Función para actualizar el costo total
    def actualizar_costo_total():
        total = sum(p["precio"] for p in caja)
        etiqueta_costo_total.configure(text=f"Costo Total: ${total:.2f}")

    # Función para actualizar la lista de productos en caja
    def actualizar_lista_caja():
        lista_caja.delete(0, ctk.END)
        for indice, producto in enumerate(caja, start=1):
            lista_caja.insert(ctk.END, f"{indice}. {producto['nombre']}")

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

    ctk.CTkButton(frame, text="Pagar con Efectivo", command=lambda: realizar_cobro("efectivo")).grid(column=0, row=6, sticky=(ctk.W, ctk.E))
    ctk.CTkButton(frame, text="Pagar con Tarjeta", command=lambda: realizar_cobro("tarjeta")).grid(column=1, row=6, sticky=(ctk.W, ctk.E))

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

    ctk.CTkButton(frame, text="Corte de Caja", command=corte_de_caja).grid(column=1, row=7, sticky=ctk.E)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    ventana_cobro.columnconfigure(0, weight=1)
    ventana_cobro.rowconfigure(1, weight=1)


# Inicio del programa
if __name__ == "__main__":
    cargar_productos()
    mostrar_ventana_login()
