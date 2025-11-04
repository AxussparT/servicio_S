import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from src.conexion import get_conexion
from tkinter import messagebox
from src.UI.ventana_gestion import VentanaGestion

# Asegúrate de que esta importación sea accesible:
from src.clases.profesor import profesor 
# Si el código falla, comenta la línea de arriba y la clase 'profesor' si no está definida.

# --para ejecutar usar python -m servicio_S.src.UI.ventana_principal
    
class VentanaPrincipal:
    
    def __init__(self, master):
        self.master = master
        self.master.title("PLASEM")
        self.master.state('zoomed') 
        db_path = "data/PLASEM.db"
        
        # --- ESTILOS ---
        estilo =ttk.Style()
        estilo.theme_use('clam')
        estilo.configure('blue.TFrame', background='#0A0F1E')
        estilo.configure('Custom.TCheckbutton', font=('Roboto', 16), background='#0A0F1E', foreground='#ffffff')
        estilo.configure('Danger.TButton', font=('Roboto', 15), background='#6D583A', foreground='#000000', padding=10)
        estilo.configure('Treeview.Heading', background='#2f4a23', foreground='#ffffff')
        
        # Estilo para el título del frame de profesores (no estaba definido)
        estilo.configure('fondo.TLabel', background='#0A0F1E', foreground='#ffffff')
        
        # --- Carga de la imagen de fondo ---
        try:
            image = Image.open(r"assets/fondo.png")
            self.original_image = image
            self.background_label = tk.Label(self.master)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.master.bind("<Configure>", self.redimensionar_fondo)
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            self.master.config(bg="grey")
            
        # --- FRAMES PRINCIPALES ---
        # Frame para Profesores
        self.frame_profesores = ttk.Frame(self.master, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_profesores.place(x=140, y=32, width=450, height=700)
        e_profesores=ttk.Label(self.frame_profesores,text="Profesores",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 20), style='fondo.TLabel')
        e_profesores.pack(pady=3,padx=10)
        
        # Frame de Datos del Profesor
        frame_contenedor_datos=ttk.Frame(self.frame_profesores,style='blue.TFrame')
        frame_contenedor_datos.pack(fill='x',pady=10)
        
        self.frame_izq_datos=ttk.Frame(frame_contenedor_datos, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq_datos.pack(side='left',padx=10,anchor='n')
        
        self.frame_der_datos=ttk.Frame(frame_contenedor_datos, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der_datos.pack(side='left',padx=10,anchor='n')
        
        # Entradas de Datos (Todos estos atributos son públicos por usar 'self.')
        ttk.Label(self.frame_izq_datos,text="No. Cuenta",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        self.entry_no_cuenta=ttk.Entry(self.frame_izq_datos,width=20,font=("Roboto", 15)) # Atributo público
        self.entry_no_cuenta.pack(pady=3,padx=10)
        
        ttk.Label(self.frame_izq_datos,text="Nombre:",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10) 
        self.entry_nombre=ttk.Entry(self.frame_izq_datos,width=20,font=("Roboto", 15)) # Atributo público
        self.entry_nombre.pack(pady=3,padx=10)
        
        ttk.Label(self.frame_izq_datos,text="Apellidos:",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        self.entry_apellido=ttk.Entry(self.frame_izq_datos,width=20,font=("Roboto", 15)) # Atributo público
        self.entry_apellido.pack(pady=3,padx=10)
        
        ttk.Label(self.frame_der_datos,text="¿En línea?:",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        self.combo_linea=ttk.Combobox(self.frame_der_datos,width=20,font=("Roboto", 15)) # Atributo público
        self.combo_linea['values']=("Sí","No")
        self.combo_linea.pack(pady=3,padx=10)
        
        ttk.Label(self.frame_der_datos,text="Horario:",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        self.entry_horario_i=ttk.Entry(self.frame_der_datos,width=20,font=("Roboto", 15)) # Atributo público
        self.entry_horario_i.pack(pady=3,padx=10)
        self.entry_horario_f=ttk.Entry(self.frame_der_datos,width=20,font=("Roboto", 15)) # Atributo público
        self.entry_horario_f.pack(pady=3,padx=10)
        
        # Checkbuttons de días de semana
        frame_contenedor=ttk.Frame(self.frame_profesores,style='blue.TFrame')
        frame_contenedor.pack(fill='x',pady=10)
        
        frame_dias=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_dias.pack(side='left',padx=10,anchor='n')
        
        frame_confirmar=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_confirmar.pack(side='left',padx=10,anchor='n')
        
        # CORRECCIÓN 1: Definir las variables como atributos de la clase (self.)
        self.var_lunes = tk.IntVar()
        self.var_martes = tk.IntVar()
        self.var_miercoles = tk.IntVar()
        self.var_jueves = tk.IntVar()
        self.var_viernes = tk.IntVar()
        self.var_sabado = tk.IntVar()

        # La función seleccionar original solo hacía 'print', por lo que no es necesaria
        # como 'command' del checkbutton. El estado se lee al presionar "Confirmar".
        
        ttk.Checkbutton(frame_dias, text="Lunes", variable=self.var_lunes, style='Custom.TCheckbutton').pack(pady=5,padx=5,anchor='w')
        ttk.Checkbutton(frame_dias, text="Martes", variable=self.var_martes, style='Custom.TCheckbutton').pack(pady=5,padx=5,anchor='w')
        ttk.Checkbutton(frame_dias, text="Miércoles", variable=self.var_miercoles, style='Custom.TCheckbutton').pack(pady=5,padx=5,anchor='w')
        ttk.Checkbutton(frame_dias, text="Jueves", variable=self.var_jueves, style='Custom.TCheckbutton').pack(pady=5,padx=5,anchor='w')
        ttk.Checkbutton(frame_dias, text="Viernes", variable=self.var_viernes, style='Custom.TCheckbutton').pack(pady=5,padx=5, anchor='w')
        ttk.Checkbutton(frame_dias, text="Sábado", variable=self.var_sabado, style='Custom.TCheckbutton').pack(pady=5,padx=5, anchor='w')
        
        # --- BOTÓN CORREGIDO ---
        boton_confirmar=ttk.Button(frame_confirmar,text="Confirmar",command=self.evento_boton_profesores,style='Danger.TButton')
        boton_confirmar.pack(pady=5,padx=5,anchor='n')
        
        separador=ttk.Separator(self.frame_profesores,orient='horizontal')
        separador.pack(fill='x',padx=10,pady=10)
        
        # --- TABLA DE PROFESORES ---
        self.frame_tablas=ttk.Frame(self.frame_profesores, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_tablas.pack(pady=10,padx=10)
        columnas=('Cuenta','Profesor','Dias','Horario','¿en linea?')
        self.tabla_profesores=ttk.Treeview(self.frame_tablas, columns=columnas, show='headings')
        self.tabla_profesores.column('Cuenta',anchor='w',width=120)
        self.tabla_profesores.column('Profesor',anchor='w',width=120)
        self.tabla_profesores.column('Dias',anchor='w',width=120)
        self.tabla_profesores.column('Horario',anchor='w',width=120)
        self.tabla_profesores.column('¿en linea?',anchor='w',width=120)
        
        self.tabla_profesores.heading('Cuenta',text='Cuenta')
        self.tabla_profesores.heading('Profesor',text='Profesor')
        self.tabla_profesores.heading('Dias',text='Dias')
        self.tabla_profesores.heading('Horario',text='Horario')
        self.tabla_profesores.heading('¿en linea?',text='¿en linea?')
        
        scrollbar_vertical=ttk.Scrollbar(self.frame_tablas,orient='vertical',command=self.tabla_profesores.yview)
        self.tabla_profesores.configure(yscroll=scrollbar_vertical.set)
        scrollbar_vertical.pack(side='right',fill='y')
        
        scrollbar_horizontal=ttk.Scrollbar(self.frame_tablas,orient='horizontal',command=self.tabla_profesores.xview)
        self.tabla_profesores.configure(xscroll=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side='bottom',fill='x')
        self.tabla_profesores.pack()
        #---MOSTRAR DATOS DEL PROFE EN LA TABLA
        
        # --- PRUEBA Y DEMÁS SECCIONES (MATERIAS Y AULAS) ---
        ttk.Label(self.frame_tablas,text="Apellidos:",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=10,padx=10)

        # Frame para Materias
        self.frame_materias = ttk.Frame(self.master, borderwidth=2, relief="solid", style='blue.TFrame')
        self.frame_materias.place(x=611, y=31, width=650, height=350)
        ttk.Label(self.frame_materias,text="Materias",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 30)).pack(pady=10,padx=10)
        
        frame_contenedor2=ttk.Frame(self.frame_materias,style='blue.TFrame')
        frame_contenedor2.pack(fill='x',pady=10)
        
        frame_izq=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_izq.pack(side='left',padx=10,anchor='n')
        
        frame_derecha=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_derecha.pack(side='left',padx=10,anchor='n')
        
        ttk.Label(frame_izq,text="Clave",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=4,padx=10)
        self.entry_materia_clave=ttk.Entry(frame_izq,width=30,font=("Roboto", 15))
        self.entry_materia_clave.pack(pady=4,padx=10)
        
        ttk.Label(frame_izq,text="Nombre",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=4,padx=10)
        self.entry_materia_nom=ttk.Entry(frame_izq,width=30,font=("Roboto", 15))
        self.entry_materia_nom.pack(pady=4,padx=10)
        
        '''ttk.Label(frame_izq,text="Grupo",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=4,padx=10)
        self.entry_materia_gru=ttk.Entry(frame_izq,width=30,font=("Roboto", 15))
        self.entry_materia_gru.pack(pady=4,padx=10)
        
        ttk.Label(frame_izq,text="Profesor",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=4,padx=10)
        self.combo_profesor=ttk.Combobox(frame_izq,width=30,font=("Roboto", 15))
        self.combo_profesor['values']=("Profesor 1","Profesor 2","Profesor 3")
        self.combo_profesor.pack(pady=4,padx=10)'''
        
        ttk.Label(frame_derecha,text="Horas a la semana",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=4,padx=10)
        self.entry_materia_horas=ttk.Entry(frame_derecha,width=20,font=("Roboto", 15))
        self.entry_materia_horas.pack(pady=4,padx=10)
        
        ttk.Label(frame_derecha,text="Semestre",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=4,padx=10)
        self.entry_materia_semestre=ttk.Entry(frame_derecha,width=20,font=("Roboto", 15))
        self.entry_materia_semestre.pack(pady=4,padx=10)
        
        '''ttk.Label(frame_derecha,text="Salón",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=4,padx=10)
        self.combo_salon=ttk.Combobox(frame_derecha,width=20,font=("Roboto", 15))
        self.combo_salon['values']=("Salón 1","Salón 2","Salón 3")
        self.combo_salon.pack(pady=4,padx=10) '''
        
        boton_confirmar2=ttk.Button(frame_derecha,text="agregar",command=self.evento_materias,style='Danger.TButton')
        boton_confirmar2.pack(pady=4,padx=5,anchor='n')
        
        boton_ventana2=ttk.Button(frame_izq,text="Abrir ventana materias",command=self.abrir_ventana_gestion,style='Danger.TButton')
        boton_ventana2.pack(pady=4,padx=5,anchor='n')
        
        # Frame para Aulas
        self.frame_aulas = ttk.Frame(self.master, borderwidth=2, relief="solid", style='blue.TFrame')
        self.frame_aulas.place(x=611, y=394, width=650, height=340)
        ttk.Label(self.frame_aulas,text="Aulas",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 20)).pack(pady=3,padx=10)
        
        frame_contenedor3=ttk.Frame(self.frame_aulas,style='blue.TFrame')
        frame_contenedor3.pack(fill='x',pady=10)
        
        frame_izq_aulas=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_izq_aulas.pack(side='left',padx=10,anchor='n')
        
        frame_der_aulas=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_der_aulas.pack(side='left',padx=10,anchor='n')
        
        ttk.Label(frame_izq_aulas,text="Número de aula",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=5,padx=10)
        self.entry_num_aula=ttk.Entry(frame_izq_aulas,width=30,font=("Roboto", 15))
        self.entry_num_aula.pack(pady=2,padx=10)
        
        ttk.Label(frame_der_aulas,text="Capacidad",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=5,padx=10)
        self.entry_capacidad_aula=ttk.Entry(frame_der_aulas,width=20,font=("Roboto", 15))
        self.entry_capacidad_aula.pack(pady=2,padx=10)
        
        ttk.Label(frame_izq_aulas,text="Tipo de aula",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=5,padx=10)
        self.combo_tipo=ttk.Combobox(frame_izq_aulas,width=20,font=("Roboto", 15)) # Atributo público
        self.combo_tipo['values']=("Normal","tecnológica","laboratorio")
        self.combo_tipo.pack(pady=2,padx=10)
        
        boton_confirmar3=ttk.Button(frame_der_aulas,text="agregar",command=self.evento_Salones,style='Danger.TButton')
        boton_confirmar3.pack(pady=5,padx=5,anchor='n')
        
        self.frame_tabla_aula=ttk.Frame(self.frame_aulas, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_tabla_aula.pack(fill='both', expand=True, pady=10, padx=10)
        columnas=('salon','capacidad','Tipo')
        self.tabla_aulas=ttk.Treeview(self.frame_tabla_aula, columns=columnas, show='headings')
        self.tabla_aulas.column('salon',anchor='w',width=120)
        self.tabla_aulas.column('capacidad',anchor='w',width=120)
        self.tabla_aulas.column('Tipo',anchor='w',width=120)
        
        self.tabla_aulas.heading('salon',text='salon')
        self.tabla_aulas.heading('capacidad',text='capacidad')
        self.tabla_aulas.heading('Tipo',text='Tipo')
        self.tabla_aulas.insert(parent='', index='end', values=('Salón 101', '30'))
        
        scrollbar_vertical=ttk.Scrollbar(self.frame_tabla_aula,orient='vertical',command=self.tabla_aulas.yview)
        self.tabla_aulas.configure(yscroll=scrollbar_vertical.set)
        scrollbar_vertical.pack(side='right',fill='y')
        
        scrollbar_horizontal=ttk.Scrollbar(self.frame_tabla_aula,orient='horizontal',command=self.tabla_aulas.xview)
        self.tabla_aulas.configure(xscroll=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side='bottom',fill='x')
        self.tabla_aulas.pack(fill='both', expand=True)
        
    # --- MÉTODOS DE LA CLASE ---
    
    # Este método estaba causando el error. Ahora está fuera de __init__ y usa self correctamente.
    def abrir_ventana_gestion(self):
        try:
            VentanaGestion(self.master)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de gestión: {e}")
            
    def mostrar_datos_profesor(self):
            for item in self.tabla_profesores.get_children():
                self.tabla_profesores.delete(item)
            conexion=None
            cursor=None
            try:
                conexion=get_conexion()
                if conexion is None:
                    return []
                cursor=conexion.cursor()
                sql_t_profesores="SELECT profesor_id,nombre,dias_disponibles,CONCAT(disponible_inicio,'-',disponible_fin) AS HORARIO,en_linea FROM profesores"
                cursor.execute(sql_t_profesores)
                resultados=cursor.fetchall()
                
                if resultados:
                    for fila in resultados:
                        self.tabla_profesores.insert('', tk.END, values=fila)
            except mysql.connector.Error as err:
                messagebox.showerror("Error",f"Error al obtener los datos de los profesores: {err}")
                return []
            finally:
                if cursor is not None:
                    cursor.close()
                if conexion is not None and conexion.is_connected():
                    conexion.close()

    def mostrar_datos_salones(self):
            for item in self.tabla_aulas.get_children():
                self.tabla_aulas.delete(item)
            conexion=None
            cursor=None
            try:
                conexion=get_conexion()
                if conexion is None:
                    return []
                cursor=conexion.cursor()
                sql_t_salones="SELECT salon_id, capacidad, tipo FROM salones"
                cursor.execute(sql_t_salones)
                resultados=cursor.fetchall()
                
                if resultados:
                    for fila in resultados:
                        self.tabla_aulas.insert('', tk.END, values=fila)
            except mysql.connector.Error as err:
                messagebox.showerror("Error",f"Error al obtener los datos de los salones: {err}")
                return []
            finally:
                if cursor is not None:
                    cursor.close()
                if conexion is not None and conexion.is_connected():
                    conexion.close()
    
    def evento_Salones(self):
        print("Botón Salones presionado")
        aula=self.entry_num_aula.get()
        capacidad=self.entry_capacidad_aula.get()
        tipo=self.combo_tipo.get()
        print(f"aula: {aula}")
        print(f"capacidad: {capacidad}")
        print(f"tipo: {tipo}")
        try:
            from src.clases.salon import salon
            nuevo_salon = salon(
                numero_aula=aula,
                capacidad=capacidad,
                tipo=tipo
            )
            self.mostrar_datos_salones() 
        except NameError:
            print("ERROR: La clase 'salon' no está definida o no ha sido importada.")
    
        
    def evento_materias(self):
        print("Botón Materias presionado")
        clave=self.entry_materia_clave.get()
        nombre=self.entry_materia_nom.get()
        #grupo=self.entry_materia_gru.get()
        #profesor=self.combo_profesor.get()
        horas=self.entry_materia_horas.get()
        semestre=self.entry_materia_semestre.get()
        #salon=self.combo_salon.get()
        print(f"clave: {clave}")
        print(f"nombre: {nombre}")
        #print(f"grupo: {grupo}")
        #print(f"profesor: {profesor}")
        #print(f"horas a la semana: {horas}")
        print(f"semestre: {semestre}")
        #print(f"salon: {salon}")
        
        try: 
            from src.clases.materia import materia
            nueva_materia = materia(
                clave=clave,
                nombre=nombre,
                #grupo=grupo,
                #profesor=profesor,
                horas_semana=horas,
                semestre=semestre,
                #salon=salon
            )
        except NameError:
            print("ERROR: La clase 'profesor' no está definida o no ha sido importada.")

        
        
        
    def evento_boton_profesores(self): 
        print("Botón Profesores presionado")
        
        # Accediendo a los widgets, que son públicos (usando self.)
        cuenta=self.entry_no_cuenta.get()
        nombre=self.entry_nombre.get()
        apellido=self.entry_apellido.get()
        en_linea=self.combo_linea.get()
        horario_inicio=self.entry_horario_i.get()
        horario_fin= self.entry_horario_f.get()
        
        # -------------------------------------------------------------
        # CORRECCIÓN 2: Obtener los días seleccionados de los Checkbuttons
        # -------------------------------------------------------------
        dias_semana = {
            "Lunes": self.var_lunes.get(),
            "Martes": self.var_martes.get(),
            "Miércoles": self.var_miercoles.get(),
            "Jueves": self.var_jueves.get(),
            "Viernes": self.var_viernes.get(),
            "Sábado": self.var_sabado.get()
        }

        dias_seleccionados = []
        for dia, valor in dias_semana.items():
            if valor == 1: # 1 significa que la casilla está marcada
                dias_seleccionados.append(dia)
        
        # Convertir la lista de días seleccionados en una cadena separada por comas
        dias_str = ", ".join(dias_seleccionados)
        # -------------------------------------------------------------
        
        nombre_completo= f"{nombre} {apellido}"
        
        # 2. Llamar al constructor de la clase 'profesor'
        try:
            nuevo_profesor = profesor(
                cuenta=cuenta,
                nombre_completo=nombre_completo,
                dias=dias_str, # <--- ¡USANDO LA CADENA DINÁMICA!
                hora_entrada=horario_inicio,
                hora_salida=horario_fin,
                linea=en_linea
            )
        
        except NameError:
            print("ERROR: La clase 'profesor' no está definida o no ha sido importada.")

        print(f"nombre: {nombre_completo}")
        print(f"apellido: {apellido}")
        print(f"en linea: {en_linea}")
        print(f"horario: de {horario_inicio} a {horario_fin}")
        self.mostrar_datos_profesor() # Actualiza la tabla después de agregar un profesor
        
    def redimensionar_fondo(self, event):
        # Redimensiona la imagen al tamaño de la ventana
        new_ancho = event.width
        new_alto = event.height
        resized_image = self.original_image.resize((new_ancho, new_alto), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label.config(image=self.background_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    app.mostrar_datos_profesor() 
    app.mostrar_datos_salones()
    root.mainloop()
    