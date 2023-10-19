import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import openpyxl
import getpass
from datetime import datetime


# Variables globales
dinero_inicial_caja = 0

# Función para cargar productos desde un archivo Excel
def cargar_productos():
    try:
        archivo_productos = "productos.xlsx"
        if not os.path.exists(archivo_productos):
            return []

        workbook = openpyxl.load_workbook(archivo_productos)
        sheet = workbook.active
        productos = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            nombre, precio, cantidad = row
            producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
            productos.append(producto)

        return productos
    except FileNotFoundError:
        return []

# Función para el inicio de sesión
def login(cargar_productos, mostrar_ventas_dia, cobrar, ventas, guardar_venta, productos):
    global dinero_inicial_caja

    # Función para verificar las credenciales al inicio de sesión
    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "adminpass":
            dinero_inicial_caja = simpledialog.askfloat("Dinero Inicial", "Por favor, ingresa el efectivo inicial en caja: $")
            if dinero_inicial_caja is not None:
                login_window.destroy()
                admin_panel(cargar_productos, mostrar_ventas_dia, cobrar, ventas, guardar_venta, productos)
            else:
                messagebox.showwarning("Error", "Debes ingresar un valor válido para el dinero inicial.")
        elif username == "empleado" and password == "empleadopass":
            dinero_inicial_caja = simpledialog.askfloat("Dinero Inicial", "Por favor, ingresa el efectivo inicial en caja: $")
            if dinero_inicial_caja is not None:
                login_window.destroy()
                empleado_panel()
            else:
                messagebox.showwarning("Error", "Debes ingresar un valor válido para el dinero inicial.")
        else:
            messagebox.showerror("Error", "Credenciales incorrectas. Inténtalo de nuevo.")

    login_window = tk.Tk()
    login_window.title("Inicio de Sesión")

    tk.Label(login_window, text="Nombre de usuario:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Contraseña:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Iniciar Sesión", command=check_login)
    login_button.pack()

    login_window.mainloop()


# Función para el panel de administrador
def admin_panel(cargar_productos, mostrar_ventas_dia, cobrar, ventas, guardar_venta, productos):
    admin_window = tk.Tk()
    admin_window.title("Panel de Administrador")

    # Lista de productos
    productos = cargar_productos()



    # Función para guardar los productos en un archivo Excel
    def guardar_productos():
        archivo_productos = "productos.xlsx"
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Encabezados
        sheet.append(["Nombre", "Precio de Venta", "Cantidad en Inventario"])

        # Agrega los productos al archivo Excel
        for producto in productos:
            sheet.append([producto["nombre"], producto["precio"], producto["cantidad"]])

        workbook.save(archivo_productos)

    # Función para agregar un producto
    def agregar_producto():
        nombre = simpledialog.askstring("Agregar Producto", "Nombre del producto:")
        precio = simpledialog.askfloat("Agregar Producto", "Precio de venta:")
        cantidad = simpledialog.askinteger("Agregar Producto", "Cantidad en inventario:")

        if nombre and precio is not None and cantidad is not None:
            producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
            productos.append(producto)
            guardar_productos()
            messagebox.showinfo("Éxito", f"{nombre} ha sido agregado al inventario.")
        else:
            messagebox.showwarning("Error", "Por favor, ingresa valores válidos.")

