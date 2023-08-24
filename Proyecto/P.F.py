import sqlite3
import tkinter as tk
from tkinter import messagebox

# Crear o conectar a la base de datos
conn = sqlite3.connect('supermercado.db')
cursor = conn.cursor()

# Crear tabla de productos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
''')

# Crear tabla de usuarios con algunos usuarios de ejemplo
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        contrasena TEXT NOT NULL,
        rol TEXT NOT NULL
    )
''')

# Agregar algunos usuarios de ejemplo
usuarios_ejemplo = [
    ('Yerik', 'c1', 'vendedor'),
    ('Fernanda', 'c2', 'vendedor'),
    ('Josue', 'c3', 'comprador'),
    ('Nathan', 'c4', 'comprador'),
]

cursor.executemany('INSERT INTO usuarios (nombre, contrasena, rol) VALUES (?, ?, ?)', usuarios_ejemplo)
conn.commit()



# Función para agregar nuevos productos (solo accesible para vendedores)
def agregar_producto():

    if usuario_actual.get("1.0", tk.END).strip() != "vendedor":
        messagebox.showerror("Error", "No tiene permisos para agregar productos.")
        return

    nombre = entry_nombre.get()
    precio = float(entry_precio.get())
    cursor.execute('INSERT INTO productos (nombre, precio) VALUES (?, ?)', (nombre, precio))
    conn.commit()
    messagebox.showinfo("Aviso", f"Producto '{nombre}' agregado con precio {precio}.")
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# Función para generar una factura
def generar_factura():
    producto = entry_producto.get()
    cursor.execute('SELECT nombre, precio FROM productos WHERE nombre = ?', (producto,))
    result = cursor.fetchone()
    if result:
        nombre, precio = result
        Iva= precio * 0.19 
        Total = Iva + precio
        factura_text.delete("1.0", tk.END)
        factura_text.insert(tk.END, f"Factura:\nProducto: {nombre}\nPrecio: {precio} \nIva: {Iva}\nPrecio con Iva: {Total}")
    else:
        messagebox.showerror("Error", f"Producto '{producto}' no encontrado en la base de datos.")


# Función para verificar las credenciales del usuario y cambiar la página
def verificar_credenciales():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Aquí deberías tener una lógica para verificar las credenciales del usuario en la base de datos de usuarios
    # Para este ejemplo, asumiremos que tenemos una tabla "usuarios" con los campos "nombre", "contrasena" y "rol"
    cursor.execute('SELECT rol FROM usuarios WHERE nombre = ? AND contrasena = ?', (usuario, contrasena))
    result = cursor.fetchone()

    if result:
        
        rol = result[0]
        usuario_actual.delete("1.0", tk.END)
        usuario_actual.insert(tk.END, rol)
        entry_usuario.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)
        label_rol = tk.Label(pagina_inicio, text="Usted inicio sesion como un:")
        label_rol.pack()

        if rol == "vendedor":
            mostrar_pagina_vendedor()
        elif rol == "comprador":
            mostrar_pagina_comprador()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Función para mostrar la página del vendedor
def mostrar_pagina_vendedor():
    
    usuario_actual.pack()
    pagina_comprador.pack_forget()
    pagina_vendedor.pack()
    factura_text.pack_forget()


# Función para mostrar la página del comprador
def mostrar_pagina_comprador():

    usuario_actual.pack()
    pagina_vendedor.pack_forget()
    pagina_comprador.pack()
    factura_text.pack()

# Crear o conectar a la base de datos
conn = sqlite3.connect('supermercado.db')
cursor = conn.cursor()

# Crear tabla de productos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
''')
conn.commit()

# Crear ventana principal
window = tk.Tk()
window.title("Supermercado")
usuario_actual = tk.Text(window, height=1, width=10)

# Página de inicio de sesión
pagina_inicio = tk.Frame(window)


label_usuario = tk.Label(pagina_inicio, text="Usuario:")
entry_usuario = tk.Entry(pagina_inicio)
label_contrasena = tk.Label(pagina_inicio, text="Contraseña:")
entry_contrasena = tk.Entry(pagina_inicio, show="*")
btn_iniciar_sesion = tk.Button(pagina_inicio, text="Iniciar Sesión", command=verificar_credenciales)

label_usuario.pack()
entry_usuario.pack()
label_contrasena.pack()
entry_contrasena.pack()
btn_iniciar_sesion.pack()

# Página del vendedor
pagina_vendedor = tk.Frame(window)

label_nombre = tk.Label(pagina_vendedor, text="Nombre del producto:")
entry_nombre = tk.Entry(pagina_vendedor)
label_precio = tk.Label(pagina_vendedor, text="Precio:")
entry_precio = tk.Entry(pagina_vendedor)
btn_agregar = tk.Button(pagina_vendedor, text="Agregar Producto", command=agregar_producto)

label_nombre.pack()
entry_nombre.pack()
label_precio.pack()
entry_precio.pack()
btn_agregar.pack()

# Página del comprador
pagina_comprador = tk.Frame(window)



label_producto = tk.Label(pagina_comprador, text="Nombre del producto a comprar:")
entry_producto = tk.Entry(pagina_comprador)
btn_factura = tk.Button(pagina_comprador, text="Generar Factura", command=generar_factura)

label_producto.pack()
entry_producto.pack()
btn_factura.pack()

# Área para mostrar el rol del usuario actual


# Área para mostrar la factura generada
factura_text = tk.Text(window, height=5, width=30)


pagina_inicio.pack()
pagina_vendedor.pack_forget()
pagina_comprador.pack_forget()
factura_text.pack_forget()
window.mainloop()