import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
#from ..conexion import inicializar_bd
#from ..gestor_horarios import GestorHorarios


    
class VentanaPrincipal:
    
    def __init__(self, master):
        self.master = master
        self.master.title("PLASEM")
        self.master.state('zoomed')  # Maximiza la ventana al iniciar
        db_path = "data/PLASEM.db"
        '''if not os.path.exists(db_path):
            print(f"La base de datos no existe en '{db_path}'. Creándola por primera vez...")
            try:
                inicializar_db()
                print("Base de datos creada exitosamente.")
            except Exception as e:
                print(f"Error crítico al inicializar la base de datos: {e}")
        else:
            print(f"Base de datos encontrada en '{db_path}'.")'''
        #--------------------------------------------------------------
        #---ESTILOS
        estilo =ttk.Style()
        estilo.theme_use('clam')  # Puedes cambiar 'clam' por otro tema si lo deseas
        estilo.configure(
            'blue.TFrame',
            background='#0A0F1E'  # Color azul claro
        )
        estilo.configure(
            'Custom.TCheckbutton',
            font=('Roboto', 16),
            background='#0A0F1E',
            foreground='#ffffff'   
        )
        estilo.configure(
            'Danger.TButton',
            font=('Roboto', 15),
            background='#6D583A',
            foreground='#000000',  # Texto blanco
            padding=10
        )
        estilo.configure(
            'Treeview.Heading',
            background='#2f4a23',  # Color de fondo del encabezado
            foreground='#ffffff',  # Color del texto del encabezado
        )
        #titulo=ttk.Style()
        #titulo.configure(
         #   'fondo.TLabel',
          #  background='#0A0F1E',  # Color azul claro
        #)
        #checbox de dias de semana
        # --- Carga de la imagen de fondo ---
        #----------------------------------------------
        #eventos_botones
            
        try:
            image = Image.open(r"assets/fondo.png")
            self.original_image = image  # Guarda la imagen original para redimensionar
            # Crea una etiqueta que contendrá la imagen de fondo
            self.background_label = tk.Label(self.master)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

            # 3. Vincula el evento <Configure> a la función de redimensionar
            # Esto hará que la función se llame CADA VEZ que la ventana cambie de tamaño
            self.master.bind("<Configure>", self.redimensionar_fondo)

        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            # Opcional: poner un color de fondo si la imagen falla
            self.master.config(bg="grey")
            
        # --- Creación del Frame DENTRO de la clase ---
       #-----FRAMES PRINCIPALES----
       # Frame para Profesores
       
        self.frame_profesores = ttk.Frame(self.master, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_profesores.place(x=140, y=32, width=450, height=700)
        e_profesores=ttk.Label(self.frame_profesores,text="Profesores",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 20)
                               ,style='fondo.TLabel')
        e_profesores.pack(pady=5,padx=10)
        #----------------------------------------
        frame_contenedor_datos=ttk.Frame(self.frame_profesores,style='blue.TFrame')
        frame_contenedor_datos.pack(fill='x',pady=10)
        
        self.frame_izq_datos=ttk.Frame(frame_contenedor_datos, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq_datos.pack(side='left',padx=10,anchor='n')
        
        self.frame_der_datos=ttk.Frame(frame_contenedor_datos, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der_datos.pack(side='left',padx=10,anchor='n')
        
        e_nombre=ttk.Label(self.frame_izq_datos,text="Nombre:",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_nombre.pack(pady=5,padx=10)
        
        self.entry_nombre=ttk.Entry(self.frame_izq_datos,width=20,font=("Roboto", 15))
        self.entry_nombre.pack(pady=5,padx=10)
        
        e_apellido=ttk.Label(self.frame_izq_datos,text="Apellidos:",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_apellido.pack(pady=5,padx=10)
        
        self.entry_apellido=ttk.Entry(self.frame_izq_datos,width=20,font=("Roboto", 15))
        self.entry_apellido.pack(pady=5,padx=10)
        
        e_linea=ttk.Label(self.frame_der_datos,text="¿En línea?:",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_linea.pack(pady=5,padx=10)
        self.combo_linea=ttk.Combobox(self.frame_der_datos,width=20,font=("Roboto", 15))
        self.combo_linea['values']=("Sí","No")
        self.combo_linea.pack(pady=5,padx=10)
        
        etiqueta_horario=ttk.Label(self.frame_der_datos,text="Horario:",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        etiqueta_horario.pack(pady=5,padx=10)
        self.entry_horario_i=ttk.Entry(self.frame_der_datos,width=20,font=("Roboto", 15))
        self.entry_horario_i.pack(pady=5,padx=10)
        #entry_horario_i.insert(0, "Inicio (HH:MM)")
        self.entry_horario_f=ttk.Entry(self.frame_der_datos,width=20,font=("Roboto", 15))
        self.entry_horario_f.pack(pady=5,padx=10)
        #entry_horario_f.insert(0, "Fin (HH:MM)")
        
        #---checkbox de dias de semana---
        
        
        frame_contenedor=ttk.Frame(self.frame_profesores,style='blue.TFrame')
        frame_contenedor.pack(fill='x',pady=10)
        
         # Frame para los Checkbuttons y el botón
        frame_dias=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_dias.pack(side='left',padx=10,anchor='n')
        
        frame_confirmar=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_confirmar.pack(side='left',padx=10,anchor='n')
        
        
        def seleccionar():
            seleccion = []
            if var_lunes.get():
                seleccion.append("Lunes")
            if var_martes.get():
                seleccion.append("Martes")
            if var_miercoles.get():
                seleccion.append("Miércoles")
            if var_jueves.get():
                seleccion.append("Jueves")
            if var_viernes.get():
                seleccion.append("Viernes")
            if var_sabado.get():
                seleccion.append("Sábado")
            print("Días seleccionados:", ", ".join(seleccion))
        var_lunes = tk.IntVar()
        var_martes = tk.IntVar()
        var_miercoles = tk.IntVar()
        var_jueves = tk.IntVar()
        var_viernes = tk.IntVar()
        var_sabado = tk.IntVar()
        
        Checkbutton_lunes = ttk.Checkbutton(frame_dias, text="Lunes", 
                                            variable=var_lunes,command=seleccionar,
                                            style='Custom.TCheckbutton')
        Checkbutton_lunes.pack(pady=5,padx=5,anchor='w')
        Checkbutton_martes = ttk.Checkbutton(frame_dias, text="Martes", 
                                             variable=var_martes,command=seleccionar
                                             ,style='Custom.TCheckbutton')
        Checkbutton_martes.pack(pady=5,padx=5,anchor='w')
        Checkbutton_miercoles = ttk.Checkbutton(frame_dias, text="Miércoles", 
                                                variable=var_miercoles, command=seleccionar
                                                ,style='Custom.TCheckbutton')
        Checkbutton_miercoles.pack(pady=5,padx=5,anchor='w')
        Checkbutton_jueves = ttk.Checkbutton(frame_dias, text="Jueves", 
                                             variable=var_jueves, command=seleccionar
                                             ,style='Custom.TCheckbutton')
        Checkbutton_jueves.pack(pady=5,padx=5,anchor='w')
        Checkbutton_viernes = ttk.Checkbutton(frame_dias, text="Viernes", 
                                              variable=var_viernes, command=seleccionar
                                              ,style='Custom.TCheckbutton')
        Checkbutton_viernes.pack(pady=5,padx=5, anchor='w')
        Checkbutton_sabado = ttk.Checkbutton(frame_dias, text="Sábado", 
                                             variable=var_sabado, command=seleccionar
                                             ,style='Custom.TCheckbutton')
        Checkbutton_sabado.pack(pady=5,padx=5, anchor='w')
        
        def evento_boton_profesores(self):
            print("Botón Profesores presionado")
            nombre=self.entry_nombre.get()
            apellido=self.entry_apellido.get()
            en_linea=self.combo_linea.get()
            horario_inicio=self.entry_horario_i.get()
            horario_fin= self.entry_horario_f.get()
            
            print(f"nombre: {nombre}")
            print(f"apellido: {apellido}")
            print(f"en linea: {en_linea}")
            print(f"horario: de {horario_inicio} a {horario_fin}")
            
            
        boton_confirmar=ttk.Button(frame_confirmar,text="Confirmar",command=evento_boton_profesores,style='Danger.TButton')
        boton_confirmar.pack(pady=5,padx=5,anchor='n')
        
        
        separador=ttk.Separator(self.frame_profesores,orient='horizontal')
        separador.pack(fill='x',padx=10,pady=10)
        #---formatos de tabla---
        self.frame_tablas=ttk.Frame(self.frame_profesores, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_tablas.pack(pady=10,padx=10)
        columnas=('Profesor','Dias','Horario','¿en linea?')
        self.tabla_profesores=ttk.Treeview(
            self.frame_tablas,
            columns=columnas,
            show='headings',
        )
        self.tabla_profesores.column('Profesor',anchor='w',width=120)
        self.tabla_profesores.column('Dias',anchor='w',width=120)
        self.tabla_profesores.column('Horario',anchor='w',width=120)
        self.tabla_profesores.column('¿en linea?',anchor='w',width=120)
        
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
        
        #----------------------------
        
        
        e_prueba=ttk.Label(self.frame_tablas,text="Apellidos:",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_prueba.pack(pady=10,padx=10)
        
        
        #ttk.label(self.frame_profesores,text="Dias de clase:",background='#0A0F1E',foreground='#ffffff',)
        
        #--------------------------------------------------------------
        #--------------------------------------------------------------
        # Frame para Materias
        self.frame_materias = ttk.Frame(self.master, borderwidth=2, relief="solid", style='blue.TFrame')
        self.frame_materias.place(x=611, y=31, width=650, height=350)
        e_materias=ttk.Label(self.frame_materias,text="Materias",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 30))
        e_materias.pack(pady=10,padx=10)
        
        '''contenedor_scroll=ttk.Frame(self.frame_materias,style='blue.TFrame')
        contenedor_scroll.pack(pady=10,padx=10)
        canvas=tk.Canvas(contenedor_scroll,background='#0A0F1E',highlightthickness=0)
        scrollbar_vertical2=ttk.Scrollbar(contenedor_scroll,orient='vertical',command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar_vertical2.set)
        
        scrollbar_vertical2.pack(side='right',fill='y')
        canvas.pack(side='left',fill='both',expand=True)
        
        self.frame_contenido_scroll=ttk.Frame(canvas,style='blue.TFrame')
        canvas.create_window((0,0),window=self.frame_contenido_scroll,anchor='nw')'''
        
        frame_contenedor2=ttk.Frame(self.frame_materias,style='blue.TFrame')
        frame_contenedor2.pack(fill='x',pady=10)
        
         # Frame para los Checkbuttons y el botón
        frame_izq=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_izq.pack(side='left',padx=10,anchor='n')
        
        frame_derecha=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_derecha.pack(side='left',padx=10,anchor='n')
        
        e_nombre_materia=ttk.Label(frame_izq,text="Nombre",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_nombre_materia.pack(pady=10,padx=10)
        entry_materia_nom=ttk.Entry(frame_izq,width=30,font=("Roboto", 15))
        entry_materia_nom.pack(pady=10,padx=10)
        
        e_grupo_materia=ttk.Label(frame_izq,text="Grupo",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_grupo_materia.pack(pady=10,padx=10)
        entry_materia_gru=ttk.Entry(frame_izq,width=30,font=("Roboto", 15))
        entry_materia_gru.pack(pady=10,padx=10)
        
        e_profesor_materia=ttk.Label(frame_izq,text="Profesor",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_profesor_materia.pack(pady=10,padx=10)
        combo_profesor=ttk.Combobox(frame_izq,width=30,font=("Roboto", 15))
        
        combo_profesor['values']=("Profesor 1","Profesor 2","Profesor 3")
        combo_profesor.pack(pady=5,padx=10)
        

        e_horas_materia=ttk.Label(frame_derecha,text="Horas a la semana",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_horas_materia.pack(pady=4,padx=10)
        entry_materia_horas=ttk.Entry(frame_derecha,width=20,font=("Roboto", 15))
        entry_materia_horas.pack(pady=4,padx=10)
        
        e_semestre_materia=ttk.Label(frame_derecha,text="Semestre",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_semestre_materia.pack(pady=4,padx=10)
        entry_materia_semestre=ttk.Entry(frame_derecha,width=20,font=("Roboto", 15))
        entry_materia_semestre.pack(pady=4,padx=10)
        
        e_salon_materia=ttk.Label(frame_derecha,text="Salón",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_salon_materia.pack(pady=4,padx=10)
        combo_salon=ttk.Combobox(frame_derecha,width=20,font=("Roboto", 15))
        combo_salon['values']=("Salón 1","Salón 2","Salón 3")
        combo_salon.pack(pady=4,padx=10) 
        
        boton_confirmar2=ttk.Button(frame_derecha,text="agregar",command=seleccionar,style='Danger.TButton')
        boton_confirmar2.pack(pady=4,padx=5,anchor='n')
        
        
        #--------------------------------------------------------------
        #--------------------------------------------------------------
        #frame para Aulas
        self.frame_aulas = ttk.Frame(self.master, borderwidth=2, relief="solid", style='blue.TFrame')
        self.frame_aulas.place(x=611, y=394, width=650, height=340)
        e_aulas=ttk.Label(self.frame_aulas,text="Aulas",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 20))
        e_aulas.pack(pady=5,padx=10)
        
        frame_contenedor3=ttk.Frame(self.frame_aulas,style='blue.TFrame')
        frame_contenedor3.pack(fill='x',pady=10)
        
         # Frame para los Checkbuttons y el botón
        frame_izq_aulas=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_izq_aulas.pack(side='left',padx=10,anchor='n')
        
        frame_der_aulas=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_der_aulas.pack(side='left',padx=10,anchor='n')
        
        e_num_aula=ttk.Label(frame_izq_aulas,text="Número de aula",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_num_aula.pack(pady=5,padx=10)
        entry_num_aula=ttk.Entry(frame_izq_aulas,width=30,font=("Roboto", 15))
        entry_num_aula.pack(pady=5,padx=10)
        
        e_capacidad_aula=ttk.Label(frame_der_aulas,text="Capacidad",background='#0A0F1E',foreground='#ffffff',
                               font=("Roboto", 10))
        e_capacidad_aula.pack(pady=5,padx=10)
        entry_capacidad_aula=ttk.Entry(frame_der_aulas,width=20,font=("Roboto", 15))
        entry_capacidad_aula.pack(pady=5,padx=10)
        
        boton_confirmar3=ttk.Button(frame_der_aulas,text="agregar",command=seleccionar,style='Danger.TButton')
        boton_confirmar3.pack(pady=5,padx=5,anchor='n')
        
        self.frame_tabla_aula=ttk.Frame(self.frame_aulas, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_tabla_aula.pack(fill='both', expand=True, pady=10, padx=10)
        columnas=('salon','capacidad')
        self.tabla_aulas=ttk.Treeview(
            self.frame_tabla_aula,
            columns=columnas,
            show='headings',
        )
        self.tabla_aulas.column('salon',anchor='w',width=120)
        self.tabla_aulas.column('capacidad',anchor='w',width=120)
        
        self.tabla_aulas.heading('salon',text='salon')
        self.tabla_aulas.heading('capacidad',text='capacidad')
        self.tabla_aulas.insert(parent='', index='end', values=('Salón 101', '30'))
        
        scrollbar_vertical=ttk.Scrollbar(self.frame_tabla_aula,orient='vertical',command=self.tabla_aulas.yview)
        self.tabla_aulas.configure(yscroll=scrollbar_vertical.set)
        scrollbar_vertical.pack(side='right',fill='y')
        
        scrollbar_horizontal=ttk.Scrollbar(self.frame_tabla_aula,orient='horizontal',command=self.tabla_aulas.xview)
        self.tabla_aulas.configure(xscroll=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side='bottom',fill='x')
        self.tabla_aulas.pack(fill='both', expand=True)
        
        #self.gestor_horarios = GestorHorarios()
        
        #--------------------------------------------------------------
        #--------------------------------------------------------------
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
    root.mainloop()