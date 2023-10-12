import getpass
import openpyxl

# Función para el inicio de sesión
def login():
    print("Por favor, inicia sesión:")
    username = input("Nombre de usuario: ")
    password = getpass.getpass("Contraseña: ")

    # Verifica si es el administrador o un empleado
    if username == "admin" and password == "adminpass":
        return "admin"
    elif username == "empleado" and password == "empleadopass":
        return "empleado"
    else:
        print("Credenciales incorrectas. Inténtalo de nuevo.")
        return None

# Función para agregar un producto
def agregar_producto(productos):
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio de venta: "))
    cantidad = int(input("Cantidad en inventario: "))

    producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
    productos.append(producto)

    print(f"{nombre} ha sido agregado al inventario.")

# Función para eliminar un producto
def eliminar_producto(productos):
    print("Productos disponibles:")
    for i, producto in enumerate(productos):
        print(f"{i + 1}. {producto['nombre']}")

    choice = int(input("Selecciona el número del producto que deseas eliminar: ") - 1)


    if 0 <= choice < len(productos):
        producto_eliminado = productos.pop(choice)
        print(f"{producto_eliminado['nombre']} ha sido eliminado del inventario.")
    else:
        print("Selección inválida.")

# Función para modificar un producto
def modificar_producto(productos):
    print("Productos disponibles:")
    for i, producto in enumerate(productos):
        print(f"{i + 1}. {producto['nombre']}")

    choice = int(input("Selecciona el número del producto que deseas modificar: ") - 1)

    if 0 <= choice < len(productos):
        producto = productos[choice]
        print("Datos actuales del producto:")
        print(f"Nombre: {producto['nombre']}")
        print(f"Precio de venta: {producto['precio']}")
        print(f"Cantidad en inventario: {producto['cantidad']}")

        nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ")
        if nombre:
            producto['nombre'] = nombre

        precio = input("Nuevo precio de venta (dejar en blanco para no cambiar): ")
        if precio:
            producto['precio'] = float(precio)

        cantidad = input("Nueva cantidad en inventario (dejar en blanco para no cambiar): ")
        if cantidad:
            producto['cantidad'] = int(cantidad)

        print(f"{producto['nombre']} ha sido modificado en el inventario.")
    else:
        print("Selección inválida.")

# Función para guardar los productos en un archivo Excel
def guardar_productos(productos):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Encabezados
    sheet.append(["Nombre", "Precio de Venta", "Cantidad en Inventario"])

    # Agrega los productos al archivo Excel
    for producto in productos:
        sheet.append(producto["nombre"], producto["precio"], producto["cantidad"])

    workbook.save("productos.xlsx")


if __name__ == "__main__":
    tipo_usuario = login()
    if tipo_usuario == "admin":
        productos = []

        while True:
            print("\nOpciones:")
            print("1. Agregar producto")
            print("2. Eliminar producto")
            print("3. Modificar producto")
            print("4. Guardar cambios y salir")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                agregar_producto(productos)
            elif opcion == "2":
                eliminar_producto(productos)
            elif opcion == "3":
                modificar_producto(productos)
            elif opcion == "4":
                guardar_productos(productos)
                break
            else:
                print("Opción inválida.")
    elif tipo_usuario == "empleado":
        print("Bienvenido, empleado. Acceso limitado.")
    else:
        print("Acceso denegado. Hasta luego.")
