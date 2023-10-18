from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import os
import openpyxl
from datetime import datetime

class InventoryApp(App):
    def build(self):
        self.title = "Gestión de Inventario"
        
        self.username_input = TextInput(hint_text="Nombre de usuario")
        self.password_input = TextInput(hint_text="Contraseña", password=True)
        self.login_button = Button(text="Iniciar sesión", on_press=self.login)

        self.add_product_button = Button(text="Agregar Producto", on_press=self.add_product)
        self.delete_product_button = Button(text="Eliminar Producto", on_press=self.delete_product)
        self.modify_product_button = Button(text="Modificar Producto", on_press=self.modify_product)
        self.cashier_button = Button(text="Caja de Cobro", on_press=self.cashier)
        self.result_label = Label()
        self.scroll_view = ScrollView()
        self.sales_label = Label()
        self.products_label = Label()

        self.productos = []  # Lista de productos
        self.tipo_usuario = ""  # Tipo de usuario (admin o empleado)
        self.ventas = []  # Registro de ventas
        self.total_ventas = 0  # Total de ventas
        self.dinero_inicial_caja = 0  # Dinero inicial en caja

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)
        layout.add_widget(self.add_product_button)
        layout.add_widget(self.delete_product_button)
        layout.add_widget(self.modify_product_button)
        layout.add_widget(self.cashier_button)
        layout.add_widget(self.result_label)
        layout.add_widget(self.scroll_view)
        layout.add_widget(self.sales_label)
        layout.add_widget(self.products_label)
        return layout

    def mostrar_ventas_dia(self, ventas):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        self.sales_label.text = f"Ventas del día ({fecha_actual}):\n"
        ventas_del_dia = self.cargar_ventas(fecha_actual)

        if not ventas_del_dia:
            self.sales_label.text += "No hay ventas registradas para el día de hoy."
            return

        total_ventas_dia = sum(venta[3] for venta in ventas_del_dia)  # Calcula el total de las ventas del día

        for venta in ventas_del_dia:
            self.sales_label.text += f"ID Venta: {venta[1]}\n"
            self.sales_label.text += f"Productos: {venta[2]}\n"
            self.sales_label.text += f"Total Venta: ${venta[3]}\n"
            self.sales_label.text += f"Método de Pago: {venta[4]}\n\n"

        self.sales_label.text += f"Dinero total de las ventas: ${total_ventas_dia:.2f}"

        return total_ventas_dia  # Devuelve el total de las ventas del día

    def cobrar(self, caja):
        if not caja:
            self.result_label.text = "La caja está vacía. No se puede realizar el cobro."
            return 0, "n/a"

        total = sum(producto["precio"] for producto in caja)
        self.result_label.text = f"Total a cobrar: ${total}"
        metodo_pago = TextInput("Método de pago (efectivo/tarjeta): ")

        if metodo_pago == "efectivo":
            pago_efectivo = float(TextInput("Monto en efectivo: "))
            cambio = pago_efectivo - total

            if cambio < 0:
                self.result_label.text = "El monto en efectivo es insuficiente."
            else:
                self.result_label.text = f"¡Cambio: ${cambio:.2f}"
            return total, "efectivo"
        elif metodo_pago == "tarjeta":
            self.result_label.text = "Por favor, verifique que el cobro se haya efectuado de manera correcta."
            return total, "tarjeta"
        else:
            self.result_label.text = "Método de pago inválido."
            return 0, "n/a"

        total = sum(producto["precio"] for producto in caja)
        self.result_label.text = f"Total a cobrar: ${total}"
        metodo_pago = TextInput("Método de pago (efectivo/tarjeta): ")

        if metodo_pago == "efectivo":
            pago_efectivo = float(TextInput("Monto en efectivo: "))
            cambio = pago_efectivo - total

            if cambio < 0:
                self.result_label.text = "El monto en efectivo es insuficiente."
            else:
                self.result_label.text = f"¡Cambio: ${cambio:.2f}"
            return total, "efectivo"
        elif metodo_pago == "tarjeta":
            self.result_label.text = "Por favor, verifique que el cobro se haya efectuado de manera correcta."
            return total, "tarjeta"
        else:
            self.result_label.text = "Método de pago inválido."
            return 0, "n/a"


    # Función para el inicio de sesión
    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == "admin" and password == "adminpass":
            self.tipo_usuario = "admin"
            self.dinero_inicial_caja = float(TextInput("Por favor, ingresa el efectivo inicial en caja: $"))
            self.result_label.text = "Iniciaste sesión como administrador."
        elif username == "empleado" and password == "empleadopass":
            self.tipo_usuario = "empleado"
            self.dinero_inicial_caja = float(TextInput("Por favor, ingresa el efectivo inicial en caja: $"))
            self.result_label.text = "Iniciaste sesión como empleado."
        else:
            self.result_label.text = "Credenciales incorrectas. Inténtalo de nuevo."

    # Función para agregar un producto
    def add_product(self, instance):
        if self.tipo_usuario == "admin":
            nombre = TextInput("Nombre del producto: ")
            precio = float(TextInput("Precio de venta: "))
            cantidad = int(TextInput("Cantidad en inventario: "))

            producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
            self.productos.append(producto)
            self.result_label.text = f"{nombre} ha sido agregado al inventario."
        else:
            self.result_label.text = "Acceso denegado. Debes ser admin para agregar productos."

    # Función para eliminar un producto
    def delete_product(self, instance):
        if self.tipo_usuario == "admin":
            if not self.productos:
                self.result_label.text = "No hay productos para eliminar."
                return

            self.result_label.text = "Productos disponibles:\n"
            for i, producto in enumerate(self.productos):
                self.result_label.text += f"{i + 1}. {producto['nombre']}\n"

            choice = int(TextInput("Selecciona el número del producto que deseas eliminar: ")) - 1

            if 0 <= choice < len(self.productos):
                producto_eliminado = self.productos.pop(choice)
                self.result_label.text = f"{producto_eliminado['nombre']} ha sido eliminado del inventario."
            else:
                self.result_label.text = "Selección inválida."
        else:
            self.result_label.text = "Acceso denegado. Debes ser admin para eliminar productos."

    # Función para modificar un producto
    def modify_product(self, instance):
        if self.tipo_usuario == "admin":
            if not self.productos:
                self.result_label.text = "No hay productos para modificar."
                return

            self.result_label.text = "Productos disponibles:\n"
            for i, producto in enumerate(self.productos):
                self.result_label.text += f"{i + 1}. {producto['nombre']}\n"

            choice = int(TextInput("Selecciona el número del producto que deseas modificar: ")) - 1

            if 0 <= choice < len(self.productos):
                producto = self.productos[choice]
                self.result_label.text = "Datos actuales del producto:\n"
                self.result_label.text += f"Nombre: {producto['nombre']}\n"
                self.result_label.text += f"Precio de venta: {producto['precio']}\n"
                self.result_label.text += f"Cantidad en inventario: {producto['cantidad']}\n"

                nombre = TextInput("Nuevo nombre (dejar en blanco para no cambiar): ")
                if nombre:
                    producto['nombre'] = nombre

                precio = TextInput("Nuevo precio de venta (dejar en blanco para no cambiar): ")
                if precio:
                    producto['precio'] = float(precio)

                cantidad = TextInput("Nueva cantidad en inventario (dejar en blanco para no cambiar): ")
                if cantidad:
                    producto['cantidad'] = int(cantidad)

                self.result_label.text = f"{producto['nombre']} ha sido modificado en el inventario."
            else:
                self.result_label.text = "Selección inválida."
        else:
            self.result_label.text = "Acceso denegado. Debes ser admin para modificar productos."

    # Función para la sección de caja de cobro
    def cashier(self, instance):
        caja = []

        while True:
            self.result_label.text = "\nOpciones de caja de cobro:\n1. Agregar producto a la caja\n2. Eliminar producto de la caja\n3. Hacer corte de caja\n4. Cobrar productos y volver a la caja\n5. Salir de la caja"

            opcion = TextInput("Selecciona una opción: ")

            if opcion == "1":
                self.result_label.text = "Productos disponibles:\n"
                for i, producto in enumerate(self.productos):
                    self.result_label.text += f"{i + 1}. {producto['nombre']} - ${producto['precio']}\n"

                choice = int(TextInput("Selecciona el número del producto que deseas agregar a la caja: ")) - 1

                if 0 <= choice < len(self.productos):
                    producto = self.productos[choice]
                    caja.append(producto)
                    self.result_label.text = f"{producto['nombre']} ha sido agregado a la caja."
                else:
                    self.result_label.text = "Selección inválida."
            elif opcion == "2":
                if not caja:
                    self.result_label.text = "La caja está vacía."
                else:
                    self.result_label.text = "Productos en la caja:\n"
                    for i, producto in enumerate(caja):
                        self.result_label.text += f"{i + 1}. {producto['nombre']} - ${producto['precio']}\n"
                    choice = int(TextInput("Selecciona el número del producto que deseas eliminar de la caja: ")) - 1
                    if 0 <= choice < len(caja):
                        producto_eliminado = caja.pop(choice)
                        self.result_label.text = f"{producto_eliminado['nombre']} ha sido eliminado de la caja."
                    else:
                        self.result_label.text = "Selección inválida."
            elif opcion == "3":
                total_ventas = self.mostrar_ventas_dia(self.ventas)  # Debes implementar mostrar_ventas_dia()
                dinero_en_caja = float(TextInput("Ingrese la cantidad de dinero en caja: $"))
                diferencia = dinero_en_caja - self.dinero_inicial_caja - total_ventas
                self.result_label.text = f"Diferencia entre caja y ventas: ${diferencia:.2f}"
            elif opcion == "4":
                if not caja:
                    self.result_label.text = "La caja está vacía. No se puede realizar el cobro."
                else:
                    total_venta, metodo_pago = self.cobrar(caja)  # Debes implementar la función cobrar()
                    self.guardar_venta(total_venta, metodo_pago, caja)  # Debes implementar guardar_venta()
                    self.total_ventas += total_venta  # Actualizar el dinero total de las ventas
                    caja = []  # Limpiar la caja después del cobro
                    self.result_label.text = f"Venta realizada por un total de ${total_venta:.2f} con {metodo_pago}."
            elif opcion == "5":
                break
            else:
                self.result_label.text = "Opción inválida."

    # Función para mostrar las ventas del día
    def mostrar_ventas_dia(self, ventas):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        self.sales_label.text = f"Ventas del día ({fecha_actual}):\n"
        ventas_del_dia = self.cargar_ventas(fecha_actual)

        if not ventas_del_dia:
            self.sales_label.text += "No hay ventas registradas para el día de hoy."
            return

        total_ventas_dia = sum(venta[3] for venta in ventas_del_dia)  # Calcula el total de las ventas del día

        for venta in ventas_del_dia:
            self.sales_label.text += f"ID Venta: {venta[1]}\n"
            self.sales_label.text += f"Productos: {venta[2]}\n"
            self.sales_label.text += f"Total Venta: ${venta[3]}\n"
            self.sales_label.text += f"Método de Pago: {venta[4]}\n\n"

        self.sales_label.text += f"Dinero total de las ventas: ${total_ventas_dia:.2f}"

        return total_ventas_dia  # Devuelve el total de las ventas del día

    # Función para cargar las ventas de una fecha específica
    def cargar_ventas(self, fecha):
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
    def guardar_venta(self, total, metodo_pago, caja):
        if not caja:
            self.result_label.text = "No se puede guardar una venta vacía."
            return

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        archivo_ventas = f"ventas_totales.xlsx"

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

        self.ventas.append(nueva_fila)  # Agregar la venta al registro de ventas

if __name__ == "__main__":
    InventoryApp().run()
