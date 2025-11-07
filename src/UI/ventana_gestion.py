import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# from src.clases.salon import salon # Descomenta si lo necesitas
from PIL import Image, ImageTk

class VentanaGestion:
    def __init__(self, master_window):
        
        #ESTILOS
        estilo =ttk.Style()
        estilo.configure('blue.TFrame', background='#0A0F1E')
        
        estilo.configure('TNotebook.Frame', background='#0A0F1E')

        # 3. Estilo para el área general del Notebook (detrás de las pestañas)
        estilo.configure('TNotebook', background='#0A0F1E')

        # 4. Estilo para las pestañas
        estilo.configure('TNotebook.Tab',
                         background='#1C2A4D',  # Fondo de pestaña no seleccionada
                         foreground='lightgrey', # Texto de pestaña no seleccionada
                         padding=[10, 5])

        # 5. Estilo para CUANDO una pestaña está SELECCIONADA
        #    'map' se usa para definir estilos basados en estados
        estilo.map('TNotebook.Tab',
                   background=[('selected', '#2A3F6E')], # Fondo de pestaña SELECCIONADA
                   foreground=[('selected', 'white')])
        
        # 1. CREACIÓN DE LA VENTANA
        # La nueva ventana se llama 'self.ventana'
        self.ventana = tk.Toplevel(master_window)
        self.ventana.title("Ventana de Gestión")
        
        # --- CORRECCIÓN 1 ---
        # Usa 'self.ventana', no 'self.master'
        self.ventana.state('zoomed')
        
        self.ventana.grab_set()  
        self.ventana.transient(master_window) 
        
        # 2. CARGA DE LA IMAGEN DE FONDO
        try:
            image = Image.open(r"assets/fondo.png")
            self.original_image = image
            
            # --- CORRECCIÓN 2 ---
            # El padre del Label es 'self.ventana'
            self.background_label = tk.Label(self.ventana)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # --- CORRECCIÓN 3 ---
            # El evento 'bind' se aplica a 'self.ventana'
            self.ventana.bind("<Configure>", self.redimensionar_fondo)
            
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            # --- CORRECCIÓN 4 ---
            # El 'config' de fallback es para 'self.ventana'
            self.ventana.config(bg="grey")
            
        # 3. CREACIÓN DE COMPONENTES
        # (Esto se movió fuera del 'except' para que siempre se ejecute)
        
        # El padre del frame es 'self.ventana'
        # --- ERROR CORREGIDO: Cambiado de tk.Frame a ttk.Frame ---
        self.frame_principal = ttk.Frame(self.ventana, borderwidth=0, relief="solid", style='blue.TFrame')
        
        # --- CAMBIO PARA CENTRAR EL FRAME ---
        # En lugar de .pack(), usamos .place() para centrar el frame
        # self.frame_principal.pack(fill='both', expand=True, padx=50, pady=50) 
        
        # Definimos un ancho y alto para el frame (ajusta según necesites)
        frame_ancho = 1100
        frame_alto = 700
        
        # Colocamos el frame en el centro de la ventana
        # relx=0.5, rely=0.5 -> Posiciona en el 50% horizontal y 50% vertical
        # anchor='center' -> Indica que el punto (relx, rely) es el CENTRO del frame
        self.frame_principal.place(relx=0.5, rely=0.5, anchor='center', width=frame_ancho, height=frame_alto)
        
        
        # --- CORRECCIÓN DE CONSISTENCIA: Cambiado de tk.Button a ttk.Button ---
        boton_cerrar = ttk.Button(self.frame_principal, text="Cerrar", command=self.ventana.destroy)
        boton_cerrar.pack(pady=2)
        
        #pestañas
        self.notebook=ttk.Notebook(self.frame_principal)
        self.notebook.pack(fill='both',expand='yes')
        self.pes0=ttk.Frame(self.notebook,style='blue.TFrame')
        self.pes1=ttk.Frame(self.notebook,style='blue.TFrame')
        
        self.notebook.add(self.pes0,text='Gestionar')
        self.notebook.add(self.pes1,text='ver horarios')
        
        #frames principales
        frame_contenedor=ttk.Frame(self.pes0,style='blue.TFrame')
        frame_contenedor.pack(fill='x',pady=10)
        
        self.frame_izq=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_izq,text="Gestion",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        self.frame_der=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_der,text="Vista previa",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        #frmae de profesores y materias
        frame_contenedor2=ttk.Frame(self.frame_izq,style='blue.TFrame')
        frame_contenedor2.pack(fill='x',pady=10)
        
        self.frame_izq_pf=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq_pf.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_izq_pf,text="Profesor",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        self.combo_profesores=ttk.Combobox(self.frame_izq_pf,width=20,font=("Roboto", 15)) # Atributo público
        self.combo_profesores['values']=("Sí","No")
        self.combo_profesores.pack(pady=3,padx=10)
        
        boton_guardar = ttk.Button(self.frame_izq_pf, text="Cerrar")
        boton_guardar.pack(pady=2)
        
        
        self.frame_der_pf=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der_pf.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_der_pf,text="materia",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        self.combo_materias=ttk.Combobox(self.frame_der_pf,width=20,font=("Roboto",15))
        self.combo_materias['values']=("si","no")
        self.combo_materias.pack(pady=3,padx=10)
        
        
        #FRAME_ASIGNACION AUTOMATICA
        frame_contenedor3=ttk.Frame(self.frame_izq,style='blue.TFrame')
        frame_contenedor3.pack(fill='x',pady=10)
        
        self.frame_izq_gp=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq_gp.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_izq_gp,text="grupo",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        self.combo_grupos=ttk.Combobox(self.frame_izq_gp,width=20,font=("Roboto", 15)) # Atributo público
        self.combo_grupos['values']=("Sí","No")
        self.combo_grupos.pack(pady=3,padx=10)
        
        boton_guardar2 = ttk.Button(self.frame_izq_gp, text="Empezar asignacion automatica")
        boton_guardar2.pack(pady=2)
        
        
        self.frame_der_gp=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der_gp.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_der_gp,text="semestre",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        self.combo_semestre=ttk.Combobox(self.frame_der_gp,width=20,font=("Roboto",15))
        self.combo_semestre['values']=("si","no")
        self.combo_semestre.pack(pady=3,padx=10)
        
        #frame derecho visualizacon
        
        self.frame_tablas=ttk.Frame(self.frame_der, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_tablas.pack(side='left',padx=10,anchor='n')
        columnas=('Profesor','materia')
        self.tabla_profesores=ttk.Treeview(self.frame_tablas, columns=columnas, show='headings')
        self.tabla_profesores.column('Profesor',anchor='w',width=120)
        self.tabla_profesores.column('materia',anchor='w',width=120)
        
        self.tabla_profesores.heading('Profesor',text='Profesor')
        self.tabla_profesores.heading('materia',text='materia')
        
        scrollbar_vertical=ttk.Scrollbar(self.frame_tablas,orient='vertical',command=self.tabla_profesores.yview)
        self.tabla_profesores.configure(yscroll=scrollbar_vertical.set)
        scrollbar_vertical.pack(side='right',fill='y')
        
        scrollbar_horizontal=ttk.Scrollbar(self.frame_tablas,orient='horizontal',command=self.tabla_profesores.xview)
        self.tabla_profesores.configure(xscroll=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side='bottom',fill='x')
        self.tabla_profesores.pack()
        
        # 4. ESPERAR CIERRE
        self.ventana.wait_window() 
        
    # --- CORRECCIÓN 5 ---
    # Este método faltaba en tu clase
    def redimensionar_fondo(self, event):
        """Redimensiona la imagen de fondo al tamaño de la ventana."""
        try:
            new_ancho = event.width
            new_alto = event.height
            
            if new_ancho > 0 and new_alto > 0 and hasattr(self, 'original_image'):
                resized_image = self.original_image.resize((new_ancho, new_alto), Image.LANCZOS)
                self.background_image = ImageTk.PhotoImage(resized_image)
                self.background_label.config(image=self.background_image)
        except Exception as e:
            print(f"Error al redimensionar fondo: {e}")