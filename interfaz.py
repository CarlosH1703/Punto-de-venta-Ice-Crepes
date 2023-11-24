import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, PhotoImage
import customtkinter as ctk
import customtkinter
from customtkinter import CTkImage
import openpyxl
import os, json, hashlib
from datetime import datetime
from PIL import Image, ImageTk


# Variables globales
productos = []
ventas = []
tipo_usuario = None
dinero_inicial_caja = 0
entry_buscar = None  # Definir aquí para que sea accesible en todo el código
combo_productos = None  # Definir aquí para que sea accesible en todo el código

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
ctk.set_widget_scaling(1.25)

#funcion para centrar las ventanas
def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    x_pos = ventana.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_pos = ventana.winfo_screenheight() // 2 - alto_ventana // 2
    ventana.geometry(f"+{x_pos}+{y_pos}")

def cargar_contraseñas():
    try:
        with open("usuarios.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"admin": cifrar_contrasena("adminpass"), "empleado": cifrar_contrasena("empleadopass")}

def guardar_contraseñas(usuarios):
    with open("usuarios.json", "w") as file:
        json.dump(usuarios, file)

def actualizar_contraseñas(contrasena_admin, contrasena_empleado):
    usuarios = cargar_contraseñas()
    usuarios["admin"] = cifrar_contrasena(contrasena_admin)
    usuarios["empleado"] = cifrar_contrasena(contrasena_empleado)
    guardar_contraseñas(usuarios)
    messagebox.showinfo("Información", "Contraseñas actualizadas correctamente")

def cifrar_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

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

# Ventana de Inicio de Sesión
# Inicio de Sesión
def iniciar_sesion(usuario, contrasena, ventana_login):
    usuarios = cargar_contraseñas()
    contrasena_cifrada = cifrar_contrasena(contrasena)
    if usuario in usuarios and usuarios[usuario] == contrasena_cifrada:
        global tipo_usuario
        tipo_usuario = usuario
        ventana_login.destroy()
        global dinero_inicial_caja
        dinero_inicial_caja = float(simpledialog.askstring("Dinero Inicial", "Por favor, ingresa el efectivo inicial en caja: $"))
        mostrar_ventana_principal()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

   

def ventana_modificar_contrasenas():
    ventana_modificar = ctk.CTkToplevel()
    ventana_modificar.title("Modificar Contraseñas")
    centrar_ventana(ventana_modificar)

    frame = ctk.CTkFrame(ventana_modificar)
    frame.grid(row=0, column=0, sticky=("nsew"))

    ctk.CTkLabel(frame, text="Nueva Contraseña Admin:").grid(row=0, column=0, sticky="w")
    entry_admin = ctk.CTkEntry(frame)
    entry_admin.grid(row=0, column=1, sticky="ew")

    ctk.CTkLabel(frame, text="Nueva Contraseña Empleado:").grid(row=1, column=0, sticky="w")
    entry_empleado = ctk.CTkEntry(frame)
    entry_empleado.grid(row=1, column=1, sticky="ew")

    ctk.CTkButton(frame, text="Actualizar", command=lambda: actualizar_contraseñas(entry_admin.get(), entry_empleado.get())).grid(row=2, column=1, sticky="e")

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

def mostrar_ventana_login():
    global entry_usuario, entry_contrasena
    ventana_login = ctk.CTk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("800x400")

    # Configura el grid de la ventana para que los elementos se expandan proporcionalmente
    ventana_login.grid_columnconfigure(0, weight=2)  # Aumentar para empujar los widgets a la derecha
    ventana_login.grid_columnconfigure(1, weight=0)  # Columna de la línea no se expande
    ventana_login.grid_columnconfigure(2, weight=1)  # Reducir para mover los widgets a la derecha
    ventana_login.grid_rowconfigure(0, weight=1)

    # Frame para la imagen del lado izquierdo
    frame_imagen = ctk.CTkFrame(ventana_login)
    frame_imagen.grid(row=0, column=0, sticky='nsew')
    frame_imagen.grid_rowconfigure(0, weight=1)
    frame_imagen.grid_columnconfigure(0, weight=1)

    # Cargar y mostrar la imagen
    ruta_imagen = "C:/Users/zoe00/OneDrive/Escritorio/PUNTO DE VENTA ICE & CREPES/Punto-de-venta-Ice-Crepes/imagenes/10222 (1).png"
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((350, 400), Image.Resampling.LANCZOS)
    foto = ImageTk.PhotoImage(imagen)
    label_imagen = ctk.CTkLabel(frame_imagen, image=foto, text="")
    label_imagen.grid(row=0, column=0, sticky='nsew')

    # Canvas para la línea divisoria
    canvas = ctk.CTkCanvas(ventana_login, width=2, height=400)
    canvas.grid(row=0, column=1, sticky="ns")
    canvas.create_line(1, 0, 1, 400, fill="gray")

    # Frame central donde estarán los widgets de login
    frame_central = ctk.CTkFrame(ventana_login)
    frame_central.grid(row=0, column=2, sticky='nsew')
    frame_central.grid_rowconfigure(1, weight=1)
    frame_central.grid_rowconfigure(5, weight=2)
    frame_central.grid_columnconfigure(0, weight=1)
    frame_central.grid_columnconfigure(1, weight=1)

    # Título de la sección de inicio de sesión
    titulo_sesion = ctk.CTkLabel(frame_central, text="Iniciar Sesión", font=("Roboto", 24))
    titulo_sesion.grid(row=1, column=0, columnspan=2, pady=(20, 20))

    # Widgets de login
    ctk.CTkLabel(frame_central, text="Usuario:").grid(row=2, column=0, sticky="e")
    entry_usuario = ctk.CTkEntry(frame_central)
    entry_usuario.grid(row=2, column=1, sticky="w", padx=20)

    ctk.CTkLabel(frame_central, text="Contraseña:").grid(row=3, column=0, sticky="e")
    entry_contrasena = ctk.CTkEntry(frame_central, show="*")
    entry_contrasena.grid(row=3, column=1, sticky="w", padx=20)

    boton_login = ctk.CTkButton(frame_central, text="Iniciar sesión", command=lambda: iniciar_sesion(entry_usuario.get(), entry_contrasena.get(), ventana_login))
    boton_login.grid(row=4, column=0, columnspan=2, pady=10)

    # Para mantener la referencia de la imagen
    label_imagen.image = foto

    ventana_login.mainloop()


# Ventana Principal
def mostrar_ventana_principal():
    ventana_principal = ctk.CTk()
    ventana_principal.title("ADMINISTRADOR")
    ventana_principal.geometry("800x400")  # Ajusta esto si necesitas una ventana de diferente tamaño
    centrar_ventana(ventana_principal)

    # Configura el grid de la ventana para que los elementos se expandan proporcionalmente
    ventana_principal.grid_columnconfigure(0, weight=1)
    ventana_principal.grid_rowconfigure(0, weight=1)

    frame = ctk.CTkFrame(ventana_principal)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure((0, 1), weight=1)
    frame.grid_rowconfigure((0, 1, 2), weight=1)

   # Definición de los iconos para los botones
    iconos = {
        "Agregar Producto": "C:/Users/zoe00/OneDrive/Escritorio/PUNTO DE VENTA ICE & CREPES/Punto-de-venta-Ice-Crepes/imagenes/boton-agregar.png",
        "Eliminar Producto": "C:/Users/zoe00/OneDrive/Escritorio/PUNTO DE VENTA ICE & CREPES/Punto-de-venta-Ice-Crepes/imagenes/contenedor-de-basura.png",
        "Modificar Producto": "C:/Users/zoe00/OneDrive/Escritorio/PUNTO DE VENTA ICE & CREPES/Punto-de-venta-Ice-Crepes/imagenes/editar.png",
        "Modificar Contraseñas": "C:/Users/zoe00/OneDrive/Escritorio/PUNTO DE VENTA ICE & CREPES/Punto-de-venta-Ice-Crepes/imagenes/rueda-dentada.png",
        "Caja de Cobro": "C:/Users/zoe00/OneDrive/Escritorio/PUNTO DE VENTA ICE & CREPES/Punto-de-venta-Ice-Crepes/imagenes/monitor.png",
        "Salir": "C:/Users/zoe00/OneDrive/Escritorio/PUNTO DE VENTA ICE & CREPES/Punto-de-venta-Ice-Crepes/imagenes/cerrar-sesion.png"
    }

    # Define los botones y sus respectivas funciones
    botones_info = [
        ("Agregar Producto", agregar_producto),
        ("Eliminar Producto", eliminar_producto),
        ("Modificar Producto", modificar_producto),
        ("Modificar Contraseñas", ventana_modificar_contrasenas),
        ("Caja de Cobro", lambda: caja_de_cobro(ventana_principal)),
        ("Salir", ventana_principal.destroy)
    ]

    def cargar_icono_redimensionado(ruta, nuevo_ancho, nuevo_alto):
        imagen = Image.open(ruta)
        imagen_redimensionada = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        return ImageTk.PhotoImage(imagen_redimensionada)

    # Carga los iconos para los botones y redimensiona
    tamanio_icono = (50, 50)  # Ejemplo: 50x50 píxeles
    for i, (texto, comando) in enumerate(botones_info):
        ruta_icono = iconos.get(texto, "")
        icono = cargar_icono_redimensionado(ruta_icono, *tamanio_icono)
        boton = ctk.CTkButton(frame, text=texto, command=comando, image=icono, compound="left")
        boton.image = icono  # Guarda una referencia al icono para evitar la recolección de basura
        
        # Posicionamiento y configuración del botón
        fila = i // 2  # Dos botones por fila
        columna = i % 2  # Dos columnas
        boton.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")

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

def caja_de_cobro(ventana_padre):
    caja = []
    ventana_cobro = ctk.CTkToplevel(ventana_padre)
    ventana_cobro.title("Caja de Cobro")
    ventana_cobro.state('zoomed')  # Pantalla completa

    frame = ctk.CTkFrame(ventana_cobro)
    frame.grid(row=0, column=0, sticky="nsew")
    ventana_cobro.grid_rowconfigure(0, weight=1)
    ventana_cobro.grid_columnconfigure(0, weight=1)

    # Buscador de Productos
    ctk.CTkLabel(frame, text="Buscar Producto:").grid(column=0, row=0, sticky=ctk.W)
    entry_buscar = ttk.Entry(frame)
    entry_buscar.grid(column=1, row=0, sticky="ew")
    frame.grid_columnconfigure(1, weight=1)

    # Implementación de la función actualizar_lista_productos
    def actualizar_lista_productos(event):
        busqueda = entry_buscar.get().lower()
        productos_filtrados = [producto for producto in productos if busqueda in producto["nombre"].lower()]
        lista_productos.delete(0, ctk.END)
        for producto in productos_filtrados:
            lista_productos.insert(ctk.END, producto["nombre"])

    entry_buscar.bind('<KeyRelease>', actualizar_lista_productos)

    lista_productos = tk.Listbox(frame)
    lista_productos.grid(column=0, row=1, columnspan=2, sticky="nsew")
    frame.grid_rowconfigure(1, weight=1)

    # Etiqueta para mostrar el costo total
    etiqueta_costo_total = ctk.CTkLabel(frame, text="Costo Total: $0.00")
    etiqueta_costo_total.grid(column=0, row=2, sticky=ctk.W)

    # Lista de Productos en Caja con Enumeración
    lista_caja = tk.Listbox(frame)
    lista_caja.grid(column=0, row=3, columnspan=2, sticky="nsew")
    frame.grid_rowconfigure(3, weight=1)

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

    boton_agregar = ctk.CTkButton(frame, text="Agregar a Caja", command=agregar_a_caja)
    boton_agregar.grid(column=0, row=4, sticky=ctk.E)

    #funcion para eliminar productos de la caja
    def eliminar_de_caja():
        seleccion = lista_caja.curselection()
        if seleccion:
            del caja[seleccion[0]]
            actualizar_lista_caja()
            actualizar_costo_total()

    boton_eliminar = ctk.CTkButton(frame, text="Eliminar de Caja", command=eliminar_de_caja)
    boton_eliminar.grid(column=1, row=4, sticky=ctk.W)

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

    # Funciones de Método de Pago y Corte de Caja
    boton_efectivo = ctk.CTkButton(frame, text="Pagar con Efectivo", command=lambda: realizar_cobro("efectivo"))
    boton_efectivo.grid(column=0, row=5, sticky=ctk.E)

    boton_tarjeta = ctk.CTkButton(frame, text="Pagar con Tarjeta", command=lambda: realizar_cobro("tarjeta"))
    boton_tarjeta.grid(column=1, row=5, sticky=ctk.W)

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

    boton_corte_caja = ctk.CTkButton(frame, text="Corte de Caja", command=corte_de_caja)
    boton_corte_caja.grid(column=1, row=6, sticky=ctk.E)

    frame.grid_rowconfigure(4, weight=0)
    frame.grid_rowconfigure(5, weight=0)
    frame.grid_rowconfigure(6, weight=0)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    ventana_cobro.columnconfigure(0, weight=1)
    ventana_cobro.rowconfigure(1, weight=1)


# Inicio del programa
if __name__ == "__main__":
    cargar_productos()
    mostrar_ventana_login()
