import customtkinter as ctk
import os
from PIL import Image
import tkinter.messagebox
import sqlite3

#Llamar a la imagen
carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")          

#Apariencia de la ventana
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Login:
    def __init__(self):  
        #Tamaño de la ventana, titulo
        self.root = ctk.CTk()
        self.root.geometry("350x350+500+200")
        self.root.title('Easy Grades')
        self.root.resizable(False, False) 

        self.usuario_entry = None
        self.combo = None 

        #Dar el tamaño
        logo = ctk.CTkImage(  
            dark_image = Image.open(os.path.join(carpeta_imagenes, "usuario.png")),
            size=(100, 100)
        )
        
        #Llamar la imagen a la ventana
        etiqueta = ctk.CTkLabel(master=self.root, image=logo, text="")
        etiqueta.pack(pady=15)

        # Label Usuario
        usuario = ctk.CTkLabel(self.root, text = "Usuario", font = ("Helvetica", 18, "bold"))
        usuario.pack()

        #Para Poder escribir el nombre de usuario
        self.usuario_entry = ctk.CTkEntry(self.root)
        self.usuario_entry.pack(pady = 10)

        #Seleccion entre Profesor y Estudiante
        self.option = ctk.StringVar(value="")
        self.combo = ctk.CTkComboBox(master=self.root, values=["Director", "Profesor", "Estudiante"], variable=self.option)
        self.combo.pack(pady=15)

       # Boton de entrar
        login_button = ctk.CTkButton(self.root, text = "Enter", command = self.seleccion)
        login_button.pack(pady=10)

        self.root.mainloop()

    def mostrar_error_seleccion(self):
        tkinter.messagebox.showerror("Error", "Selecciona una opción válida: 'Profesor' o 'Estudiante'.")

    def verificar_estudiante(self, usuario):
      conn = sqlite3.connect('CURSO.db')
      cursor = conn.cursor()

      cursor.execute("SELECT * FROM Estudiantes WHERE USUARIO=?", (usuario,))
      estudiante = cursor.fetchone()

      conn.close()

      return estudiante is not None
    
    def verificar_profesor(self, usuario): 
        conn = sqlite3.connect('CURSO.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Docentes WHERE NOMBRE=?", (usuario,))
        profesor = cursor.fetchone()

        conn.close()

        return profesor is not None
    
    def verificar_director(self, usuario):
        conn = sqlite3.connect('CURSO.db')
        cursor = conn.cursor()

        cursor.execute("SELECT NOMBRE FROM Director WHERE NOMBRE=?", (usuario,))
        director = cursor.fetchone()

        conn.close()

        return director is not None

    def redirigir_ventana(self, ventana_clase, usuario):
        self.root.destroy()
        ventana_clase(usuario)

    def seleccion(self):
        usuario = self.usuario_entry.get()
        seleccionado = self.combo.get()
        
        if usuario and seleccionado:
            if seleccionado == "Profesor":
                if self.verificar_profesor(usuario):
                   self.root.destroy()
                   Profesor(usuario)
                else:
                   self.mostrar_error_seleccion()
                   tkinter.messagebox.showerror("Error", "El nombre de profesor ingresado es inválido.")
            elif seleccionado == "Estudiante":
                if self.verificar_estudiante(usuario):
                   self.root.destroy()
                   Estudiante(usuario)
                else:
                   self.mostrar_error_seleccion()
                   tkinter.messagebox.showerror("Error", "El nombre de estudiante ingresado es inválido.")
            elif seleccionado == "Director":
                if self.verificar_director(usuario):
                   self.root.destroy()    
                   Director(usuario)  
                else:
                   tkinter.messagebox.showerror("Error", "El nombre de director ingresado es inválido.")
                   self.mostrar_error_seleccion()   
            else:
                self.mostrar_error_seleccion()
        else:
            tkinter.messagebox.showerror("Error", "Por favor, ingrese un nombre de usuario y seleccione una opción")

class Estudiante:
    def __init__(self, usuario):
        conn = sqlite3.connect('CURSO.db')
        cursor_sql = conn.cursor()

        # Obtener las notas del estudiante desde la base de datos (código faltante)
        cursor_sql.execute("SELECT MATEMATICAS, ESPANOL, CIENCIAS, ESTUDIOS, CONDUCTA FROM Estudiantes WHERE USUARIO=?", (usuario,))
        notas_estudiante = cursor_sql.fetchone()

        conn.commit()
        conn.close()
        #Tamaño de la ventana, titulo
        self.root = ctk.CTk()
        self.root.geometry("350x350+500+200")
        self.root.title(f'Estudiante - {usuario}')
        self.root.resizable(False, False) 

        #Dar el tamaño
        logo = ctk.CTkImage(  
            light_image = Image.open(os.path.join(carpeta_imagenes, "book.png")),
            size=(80, 80)
        )

        #Llamar la imagen a la ventana
        etiqueta = ctk.CTkLabel(master = self.root, image = logo, text = "")
        etiqueta.pack(pady = 15)

        atras = ctk.CTkButton(self.root, text="<", width=5, command=self.back)
        atras.place(x=10, y=10)

        # Crear etiquetas para las notas y el promedio
        self.nota_mate_label = ctk.CTkLabel(self.root, text=f"Matemática:              {notas_estudiante[0]}", font=("Helvetica", 18))
        self.nota_mate_label.place(x=70, y=95)

        self.nota_espanol_label = ctk.CTkLabel(self.root, text=f"Español:                   {notas_estudiante[1]}", font=("Helvetica", 18))
        self.nota_espanol_label.place(x=70, y=145)

        self.nota_sociales_label = ctk.CTkLabel(self.root, text=f"Ciencias:                  {notas_estudiante[3]}", font=("Helvetica", 18))
        self.nota_sociales_label.place(x=70, y=245)

        self.nota_ciencias_label = ctk.CTkLabel(self.root, text=f"Estudios Sociales:    {notas_estudiante[2]}", font=("Helvetica", 18))
        self.nota_ciencias_label.place(x=70, y=195)

        self.promedio_label = ctk.CTkLabel(self.root, text=f"Promedio:                 {notas_estudiante[4]}", font=("Helvetica", 18))
        self.promedio_label.place(x=70, y=295)

        self.root.mainloop()

    def back(self):
        self.root.destroy()
        Login()

class Profesor:
    def __init__(self, usuario):    
        #Tamaño de la ventana, titulo
        self.root = ctk.CTk()
        self.root.geometry("350x350+500+200")
        self.root.title(f'Profesor - {usuario}')
        self.root.resizable(False, False) 

        self.usuario = usuario
        self.materia_profesor = self.verificar_materia_profesor()

        #Dar el tamaño
        logo = ctk.CTkImage(  
            light_image = Image.open(os.path.join(carpeta_imagenes, "profe.png")),
            size=(70, 70)
        )

        #Llamar la imagen a la ventana
        etiqueta = ctk.CTkLabel(master = self.root, image = logo, text = "")
        etiqueta.pack(pady = 15)

        atras = ctk.CTkButton(self.root, text="<", width=5, command=self.back)
        atras.place(x=15, y=10)
        
        option = ctk.StringVar(value = "")
        self.combo = ctk.CTkComboBox(master=self.root, values=self.obtener_nombres_estudiantes(), variable=option)
        self.combo.place(x=35, y=305)

        #Boton para mostrar los datos
        look_button = ctk.CTkButton(self.root, text = "Look For", width = 10, command=self.mostrar_notas) 
        look_button.place(x = 185, y = 305)

        #Materias
        materia1 = ctk.CTkLabel(self.root, text = "Matematica", font = ("Helvetica", 16, "bold"))
        materia1.place(x = 35, y = 105)

        self.materia1_entry = ctk.CTkEntry(self.root, width = 65)
        self.materia1_entry.place(x = 185, y = 105)

        materia2 = ctk.CTkLabel(self.root, text ="Español", font = ("Helvetica", 16, "bold"))
        materia2.place(x = 35, y = 145)

        self.materia2_entry = ctk.CTkEntry(self.root, width = 65)
        self.materia2_entry.place(x = 185, y = 145)

        materia3 = ctk.CTkLabel(self.root, text = "Ciencias", font = ("Helvetica", 16, "bold"))
        materia3.place(x = 35, y = 185)

        self.materia3_entry = ctk.CTkEntry(self.root, width = 65)
        self.materia3_entry.place(x = 185, y = 185)

        materia4 = ctk.CTkLabel(self.root, text = "Estudios Sociales", font = ("Helvetica", 16, "bold"))
        materia4.place(x = 35, y = 225)

        self.materia4_entry = ctk.CTkEntry(self.root, width = 65)
        self.materia4_entry.place(x = 185, y = 225)

        promedio = ctk.CTkLabel(self.root, text = "Promedio", font = ("Helvetica", 16, "bold"))
        promedio.place(x = 35, y = 265)

        self.promedio_entry = ctk.CTkEntry(self.root, width = 65)
        self.promedio_entry.place(x = 185, y = 265)

        #Boton para guardar los cambios
        save_button = ctk.CTkButton(self.root, text = "Save", width = 55, command=self.guardar_cambios)
        save_button.place(x = 265, y = 305)

        self.root.mainloop() 

    def obtener_nombres_estudiantes(self):
        conn = sqlite3.connect('CURSO.db')
        cursor = conn.cursor()
        cursor.execute("SELECT USUARIO FROM Estudiantes")
        estudiantes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return estudiantes
     
    def mostrar_notas(self):
        estudiante_seleccionado = self.combo.get()

        materia_profesor = self.verificar_materia_profesor()

        conn = sqlite3.connect('CURSO.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MATEMATICAS, ESPANOL, CIENCIAS, ESTUDIOS, CONDUCTA FROM Estudiantes WHERE USUARIO=?", (estudiante_seleccionado,))
        notas_estudiante = cursor.fetchone()
        conn.close()

        self.materia1_entry.delete(0, "end")
        self.materia1_entry.insert(0, str(notas_estudiante[0]))

        self.materia2_entry.delete(0, "end")
        self.materia2_entry.insert(0, str(notas_estudiante[1]))

        self.materia3_entry.delete(0, "end")
        self.materia3_entry.insert(0, str(notas_estudiante[2]))

        self.materia4_entry.delete(0, "end")
        self.materia4_entry.insert(0, str(notas_estudiante[3]))

        self.promedio_entry.delete(0, "end")
        self.promedio_entry.insert(0, str(notas_estudiante[4]))

        # Habilita o deshabilita la edición del Entry correspondiente a la materia del profesor
        if materia_profesor == "Matematicas":
            self.materia1_entry.configure(state="normal")
            self.materia2_entry.configure(state="disabled")
            self.materia3_entry.configure(state="disabled")
            self.materia4_entry.configure(state="disabled")
            self.promedio_entry.configure(state="disabled")
        elif materia_profesor == "Espanol":
            self.materia1_entry.configure(state="disabled")
            self.materia2_entry.configure(state="normal")
            self.materia3_entry.configure(state="disabled")
            self.materia4_entry.configure(state="disabled")
            self.promedio_entry.configure(state="disabled")
        elif materia_profesor == "Ciencias":
            self.materia1_entry.configure(state="disabled")
            self.materia2_entry.configure(state="disabled")
            self.materia3_entry.configure(state="normal")
            self.materia4_entry.configure(state="disabled")
            self.promedio_entry.configure(state="disabled")
        elif materia_profesor == "Estudios":
            self.materia1_entry.configure(state="disabled")
            self.materia2_entry.configure(state="disabled")
            self.materia3_entry.configure(state="disabled")
            self.materia4_entry.configure(state="normal")
            self.promedio_entry.configure(state="disabled")
        elif self.materia_profesor == "Guia":
            self.materia1_entry.configure(state="normal")
            self.materia2_entry.configure(state="normal")
            self.materia3_entry.configure(state="normal")
            self.materia4_entry.configure(state="normal")
            self.promedio_entry.configure(state="normal")

    def guardar_cambios(self):
        estudiante_seleccionado = self.combo.get()

        nota_mate = self.materia1_entry.get()
        nota_espanol = self.materia2_entry.get()
        nota_ciencias = self.materia3_entry.get()
        nota_sociales = self.materia4_entry.get()
        promedio = self.promedio_entry.get()

        if self.materia_profesor == "Matematicas":
            conn = sqlite3.connect('CURSO.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Estudiantes SET MATEMATICAS=? WHERE USUARIO=?", (nota_mate, estudiante_seleccionado))
            conn.commit()
            conn.close()
            tkinter.messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        elif self.materia_profesor == "Espanol":
            conn = sqlite3.connect('CURSO.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Estudiantes SET ESPANOL=? WHERE USUARIO=?", (nota_espanol, estudiante_seleccionado))
            conn.commit()
            conn.close()
            tkinter.messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        elif self.materia_profesor == "Ciencias":
            conn = sqlite3.connect('CURSO.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Estudiantes SET CIENCIAS=? WHERE USUARIO=?", (nota_ciencias, estudiante_seleccionado))
            conn.commit()
            conn.close()
            tkinter.messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        elif self.materia_profesor == "Estudios":
            conn = sqlite3.connect('CURSO.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Estudiantes SET ESTUDIOS=? WHERE USUARIO=?", (nota_sociales, estudiante_seleccionado))
            conn.commit()
            conn.close()
            tkinter.messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        elif self.materia_profesor == "Guia":
            conn = sqlite3.connect('CURSO.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Estudiantes SET MATEMATICAS=?, ESPANOL=?, CIENCIAS=?, ESTUDIOS=?, CONDUCTA=? WHERE USUARIO=?", (nota_mate, nota_espanol, nota_ciencias, nota_sociales, promedio, estudiante_seleccionado))
            conn.commit()
            conn.close()
            tkinter.messagebox.showinfo("Éxito", "Cambios guardados correctamente.")
        else:
            tkinter.messagebox.showerror("Error", "No tienes permiso para modificar la nota de esta materia")

    def verificar_materia_profesor(self):
        conn = sqlite3.connect('CURSO.db')
        cursor = conn.cursor()

        cursor.execute("SELECT MATERIA FROM Docentes WHERE NOMBRE=?", (self.usuario,))
        materia = cursor.fetchone()[0]  # Obtenemos el valor de la primera columna
        conn.close()

        return materia
    
    def back(self):
        self.root.destroy()
        Login()

class Director:
    def __init__(self, usuario):
        self.root = ctk.CTk()
        self.root.geometry("350x350+500+200")
        self.root.title(f'Director - {usuario}')
        self.root.resizable(False, False)

        logo = ctk.CTkImage(  
            light_image = Image.open(os.path.join(carpeta_imagenes, "tie.png")),
            size=(80, 80)
        )

        #Llamar la imagen a la ventana
        etiqueta = ctk.CTkLabel(master = self.root, image = logo, text = "")
        etiqueta.pack(pady = 10)

        atras = ctk.CTkButton(self.root, text="<", width=5, command=self.back)
        atras.place(x=15, y=10)

        self.nombre = ctk.CTkLabel(self.root, text = "Ingrese el nombre ", font = ("Helvetica", 16, "bold"))
        self.nombre.place(x=25, y=105)

        # Crear Entry para ingresar el nombre
        self.nombre_entry = ctk.CTkEntry(self.root)
        self.nombre_entry.place(x=195, y=105)

        self.materia = ctk.CTkLabel(self.root, text="Ingrese la materia", font=("Helvetica", 16, "bold"))
        self.materia.place(x=25, y=165)

        # Crear Entry para ingresar la materia
        self.materia_entry = ctk.CTkEntry(self.root)
        self.materia_entry.place(x=195, y=165)

        self.option = ctk.StringVar(value="")
        self.combo = ctk.CTkComboBox(master=self.root, values=["Profesor", "Estudiante"], variable=self.option)
        self.combo.place(x=195, y=225)

        # Crear botón para ejecutar la acción de agregar
        add_button = ctk.CTkButton(self.root, text="Add", command=self.agregar)
        add_button.place(x=195, y=285)

        # Crear botón para ejecutar la acción de eliminar
        delete_button = ctk.CTkButton(self.root, text="Delete", command=self.eliminar)
        delete_button.place(x=25, y=285)

        self.root.mainloop()

    def agregar(self):
        seleccionado = self.option.get()
        nombre = self.nombre_entry.get()
        materia = self.materia_entry.get()

        if seleccionado == "Profesor":
            conn = sqlite3.connect('CURSO.db')
            cursor_sql = conn.cursor()
            
            # Insertar el nombre del profesor en la tabla Docentes
            cursor_sql.execute("INSERT INTO Docentes (NOMBRE, MATERIA) VALUES (?, ?)", (nombre, materia))
            conn.commit()
            conn.close()
            
            tkinter.messagebox.showinfo("Éxito", "Profesor agregado correctamente.")
        elif seleccionado == "Estudiante":
            conn = sqlite3.connect('CURSO.db')
            cursor_sql = conn.cursor()
            
            # Insertar el nombre del estudiante en la tabla Estudiantes
            cursor_sql.execute("INSERT INTO Estudiantes (USUARIO) VALUES (?)", (nombre,))
            conn.commit()
            conn.close()
            
            tkinter.messagebox.showinfo("Éxito", "Estudiante agregado correctamente.")
        else:
            tkinter.messagebox.showerror("Error", "Selecciona una opción válida: 'Profesor' o 'Estudiante'.")

    def eliminar(self):
        seleccionado = self.option.get()
        nombre = self.nombre_entry.get()

        if seleccionado == "Profesor":
            conn = sqlite3.connect('CURSO.db')
            cursor_sql = conn.cursor()
            
            # Eliminar al profesor de la tabla Docentes
            cursor_sql.execute("DELETE FROM Docentes WHERE NOMBRE=?", (nombre,))
            conn.commit()
            conn.close()
            
            tkinter.messagebox.showinfo("Éxito", "Profesor eliminado correctamente.")
        elif seleccionado == "Estudiante":
            conn = sqlite3.connect('CURSO.db')
            cursor_sql = conn.cursor()
            
            # Eliminar al estudiante de la tabla Estudiantes
            cursor_sql.execute("DELETE FROM Estudiantes WHERE USUARIO=?", (nombre,))
            conn.commit()
            conn.close()
            
            tkinter.messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
        else:
            tkinter.messagebox.showerror("Error", "Selecciona una opción válida: 'Profesor' o 'Estudiante'.")

    def back(self):
        self.root.destroy()
        Login()