# Función para eliminar un producto
    def eliminar_producto():
        def delete_product():
            selected_product = combo.get()
            if selected_product:
                for producto in productos:
                    if producto["nombre"] == selected_product:
                        productos.remove(producto)
                        guardar_productos()
                        messagebox.showinfo("Éxito", f"{selected_product} ha sido eliminado del inventario.")
                        eliminar_window.destroy()
                        break

        if not productos:
            messagebox.showinfo("Información", "No hay productos para eliminar.")
            return

        eliminar_window = tk.Toplevel()
        eliminar_window.title("Eliminar Producto")

        producto_names = [producto["nombre"] for producto in productos]
        combo = tk.StringVar()
        combo.set(producto_names[0])  # Valor inicial
        combo_box = tk.OptionMenu(eliminar_window, combo, *producto_names)
        combo_box.pack()

        delete_button = tk.Button(eliminar_window, text="Eliminar Producto", command=delete_product)
        delete_button.pack()


   # Función para modificar un producto
    def modificar_producto():
        def apply_changes():
            selected_product = combo.get()
            modified_name = name_entry.get()
            modified_price = price_entry.get()
            modified_inventory = inventory_entry.get()

            if selected_product and modified_name and modified_price and modified_inventory:
                for producto in productos:
                    if producto["nombre"] == selected_product:
                        producto["nombre"] = modified_name
                        producto["precio"] = float(modified_price)
                        producto["cantidad"] = int(modified_inventory)
                        guardar_productos()
                        messagebox.showinfo("Éxito", f"{selected_product} ha sido modificado en el inventario.")
                        modificar_window.destroy()
                        break

        if not productos:
            messagebox.showinfo("Información", "No hay productos para modificar.")
            return

        modificar_window = tk.Toplevel()
        modificar_window.title("Modificar Producto")

        producto_names = [producto["nombre"] for producto in productos]
        combo = tk.StringVar()
        combo.set(producto_names[0])  # Valor inicial
        combo_box = tk.OptionMenu(modificar_window, combo, *producto_names)
        combo_box.pack()

        tk.Label(modificar_window, text="Nuevo Nombre:").pack()
        name_entry = tk.Entry(modificar_window)
        name_entry.pack()

        tk.Label(modificar_window, text="Nuevo Precio:").pack()
        price_entry = tk.Entry(modificar_window)
        price_entry.pack()

        tk.Label(modificar_window, text="Nuevo Inventario:").pack()
        inventory_entry = tk.Entry(modificar_window)
        inventory_entry.pack()

        apply_button = tk.Button(modificar_window, text="Aplicar Cambios", command=apply_changes)
        apply_button.pack()

    
    # Función para la sección de caja de cobro
    def caja_de_cobro(mostrar_ventas_dia, cobrar, ventas, guardar_venta, productos):
        caja = []

        while True:
            opciones = ["Agregar producto a la caja", "Eliminar producto de la caja", "Hacer corte de caja", "Cobrar productos y volver a la caja", "Salir de la caja"]
            opcion = simpledialog.askoption("Caja de Cobro", "Opciones de caja de cobro:", optionlist=opciones)

            if opcion == opciones[0]:
                if productos:
                    producto_names = [producto["nombre"] for producto in productos]
                    selected_product = simpledialog.askstring("Agregar Producto", "Productos disponibles:", initialvalue="\n".join(producto_names))
                    if selected_product in producto_names:
                        index = producto_names.index(selected_product)
                        caja.append(productos.pop(index))
                        messagebox.showinfo("Éxito", f"{selected_product} ha sido agregado a la caja.")
                    else:
                        messagebox.showwarning("Error", "Producto no encontrado.")
                else:
                    messagebox.showinfo("Información", "No hay productos disponibles.")
            elif opcion == opciones[1]:
                if not caja:
                    messagebox.showinfo("Información", "La caja está vacía.")
                else:
                    selected_product = simpledialog.askstring("Eliminar Producto", "Productos en la caja:", initialvalue="\n".join([producto["nombre"] for producto in caja]))
                    if selected_product in [producto["nombre"] for producto in caja]:
                        index = [producto["nombre"] for producto in caja].index(selected_product)
                        removed_product = caja.pop(index)
                        productos.append(removed_product)  # Devuelve el producto al inventario
                        messagebox.showinfo("Éxito", f"{removed_product['nombre']} ha sido eliminado de la caja.")
                    else:
                        messagebox.showwarning("Error", "Producto no encontrado en la caja.")
            elif opcion == opciones[2]:
                total_ventas = mostrar_ventas_dia(ventas)
                dinero_en_caja = simpledialog.askfloat("Corte de Caja", "Ingrese la cantidad de dinero en caja: $")
                if dinero_en_caja is not None:
                    diferencia = dinero_en_caja - dinero_inicial_caja - total_ventas
                    messagebox.showinfo("Corte de Caja", f"Diferencia entre caja y ventas: ${diferencia:.2f}")
            elif opcion == opciones[3]:
                total_venta, metodo_pago = cobrar(caja)
                guardar_venta(total_venta, metodo_pago, caja)
                total_ventas += total_venta
                caja = []
            elif opcion == opciones[4]:
                break

    # Botones para agregar, eliminar y modificar productos
    tk.Button(admin_window, text="Agregar Producto", command=agregar_producto).pack()
    tk.Button(admin_window, text="Eliminar Producto", command=eliminar_producto).pack()
    tk.Button(admin_window, text="Modificar Producto", command=modificar_producto).pack()
    # Botón para abrir la caja de cobro en el panel de administrador
    tk.Button(admin_window, text="Caja de Cobro", command=lambda: caja_de_cobro(mostrar_ventas_dia, cobrar, ventas, guardar_venta, productos)).pack()
    # Botón para guardar cambios y salir
    tk.Button(admin_window, text="Guardar Cambios y Salir", command=lambda: [guardar_productos(productos), admin_window.destroy()]).pack()

    admin_window.mainloop()


