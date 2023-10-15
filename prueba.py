from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import openpyxl
import os
import getpass
from datetime import datetime

class ProductManager(App):
    def __init__(self, **kwargs):
        super(ProductManager, self).__init__(**kwargs)
        self.products = []
        self.total_sales = 0
        self.registered_products = []
        self.dinero_inicial_caja = 0
        self.user_type = None

    def build(self):
        self.title = 'Sistema de Gestión de Productos'
        self.layout = BoxLayout(orientation='vertical')
        self.status_label = Label(text="Inicia sesión para continuar")
        self.layout.add_widget(self.status_label)
        self.username_input = TextInput(hint_text="Nombre de usuario")
        self.password_input = TextInput(hint_text="Contraseña", password=True)
        login_button = Button(text="Iniciar Sesión")
        login_button.bind(on_release=self.login)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(login_button)
        return self.layout

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username == "admin" and password == "adminpass":
            self.user_type = "admin"
            self.show_admin_interface()
        elif username == "empleado" and password == "empleadopass":
            self.user_type = "empleado"
            self.show_employee_interface()
        else:
            self.show_error_popup("Credenciales incorrectas. Inténtalo de nuevo.")

    def show_admin_interface(self):
        self.layout.clear_widgets()
        self.admin_layout = BoxLayout(orientation='vertical')
        self.admin_layout.add_widget(Label(text="Panel de Administrador"))
        add_product_button = Button(text="Agregar Producto")
        add_product_button.bind(on_release=self.add_product)
        self.admin_layout.add_widget(add_product_button)
        remove_product_button = Button(text="Eliminar Producto")
        remove_product_button.bind(on_release=self.remove_product)
        self.admin_layout.add_widget(remove_product_button)
        modify_product_button = Button(text="Modificar Producto")
        modify_product_button.bind(on_release=self.modify_product)
        self.admin_layout.add_widget(modify_product_button)
        cash_register_button = Button(text="Caja de Cobro")
        cash_register_button.bind(on_release=self.cash_register)
        self.admin_layout.add_widget(cash_register_button)
        logout_button = Button(text="Cerrar Sesión")
        logout_button.bind(on_release=self.logout)
        self.admin_layout.add_widget(logout_button)
        self.layout.add_widget(self.admin_layout)

    def show_employee_interface(self):
        self.layout.clear_widgets()
        self.employee_layout = BoxLayout(orientation='vertical')
        self.employee_layout.add_widget(Label(text="Panel de Empleado"))
        cash_register_button = Button(text="Caja de Cobro")
        cash_register_button.bind(on_release=self.cash_register)
        self.employee_layout.add_widget(cash_register_button)
        logout_button = Button(text="Cerrar Sesión")
        logout_button.bind(on_release=self.logout)
        self.employee_layout.add_widget(logout_button)
        self.layout.add_widget(self.employee_layout)

    def add_product(self, instance):
        popup = Popup(title='Agregar Producto', auto_dismiss=False, size_hint=(0.4, 0.5))
        content = BoxLayout(orientation='vertical')
        name_input = TextInput(hint_text='Nombre del producto')
        price_input = TextInput(hint_text='Precio de venta')
        quantity_input = TextInput(hint_text='Cantidad en inventario')
        add_button = Button(text='Agregar')
        add_button.bind(on_release=lambda x: self.confirm_add_product(popup, name_input.text, price_input.text, quantity_input.text))
        cancel_button = Button(text='Cancelar')
        cancel_button.bind(on_release=popup.dismiss)
        content.add_widget(name_input)
        content.add_widget(price_input)
        content.add_widget(quantity_input)
        content.add_widget(add_button)
        content.add_widget(cancel_button)
        popup.content = content
        popup.open()

    def confirm_add_product(self, popup, name, price, quantity):
        if name and price and quantity:
            product = {"nombre": name, "precio": float(price), "cantidad": int(quantity)}
            self.products.append(product)
            popup.dismiss()
        else:
            self.show_error_popup("Por favor, completa todos los campos.")


    def remove_product(self, instance):
        if not self.products:
            self.show_error_popup("No hay productos para eliminar.")
        else:
            popup = Popup(title='Eliminar Producto', auto_dismiss=False, size_hint=(0.4, 0.5))
            content = BoxLayout(orientation='vertical')
            product_names = [product["nombre"] for product in self.products]
            product_spinner = Spinner(text=product_names[0], values=product_names)
            remove_button = Button(text='Eliminar')
            remove_button.bind(on_release=lambda x: self.confirm_remove_product(popup, product_spinner.text))
            cancel_button = Button(text='Cancelar')
            cancel_button.bind(on_release=popup.dismiss)
            content.add_widget(product_spinner)
            content.add_widget(remove_button)
            content.add_widget(cancel_button)
            popup.content = content
            popup.open()

    def confirm_remove_product(self, popup, product_name):
        product_to_remove = None
        for product in self.products:
            if product["nombre"] == product_name:
                product_to_remove = product
                break
        if product_to_remove:
            self.products.remove(product_to_remove)
            self.save_products()  # Guardar productos en el archivo
            popup.dismiss()
        else:
            self.show_error_popup("Producto no encontrado.")

    def modify_product(self, instance):
        if not self.products:
            self.show_error_popup("No hay productos para modificar.")
        else:
            popup = Popup(title='Modificar Producto', auto_dismiss=False, size_hint=(0.4, 0.5))
            content = BoxLayout(orientation='vertical')
            product_names = [product["nombre"] for product in self.products]
            product_spinner = Spinner(text=product_names[0], values=product_names)
            modify_button = Button(text='Modificar')
            modify_button.bind(on_release=lambda x: self.confirm_modify_product(popup, product_spinner.text))
            cancel_button = Button(text='Cancelar')
            cancel_button.bind(on_release=popup.dismiss)
            content.add_widget(product_spinner)
            content.add_widget(modify_button)
            content.add_widget(cancel_button)
            popup.content = content
            popup.open()

    def confirm_modify_product(self, popup, product_name):
        for product in self.products:
            if product["nombre"] == product_name:
                self.modify_product_details(product)
                break
        self.save_products()  # Guardar productos en el archivo
        popup.dismiss()

    def modify_product_details(self, product):
        popup = Popup(title='Modificar Detalles', auto_dismiss=False, size_hint=(0.4, 0.5))
        content = BoxLayout(orientation='vertical')
        name_label = Label(text='Nombre del producto: ' + product["nombre"])
        price_input = TextInput(hint_text='Nuevo precio de venta')
        quantity_input = TextInput(hint_text='Nueva cantidad en inventario')
        modify_button = Button(text='Modificar')
        modify_button.bind(on_release=lambda x: self.confirm_modify_details(product, price_input.text, quantity_input.text, popup))
        cancel_button = Button(text='Cancelar')
        cancel_button.bind(on_release=popup.dismiss)
        content.add_widget(name_label)
        content.add_widget(price_input)
        content.add_widget(quantity_input)
        content.add_widget(modify_button)
        content.add_widget(cancel_button)
        popup.content = content
        popup.open()

    def confirm_modify_details(self, product, new_price, new_quantity, popup):
        if new_price:
            product["precio"] = float(new_price)
        if new_quantity:
            product["cantidad"] = int(new_quantity)
        popup.dismiss()

    def cash_register(self, instance):
        popup = Popup(title='Caja de Cobro', auto_dismiss=False, size_hint=(0.6, 0.7))
        content = BoxLayout(orientation='vertical')
        products_in_register = []
        register_total = 0
        product_layout = GridLayout(cols=3, spacing=10, size_hint_y=None)
        product_layout.bind(minimum_height=product_layout.setter('height'))
        for product in self.products:
            product_name = product["nombre"]
            product_price = product["precio"]
            quantity = TextInput(hint_text='0', input_filter='int')
            add_button = Button(text='+')
            add_button.bind(on_release=lambda x, product=product: self.add_to_register(product, quantity.text))
            product_layout.add_widget(Label(text=product_name))
            product_layout.add_widget(Label(text=str(product_price)))
            product_layout.add_widget(quantity)
            product_layout.add_widget(add_button)
        product_scrollview = ScrollView()
        product_scrollview.add_widget(product_layout)
        cash_label = Label(text=f'Total: ${register_total:.2f}')
        complete_sale_button = Button(text='Completar Venta')
        complete_sale_button.bind(on_release=lambda x: self.complete_sale(cash_label, popup))
        cancel_button = Button(text='Cancelar')
        cancel_button.bind(on_release=popup.dismiss)
        content.add_widget(product_scrollview)
        content.add_widget(cash_label)
        content.add_widget(complete_sale_button)
        content.add_widget(cancel_button)
        popup.content = content
        popup.open()

    def add_to_register(self, product, quantity_str):
        if quantity_str:
            quantity = int(quantity_str)
            if quantity > 0 and product["cantidad"] >= quantity:
                product["cantidad"] -= quantity
                self.register_total += product["precio"] * quantity
                self.registered_products.append((product["nombre"], product["precio"], quantity))
                self.show_success_popup(f'{quantity} {product["nombre"]} agregado(s) al registro.')
            else:
                self.show_error_popup('Cantidad no válida o insuficiente en inventario.')
        else:
            self.show_error_popup('Cantidad no válida.')

    def complete_sale(self, cash_label, popup):
        if self.registered_products:
            cash_label.text = f'Total: ${self.register_total:.2f}'
            popup.title = 'Completar Venta'
            cash_label.text = f'Total: ${self.register_total:.2f}'
            cash_input = TextInput(hint_text='Dinero recibido', input_filter='float')
            accept_button = Button(text='Aceptar')
            accept_button.bind(on_release=lambda x: self.accept_sale(cash_input.text, cash_label, popup))
            cancel_button = Button(text='Cancelar')
            cancel_button.bind(on_release=popup.dismiss)
            cash_layout = BoxLayout(orientation='vertical')
            cash_layout.add_widget(cash_input)
            cash_layout.add_widget(accept_button)
            cash_layout.add_widget(cancel_button)
            popup.content = cash_layout
        else:
            self.show_error_popup('No hay productos en el registro.')

    def accept_sale(self, cash_received_str, cash_label, popup):
        if cash_received_str:
            cash_received = float(cash_received_str)
            if cash_received >= self.register_total:
                change = cash_received - self.register_total
                self.total_sales += self.register_total
                self.register_total = 0
                self.registered_products = []
                cash_label.text = f'Cambio: ${change:.2f}'
                popup.title = 'Venta Completada'
                self.show_success_popup(f'Venta completada. Cambio: ${change:.2f}')
            else:
                self.show_error_popup('El dinero recibido es insuficiente.')
        else:
            self.show_error_popup('Cantidad no válida.')

    def show_error_popup(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 150))
        popup.open()

    def show_success_popup(self, message):
        popup = Popup(title='Éxito', content=Label(text=message), size_hint=(None, None), size=(300, 150))
        popup.open()

    def logout(self, instance):
        self.layout.clear_widgets()
        self.build()

if __name__ == '__main__':
    ProductManager().run()
