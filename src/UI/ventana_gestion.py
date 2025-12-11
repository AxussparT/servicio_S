import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from src.conexion import get_conexion 

class VentanaGestion:
    def __init__(self, master_window):
        
        estilo =ttk.Style()
        estilo.configure('blue.TFrame', background='#0A0F1E')
        
        # 1. CREACIÓN DE LA VENTANA Toplevel
        self.ventana = tk.Toplevel(master_window)
        self.ventana.title("Ventana de Gestión")
        self.ventana.state('zoomed')
        self.ventana.grab_set() 
        self.ventana.transient(master_window) 
        
        # 2. CARGA Y AJUSTE DE LA IMAGEN DE FONDO
        try:
            image = Image.open(r"assets/fondo.png")
            self.original_image = image
            self.background_label = tk.Label(self.ventana)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.ventana.bind("<Configure>", self.redimensionar_fondo)
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            self.ventana.config(bg="grey")
            
        # 3. CREACIÓN DE COMPONENTES
        self.frame_principal = ttk.Frame(self.ventana, borderwidth=0, relief="solid", style='blue.TFrame')
        frame_ancho = 1100
        frame_alto = 700
        self.frame_principal.place(relx=0.5, rely=0.5, anchor='center', width=frame_ancho, height=frame_alto)
        
        boton_cerrar = ttk.Button(self.frame_principal, text="Cerrar", command=self.ventana.destroy)
        boton_cerrar.pack(pady=2)
        
        # Pestañas (Notebook)
        self.notebook=ttk.Notebook(self.frame_principal)
        self.notebook.pack(fill='both',expand='yes')
        self.pes0=ttk.Frame(self.notebook,style='blue.TFrame')
        self.pes1=ttk.Frame(self.notebook,style='blue.TFrame')
        
        self.notebook.add(self.pes0,text='Gestionar')
        self.notebook.add(self.pes1,text='ver horarios')
        
        # Frames principales
        frame_contenedor=ttk.Frame(self.pes0,style='blue.TFrame')
        frame_contenedor.pack(fill='x',pady=10)
        
        self.frame_izq=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_izq,text="Gestion",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        self.frame_der=ttk.Frame(frame_contenedor, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_der,text="Vista previa",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        # Frame de profesores y materias
        frame_contenedor2=ttk.Frame(self.frame_izq,style='blue.TFrame')
        frame_contenedor2.pack(fill='x',pady=10)
        
        self.frame_izq_pf=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq_pf.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_izq_pf,text="Profesor",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        # COMBO PROFESORES
        self.combo_profesores=ttk.Combobox(self.frame_izq_pf,width=20,font=("Roboto", 15), state='readonly') 
        self.combo_profesores.pack(pady=3,padx=10)
        self.combo_profesores.bind("<<ComboboxSelected>>", self.actualizar_vista_previa) 
        
        # Botón "Asignar Manualmente"
        boton_asignar = ttk.Button(self.frame_izq_pf, text="Asignar Manualmente", 
                                   command=self.asignar_profesor_materia)
        boton_asignar.pack(pady=2)
        
        
        self.frame_der_pf=ttk.Frame(frame_contenedor2, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der_pf.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_der_pf,text="materia",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        # COMBO MATERIAS
        self.combo_materias=ttk.Combobox(self.frame_der_pf,width=20,font=("Roboto",15), state='readonly')
        self.combo_materias.pack(pady=3,padx=10)
        
        # VINCULACIÓN: Actualiza semestre, vista previa Y FILTRA GRUPOS
        self.combo_materias.bind("<<ComboboxSelected>>", 
                                 lambda e: (self.mostrar_semestre_de_materia(e), 
                                            self.actualizar_vista_previa(e),
                                            self.actualizar_combo_grupos(e)))
        
        # FRAME_ASIGNACION AUTOMATICA
        frame_contenedor3=ttk.Frame(self.frame_izq,style='blue.TFrame')
        frame_contenedor3.pack(fill='x',pady=10)
        
        self.frame_izq_gp=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_izq_gp.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_izq_gp,text="grupo",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        
        # COMBO GRUPOS - Estado normal para permitir la entrada manual
        self.combo_grupos=ttk.Combobox(self.frame_izq_gp,width=20,font=("Roboto", 15), state='normal') 
        self.combo_grupos.pack(pady=3,padx=10)
        
        boton_guardar2 = ttk.Button(self.frame_izq_gp, text="Empezar asignacion automatica")
        boton_guardar2.pack(pady=2)
        
        
        self.frame_der_gp=ttk.Frame(frame_contenedor3, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_der_gp.pack(side='left',padx=10,anchor='n')
        ttk.Label(self.frame_der_gp,text="semestre",background='#0A0F1E',foreground='#ffffff', font=("Roboto", 10)).pack(pady=3,padx=10)
        # COMBO SEMESTRE
        self.combo_semestre=ttk.Combobox(self.frame_der_gp,width=20,font=("Roboto",15), state='readonly')
        self.combo_semestre.pack(pady=3,padx=10)
        
        # Vista Previa (Tabla)
        self.frame_tablas=ttk.Frame(self.frame_der, borderwidth=0, relief="solid", style='blue.TFrame')
        self.frame_tablas.pack(side='left',padx=10,anchor='n')
        columnas=('Profesor','materia')
        self.tabla_profesores=ttk.Treeview(self.frame_tablas, columns=columnas, show='headings')
        self.tabla_profesores.column('Profesor',anchor='w',width=120)
        self.tabla_profesores.column('materia',anchor='w',width=120)
        
        self.tabla_profesores.heading('Profesor',text='Profesor')
        self.tabla_profesores.heading('materia',text='materia (Grupo)')
        
        scrollbar_vertical=ttk.Scrollbar(self.frame_tablas,orient='vertical',command=self.tabla_profesores.yview)
        self.tabla_profesores.configure(yscroll=scrollbar_vertical.set)
        scrollbar_vertical.pack(side='right',fill='y')
        
        scrollbar_horizontal=ttk.Scrollbar(self.frame_tablas,orient='horizontal',command=self.tabla_profesores.xview)
        self.tabla_profesores.configure(xscroll=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side='bottom',fill='x')
        self.tabla_profesores.pack()
        
        # Diccionarios para almacenar el mapeo de IDs y datos de la BD
        self.profesores_map = {} 
        self.materias_map = {} # {materia_id: semestre_id}
        self.horas_materia_map = {} 
        self.grupos_map = {} # {grupo_id: 'ID - Nombre'}
        self.semestres_map = {}
        
        # 4. Cargar datos iniciales y esperar cierre
        self.cargar_combos_bd() 
        self.ventana.wait_window() 
        
    # --- MÉTODOS DE LA CLASE ---

    def obtener_disponibilidad_y_periodo(self, profesor_id, materia_id):
        """
        Consulta la disponibilidad del profesor y las horas/semestre de la materia.
        Calcula el Periodo (A/B) de la materia.
        Retorna un diccionario con los datos.
        """
        datos = {
            'dias_dis': 'No Definido',
            'horas_dis': 'No Definido',
            'horas_sem': 0,
            'semestre': 0,
            'periodo': 'N'
        }
        conexion = None
        cursor = None

        try:
            conexion = get_conexion()
            if conexion is None:
                return datos
            cursor = conexion.cursor()

            # Obtener datos de la Materia (Semestre y Horas_Semana)
            sql_materia = "SELECT semestre_id, horas_semana FROM materias WHERE materia_id = %s"
            cursor.execute(sql_materia, (materia_id,))
            res_materia = cursor.fetchone()
            
            if res_materia:
                # El campo horas_semana en la BD es VARCHAR, se intenta convertir a INT para el cálculo
                try:
                    datos['semestre'] = int(res_materia[0])
                    datos['horas_sem'] = int(res_materia[1])
                except (ValueError, TypeError):
                    datos['semestre'] = 0
                    datos['horas_sem'] = 0
                
                # Clasificar el Periodo A (Impar) o B (Par)
                if datos['semestre'] > 0:
                    datos['periodo'] = 'A' if datos['semestre'] % 2 != 0 else 'B'

            # Obtener Disponibilidad del Profesor 
            sql_profesor = "SELECT dias_disponibles, disponible_inicio, disponible_fin FROM profesores WHERE profesor_id = %s"
            cursor.execute(sql_profesor, (profesor_id,))
            res_profesor = cursor.fetchone()
            
            if res_profesor:
                dias = res_profesor[0] if res_profesor[0] else 'ND'
                h_inicio = str(res_profesor[1]) if res_profesor[1] else '00:00:00'
                h_fin = str(res_profesor[2]) if res_profesor[2] else '00:00:00'
                
                datos['dias_dis'] = dias
                datos['horas_dis'] = f"{h_inicio.split('.')[0]}-{h_fin.split('.')[0]}" # Formato 08:00:00-14:00:00

            return datos

        except mysql.connector.Error as err:
            print(f"Error de BD al obtener datos auxiliares: {err}")
            return datos
        finally:
            if cursor: cursor.close()
            if conexion and conexion.is_connected(): conexion.close()


    def cargar_combos_bd(self):
        """Carga los datos de las tablas en los combos y el mapa de materias/grupos."""
        conexion = None
        cursor = None
        
        try:
            conexion = get_conexion()
            if conexion is None:
                messagebox.showerror("Error de Conexión", "No se pudo establecer conexión con la base de datos para cargar combos.")
                return

            cursor = conexion.cursor()
            
            # --- PROFESORES (Carga completa) ---
            sql_profesores = "SELECT profesor_id, nombre FROM profesores ORDER BY nombre"
            cursor.execute(sql_profesores)
            profesores_data_raw = cursor.fetchall()
            self.profesores_map = {str(row[0]): f"{row[0]} - {row[1]}" for row in profesores_data_raw}
            self.combo_profesores['values'] = list(self.profesores_map.values())
            if self.profesores_map: self.combo_profesores.set(list(self.profesores_map.values())[0])
                
            # --- SEMESTRES (Carga completa) ---
            sql_semestres = "SELECT id_semestre, nombre FROM semestres ORDER BY id_semestre"
            cursor.execute(sql_semestres)
            semestres_data_raw = cursor.fetchall()
            self.semestres_map = {str(row[0]): f"{row[0]} - {row[1]}" for row in semestres_data_raw}
            self.combo_semestre['values'] = list(self.semestres_map.values())
            if self.semestres_map: self.combo_semestre.set(list(self.semestres_map.values())[0])

            # --- MATERIAS (Carga completa incluyendo horas y semestre) ---
            sql_materias = "SELECT materia_id, nombre, semestre_id, horas_semana FROM materias ORDER BY nombre"
            cursor.execute(sql_materias)
            materias_combo_data = []
            self.materias_map = {} 
            self.horas_materia_map = {}
            
            for row in cursor.fetchall():
                materia_id, nombre_materia, semestre_id, horas_semana = row
                combo_value = f"{materia_id} - {nombre_materia}"
                materias_combo_data.append(combo_value)
                self.materias_map[str(materia_id)] = semestre_id 
                self.horas_materia_map[str(materia_id)] = horas_semana 
                
            self.combo_materias['values'] = materias_combo_data
            if materias_combo_data:
                self.combo_materias.set(materias_combo_data[0])
                self.mostrar_semestre_de_materia() 
                
            # --- GRUPOS (Carga inicial) ---
            sql_grupos = "SELECT grupo_id, nombre FROM grupos ORDER BY nombre"
            cursor.execute(sql_grupos)
            grupos_data_raw = cursor.fetchall()
            self.grupos_map = {str(row[0]): f"{row[0]} - {row[1]}" for row in grupos_data_raw}
            
            # Cargar grupos y actualizar filtro inicial
            self.actualizar_combo_grupos()
            self.actualizar_vista_previa()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error de BD", f"Error al cargar los combos: {err}")
            
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
    
    def actualizar_combo_grupos(self, event=None):
        """
        Filtra el combobox de Grupos para quitar aquellos a los que 
        la materia seleccionada ya ha sido asignada.
        """
        # Asegurarse de que la ventana exista antes de manipular widgets
        if not self.ventana.winfo_exists():
            return
            
        selected_materia_str = self.combo_materias.get()
        if not selected_materia_str or ' - ' not in selected_materia_str:
            # Si no hay materia seleccionada, muestra todos los grupos
            grupos_disponibles = list(self.grupos_map.values())
            self.combo_grupos['values'] = grupos_disponibles
            if grupos_disponibles:
                 self.combo_grupos.set(grupos_disponibles[0])
            else:
                 self.combo_grupos.set("")
            return

        materia_id = selected_materia_str.split(' - ')[0]
        grupos_asignados = set()
        conexion = None
        cursor = None
        
        try:
            conexion = get_conexion()
            if conexion is None:
                return

            cursor = conexion.cursor()
            
            # Consultar todos los grupos que ya tienen esta materia asignada
            sql_asignados = "SELECT DISTINCT grupo_id FROM asignaciones WHERE materia_id = %s"
            cursor.execute(sql_asignados, (materia_id,))
            
            for row in cursor.fetchall():
                grupos_asignados.add(row[0])

            # Filtrar el mapa completo de grupos
            grupos_disponibles_data = []
            for grupo_id, display_value in self.grupos_map.items():
                if grupo_id not in grupos_asignados:
                    grupos_disponibles_data.append(display_value)
            
            self.combo_grupos['values'] = grupos_disponibles_data
            
            # Mantener la selección actual si sigue siendo válida o establecer el primer elemento
            current_selection = self.combo_grupos.get()
            if current_selection not in grupos_disponibles_data or current_selection == "TODOS ASIGNADOS" or current_selection == "Error de carga":
                 if grupos_disponibles_data:
                    self.combo_grupos.set(grupos_disponibles_data[0])
                 else:
                    self.combo_grupos.set("TODOS ASIGNADOS")
                
        except mysql.connector.Error as err:
            print(f"Error de BD al filtrar grupos: {err}")
            self.combo_grupos.set("Error de carga")
        finally:
            if cursor: cursor.close()
            if conexion and conexion.is_connected(): conexion.close()


    def obtener_o_crear_grupo(self, grupo_input_str):
        """
        Busca el ID de un grupo existente o lo inserta como nuevo grupo si no lo encuentra.
        Retorna el grupo_id (VARCHAR) o None si falla.
        """
        grupo_input_str = grupo_input_str.strip()
        if not grupo_input_str:
            messagebox.showerror("Error de Grupo", "El campo Grupo no puede estar vacío.")
            return None
        
        conexion = None
        cursor = None
        
        try:
            conexion = get_conexion()
            if conexion is None:
                return None
            cursor = conexion.cursor()

            # 1. Intentar extraer ID si el formato es 'ID - Nombre' (grupo ya cargado y seleccionado)
            if ' - ' in grupo_input_str:
                grupo_id_check = grupo_input_str.split(' - ')[0]
                sql_check = "SELECT grupo_id FROM grupos WHERE grupo_id = %s"
                cursor.execute(sql_check, (grupo_id_check,))
                if cursor.fetchone():
                    return grupo_id_check 
            
            # 2. Usar la entrada simple como ID y Nombre (para la creación)
            grupo_simple = grupo_input_str.upper() 
            
            # Buscar si el valor simple ya existe como ID
            sql_check_id = "SELECT grupo_id FROM grupos WHERE grupo_id = %s"
            cursor.execute(sql_check_id, (grupo_simple,))
            if cursor.fetchone():
                return grupo_simple # Ya existe con ese ID/nombre simple.

            # 3. Insertar como nuevo grupo
            sql_insert = "INSERT INTO grupos (grupo_id, nombre) VALUES (%s, %s)"
            cursor.execute(sql_insert, (grupo_simple, grupo_simple))
            conexion.commit()
            
            self.cargar_combos_bd() # Recargar combos para incluir el nuevo grupo
            messagebox.showinfo("Nuevo Grupo Creado", f"El grupo '{grupo_simple}' ha sido registrado y utilizado.")
            
            return grupo_simple

        except mysql.connector.Error as err:
            conexion.rollback()
            messagebox.showerror("Error de BD", f"Error al gestionar el grupo: {err}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado al procesar el grupo: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def mostrar_semestre_de_materia(self, event=None):
        """Detecta la materia seleccionada y actualiza el combobox de semestre automáticamente."""
        if not self.ventana.winfo_exists():
            return

        selected_materia_str = self.combo_materias.get()
        if not selected_materia_str:
            self.combo_semestre.set("") 
            return
            
        try:
            materia_id = selected_materia_str.split(' - ')[0]
            semestre_id = self.materias_map.get(materia_id)
            
            if semestre_id is not None:
                semestre_display_value = self.semestres_map.get(str(semestre_id))
                
                if semestre_display_value:
                    self.combo_semestre.set(semestre_display_value)
                else:
                    self.combo_semestre.set("Error: Semestre desconocido")
            else:
                self.combo_semestre.set("No Asignado")
                
        except Exception as e:
            print(f"Error al procesar la selección de materia: {e}")
            self.combo_semestre.set("")

    def asignar_profesor_materia(self):
        """
        Guarda la asignación de Profesor, Materia y GRUPO.
        Incluye validación para evitar que la misma Materia se asigne dos veces al mismo Grupo.
        """
        # 🚨 SOLUCIÓN ERROR TCL: Verificar que la ventana exista antes de continuar
        if not self.ventana.winfo_exists():
            return
        
        profesor_str = self.combo_profesores.get()
        materia_str = self.combo_materias.get()
        grupo_str = self.combo_grupos.get() 
        
        try:
            profesor_id = profesor_str.split(' - ')[0]
            materia_id = materia_str.split(' - ')[0]
        except IndexError:
            messagebox.showerror("Error de Selección", "Debe seleccionar Profesor y Materia válidos.")
            return
        
        # 1. Obtener/Crear el ID del grupo
        grupo_id = self.obtener_o_crear_grupo(grupo_str)
        if grupo_id is None:
            return 
            
        # 2. Obtener datos auxiliares (Disponibilidad, Horas, Periodo)
        datos_aux = self.obtener_disponibilidad_y_periodo(profesor_id, materia_id)
        if datos_aux['semestre'] == 0:
            messagebox.showwarning("Datos Incompletos", "No se pudo obtener el semestre o las horas/semana de la materia. Asignación cancelada.")
            return

        conexion = None
        cursor = None
        
        try:
            conexion = get_conexion()
            if conexion is None:
                return

            cursor = conexion.cursor()
            
            # 3. VALIDACIÓN CLAVE: Verificar si la Materia ya está asignada al GRUPO
            sql_check_grupo_materia = "SELECT profesor_id FROM asignaciones WHERE materia_id = %s AND grupo_id = %s"
            cursor.execute(sql_check_grupo_materia, (materia_id, grupo_id))
            
            # Guardamos el resultado ANTES de cerrar el cursor para otra consulta
            asignacion_existente = cursor.fetchone()
            
            if asignacion_existente:
                profesor_existente_id = asignacion_existente[0]
                
                # Cerrar el cursor actual y abrir uno nuevo para obtener el nombre del profesor
                cursor.close() 
                cursor = conexion.cursor() 
                
                sql_prof_nombre = "SELECT nombre FROM profesores WHERE profesor_id = %s"
                cursor.execute(sql_prof_nombre, (profesor_existente_id,))
                
                nombre_prof_existente_res = cursor.fetchone()
                nombre_prof_existente = nombre_prof_existente_res[0] if nombre_prof_existente_res else profesor_existente_id

                messagebox.showwarning("Asignación Duplicada", 
                                       f"La Materia **{materia_id}** ya está asignada al Grupo **{grupo_id}** "
                                       f"por el Profesor **{nombre_prof_existente}**. No se puede asignar a otro profesor.")
                return
            
            # Si llegamos aquí sin duplicados, aseguramos que el cursor esté abierto para la inserción
            if cursor is None or cursor.closed:
                 cursor = conexion.cursor()

            # 4. Insertar la nueva asignación con todos los nuevos campos
            sql_insert = """
                INSERT INTO asignaciones (
                    profesor_id, materia_id, grupo_id, 
                    dias_dis, horas_dis, 
                    horas_sem, semestre, periodo
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                profesor_id, materia_id, grupo_id, 
                datos_aux['dias_dis'], datos_aux['horas_dis'], 
                datos_aux['horas_sem'], datos_aux['semestre'], datos_aux['periodo']
            )
            
            cursor.execute(sql_insert, valores)
            conexion.commit()
            
            messagebox.showinfo("Éxito", 
                                 f"Asignación guardada: Profesor {profesor_id} a Materia {materia_id} para el Grupo {grupo_id}.")
            
            # 5. Actualizar UI
            self.actualizar_vista_previa()
            self.actualizar_combo_grupos() # Refresca el filtro de grupos
            
        except mysql.connector.Error as err:
            if conexion and conexion.is_connected():
                   conexion.rollback()
            messagebox.showerror("Error de BD", 
                                 f"Error al intentar asignar: {err}\nVerifique si las claves foráneas y la estructura de la tabla 'asignaciones' son correctas.")
            
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    
    def actualizar_vista_previa(self, event=None):
        """Consulta la BD para obtener las asignaciones y actualiza la tabla de vista previa."""
        
        # 🚨 SOLUCIÓN ERROR TCL: Verificar que la ventana exista antes de manipular combos
        if not self.ventana.winfo_exists():
            return

        # Verificar existencia de Comboboxes (puede ocurrir si la destrucción es rápida)
        if not hasattr(self, 'combo_profesores') or not self.combo_profesores.winfo_exists():
            return

        profesor_str = self.combo_profesores.get()
        materia_str = self.combo_materias.get()
        grupo_str = self.combo_grupos.get() 
        
        try:
            profesor_id = profesor_str.split(' - ')[0] if profesor_str and ' - ' in profesor_str else None
            materia_id = materia_str.split(' - ')[0] if materia_str and ' - ' in materia_str else None
            
            if grupo_str and ' - ' in grupo_str:
                 grupo_id = grupo_str.split(' - ')[0]
            elif grupo_str:
                 grupo_id = grupo_str.upper()
            else:
                 grupo_id = None
                 
        except:
            profesor_id = None
            materia_id = None
            grupo_id = None
        
        for item in self.tabla_profesores.get_children():
            self.tabla_profesores.delete(item)
        
        conexion = None
        cursor = None
        
        try:
            conexion = get_conexion()
            if conexion is None:
                return

            cursor = conexion.cursor()
            
            # Obtiene los nombres de profesores, materias y grupos
            sql = """
                SELECT 
                    a.profesor_id, p.nombre AS nombre_profesor, 
                    a.materia_id, m.nombre AS nombre_materia,
                    a.grupo_id, g.nombre AS nombre_grupo
                FROM 
                    asignaciones a
                JOIN profesores p ON a.profesor_id = p.profesor_id
                JOIN materias m ON a.materia_id = m.materia_id
                JOIN grupos g ON a.grupo_id = g.grupo_id 
                WHERE 1=1 
            """
            params = []

            if profesor_id:
                sql += " AND a.profesor_id = %s"
                params.append(profesor_id)

            if materia_id:
                sql += " AND a.materia_id = %s"
                params.append(materia_id)
            
            if grupo_id: 
                sql += " AND a.grupo_id = %s"
                params.append(grupo_id)
                
            sql += " LIMIT 50" 
            
            cursor.execute(sql, params)
            resultados = cursor.fetchall()
            
            # Insertar resultados en la Treeview
            if resultados:
                for row in resultados:
                    profesor_display = f"{row[0]} - {row[1]}"
                    materia_display = f"{row[2]} - {row[3]} ({row[5]})" 
                    self.tabla_profesores.insert('', 'end', values=(profesor_display, materia_display))
            else:
                self.tabla_profesores.insert('', 'end', values=("(No hay asignaciones para la selección)", ""))
                
        except mysql.connector.Error as err:
            self.tabla_profesores.insert('', 'end', values=(f"Error de BD: {err}", ""))
        except Exception as e:
            self.tabla_profesores.insert('', 'end', values=(f"Error general: {e}", ""))
            
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
    
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