# Función para el panel de empleado
def empleado_panel():
    empleado_window = tk.Tk()
    empleado_window.title("Panel de Empleado")

    # Lista para mantener el registro de ventas durante la sesión
    ventas = []

    # Función para cargar las ventas de una fecha específica
    def cargar_ventas(fecha):
        try:
            archivo_ventas = "ventas_totales.xlsx"
            if not os.path.exists(archivo_ventas):
                return []

            workbook = openpyxl.load_workbook(archivo_ventas)
            sheet = workbook.active
            ventas = []

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] == fecha:
                    ventas.append(row)

            return ventas
        except FileNotFoundError:
            return []

    # Función para guardar la venta en un archivo Excel
    def guardar_venta(total, metodo_pago, caja):
        if not caja:
            messagebox.showwarning("Error", "No se puede guardar una venta vacía.")
            return

        fecha_actual = datetime.now().strftime("%Y-%m-d")
        archivo_ventas = "ventas_totales.xlsx"

        if not os.path.exists(archivo_ventas):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Fecha", "ID Venta", "Productos", "Total Venta", "Método de Pago"])
        else:
            workbook = openpyxl.load_workbook(archivo_ventas)
            sheet = workbook.active

        productos_vendidos = ", ".join(producto["nombre"] for producto in caja)
        nueva_fila = [fecha_actual, len(sheet["A"]) + 1, productos_vendidos, total, metodo_pago]
        sheet.append(nueva_fila)

        workbook.save(archivo_ventas)

        ventas.append(nueva_fila)  # Agregar la venta al registro de ventas

    # Función para cobrar productos y calcular el cambio
    def cobrar(caja):
        if not caja:
            messagebox.showwarning("Error", "La caja está vacía. No se puede realizar el cobro.")
            return 0, "n/a"

        total = sum(producto["precio"] for producto in caja)
        metodo_pago = simpledialog.askstring("Cobrar", f"Total a cobrar: ${total}\nMétodo de pago (efectivo/tarjeta):", initialvalue="efectivo")

        if metodo_pago:
            if metodo_pago == "efectivo":
                pago_efectivo = simpledialog.askfloat("Cobrar", "Monto en efectivo:")
                if pago_efectivo is not None:
                    cambio = pago_efectivo - total
                    if cambio < 0:
                        messagebox.showwarning("Error", "El monto en efectivo es insuficiente.")
                    else:
                        messagebox.showinfo("Cobro Realizado", f"¡Cambio: ${cambio:.2f}")
                    return total, "efectivo"
            elif metodo_pago == "tarjeta":
                messagebox.showinfo("Cobro Realizado", "Por favor, verifique que el cobro se haya efectuado de manera correcta.")
                return total, "tarjeta"
            else:
                messagebox.showwarning("Error", "Método de pago inválido.")
        return 0, "n/a"

    # Función para la sección de caja de cobro
    def caja_de_cobro(mostrar_ventas_dia, cobrar, ventas, guardar_venta, productos):
        caja = []

        while True:
            opciones = ["Agregar producto a la caja", "Eliminar producto de la caja", "Hacer corte de caja", "Cobrar productos y volver a la caja", "Salir de la caja"]
            opcion = simpledialog.askoption("Caja de Cobro", "Opciones de caja de cobro:", optionlist=opciones)

            if opcion == opciones[0]:
                if productos:
                    producto_names = [producto["nombre"] for producto in productos]
                    selected_product = simpledialog.askstring("Agregar Producto", "Productos disponibles:", initialvalue="\n".join(producto_names))
                    if selected_product in producto_names:
                        index = producto_names.index(selected_product)
                        caja.append(productos.pop(index))
                        messagebox.showinfo("Éxito", f"{selected_product} ha sido agregado a la caja.")
                    else:
                        messagebox.showwarning("Error", "Producto no encontrado.")
                else:
                    messagebox.showinfo("Información", "No hay productos disponibles.")
            elif opcion == opciones[1]:
                if not caja:
                    messagebox.showinfo("Información", "La caja está vacía.")
                else:
                    selected_product = simpledialog.askstring("Eliminar Producto", "Productos en la caja:", initialvalue="\n".join([producto["nombre"] for producto in caja]))
                    if selected_product in [producto["nombre"] for producto in caja]:
                        index = [producto["nombre"] for producto in caja].index(selected_product)
                        removed_product = caja.pop(index)
                        messagebox.showinfo("Éxito", f"{removed_product['nombre']} ha sido eliminado de la caja.")
                    else:
                        messagebox.showwarning("Error", "Producto no encontrado en la caja.")
            elif opcion == opciones[2]:
                total_ventas = mostrar_ventas_dia(ventas)
                dinero_en_caja = simpledialog.askfloat("Corte de Caja", "Ingrese la cantidad de dinero en caja: $")
                if dinero_en_caja is not None:
                    diferencia = dinero_en_caja - dinero_inicial_caja - total_ventas
                    messagebox.showinfo("Corte de Caja", f"Diferencia entre caja y ventas: ${diferencia:.2f}")
            elif opcion == opciones[3]:
                total_venta, metodo_pago = cobrar(caja)
                guardar_venta(total_venta, metodo_pago, caja)
                total_ventas += total_venta
                caja = []
            elif opcion == opciones[4]:
                break

    # Función para mostrar las ventas del día
    def mostrar_ventas_dia(ventas):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        ventas_del_dia = cargar_ventas(fecha_actual)

        if not ventas_del_dia:
            messagebox.showinfo("Información", "No hay ventas registradas para el día de hoy.")
            return 0

        total_ventas_dia = sum(venta[3] for venta in ventas_del_dia)

        venta_str = ""
        for venta in ventas_del_dia:
            venta_str += f"ID Venta: {venta[1]}\nProductos: {venta[2]}\nTotal Venta: ${venta[3]:.2f}\nMétodo de Pago: {venta[4]}\n\n"

        messagebox.showinfo(f"Ventas del día ({fecha_actual})", venta_str + f"Dinero total de las ventas: ${total_ventas_dia:.2f}")
        return total_ventas_dia

    tk.Button(empleado_window, text="Caja de Cobro", command=caja_de_cobro).pack()

    empleado_window.mainloop()

if __name__ == "__main__":
    login()