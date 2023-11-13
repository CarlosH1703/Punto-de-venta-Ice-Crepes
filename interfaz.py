import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
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
def mostrar_ventana_login():
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")

    tk.Label(ventana_login, text="Nombre de usuario:").pack()
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()

    tk.Label(ventana_login, text="Contraseña:").pack()
    entry_contrasena = tk.Entry(ventana_login, show="*")
    entry_contrasena.pack()

    tk.Button(ventana_login, text="Iniciar sesión", command=lambda: iniciar_sesion(entry_usuario.get(), entry_contrasena.get())).pack()
    ventana_login.mainloop()

# Ventana Principal
def mostrar_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de Gestión")

    if tipo_usuario == "admin":
        tk.Button(ventana_principal, text="Agregar Producto", command=agregar_producto).pack()
        tk.Button(ventana_principal, text="Eliminar Producto", command=eliminar_producto).pack()
        tk.Button(ventana_principal, text="Modificar Producto", command=modificar_producto).pack()

    tk.Button(ventana_principal, text="Caja de Cobro", command=lambda: caja_de_cobro(ventana_principal)).pack()
    tk.Button(ventana_principal, text="Salir", command=ventana_principal.destroy).pack()

# Función para agregar producto
def agregar_producto():
    def guardar_nuevo_producto():
        nombre = entry_nombre.get()
        precio = float(entry_precio.get())
        cantidad = int(entry_cantidad.get())
        productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
        ventana_agregar.destroy()
        guardar_productos()

    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Producto")

    tk.Label(ventana_agregar, text="Nombre del producto:").pack()
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.pack()

    tk.Label(ventana_agregar, text="Precio de venta:").pack()
    entry_precio = tk.Entry(ventana_agregar)
    entry_precio.pack()

    tk.Label(ventana_agregar, text="Cantidad en inventario:").pack()
    entry_cantidad = tk.Entry(ventana_agregar)
    entry_cantidad.pack()

    tk.Button(ventana_agregar, text="Agregar", command=guardar_nuevo_producto).pack()

# Función para eliminar producto
def eliminar_producto():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Producto")

    # Crear un Combobox en lugar de un Listbox
    nombres_productos = [producto["nombre"] for producto in productos]
    combo_productos = ttk.Combobox(ventana_eliminar, values=nombres_productos)
    combo_productos.pack()

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
            # Actualizar los valores del combobox
            combo_productos['values'] = [producto["nombre"] for producto in productos]
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto")

    tk.Button(ventana_eliminar, text="Eliminar", command=eliminar).pack()

# Función para modificar producto
def modificar_producto():
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Producto")

    # Crear un Combobox para seleccionar el producto a modificar
    nombres_productos = [producto["nombre"] for producto in productos]
    combo_productos = ttk.Combobox(ventana_modificar, values=nombres_productos)
    combo_productos.pack()

    tk.Label(ventana_modificar, text="Nombre del producto:").pack()
    entry_nombre = tk.Entry(ventana_modificar)
    entry_nombre.pack()

    tk.Label(ventana_modificar, text="Precio de venta:").pack()
    entry_precio = tk.Entry(ventana_modificar)
    entry_precio.pack()

    tk.Label(ventana_modificar, text="Cantidad en inventario:").pack()
    entry_cantidad = tk.Entry(ventana_modificar)
    entry_cantidad.pack()

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

    tk.Button(ventana_modificar, text="Cargar Producto", command=cargar_producto_para_modificar).pack()

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
            # Actualizar los valores del combobox
            combo_productos['values'] = [producto["nombre"] for producto in productos]
            messagebox.showinfo("Éxito", "Producto modificado con éxito")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto válido")

    tk.Button(ventana_modificar, text="Guardar Cambios", command=guardar_cambios).pack()


# Función para la caja de cobro
def caja_de_cobro(ventana_padre):
    caja = []
    ventana_cobro = tk.Toplevel(ventana_padre)
    ventana_cobro.title("Caja de Cobro")

    # Buscador de Productos
    def actualizar_lista_productos(event):
        busqueda = entry_buscar.get().lower()
        productos_filtrados = [producto for producto in productos if busqueda in producto["nombre"].lower()]
        lista_productos.delete(0, tk.END)
        for producto in productos_filtrados:
            lista_productos.insert(tk.END, producto["nombre"])

    tk.Label(ventana_cobro, text="Buscar Producto:").pack()
    entry_buscar = tk.Entry(ventana_cobro)
    entry_buscar.pack()
    entry_buscar.bind('<KeyRelease>', actualizar_lista_productos)

    lista_productos = tk.Listbox(ventana_cobro)
    lista_productos.pack()

# Etiqueta para mostrar el costo total
    etiqueta_costo_total = tk.Label(ventana_cobro, text="Costo Total: $0.00")
    etiqueta_costo_total.pack()

    def actualizar_costo_total():
        total = sum(p["precio"] for p in caja)
        etiqueta_costo_total.config(text=f"Costo Total: ${total:.2f}")

    # Lista de Productos en Caja con Enumeración
    lista_caja = tk.Listbox(ventana_cobro)
    lista_caja.pack()

    def actualizar_lista_caja():
        lista_caja.delete(0, tk.END)
        for indice, producto in enumerate(caja, start=1):
            lista_caja.insert(tk.END, f"{indice}. {producto['nombre']}")

    def agregar_a_caja():
        seleccion = lista_productos.curselection()
        if seleccion:
            producto_seleccionado = productos[seleccion[0]]
            caja.append(producto_seleccionado)
            actualizar_lista_caja()
            actualizar_costo_total()

    tk.Button(ventana_cobro, text="Agregar a Caja", command=agregar_a_caja).pack()

    # Método de Pago
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

    tk.Button(ventana_cobro, text="Pagar con Efectivo", command=lambda: realizar_cobro("efectivo")).pack()
    tk.Button(ventana_cobro, text="Pagar con Tarjeta", command=lambda: realizar_cobro("tarjeta")).pack()

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



    tk.Button(ventana_cobro, text="Corte de Caja", command=corte_de_caja).pack()


# Inicio del programa
if __name__ == "__main__":
    cargar_productos()
    mostrar_ventana_login()
