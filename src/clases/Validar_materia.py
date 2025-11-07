from src.conexion import get_conexion
from tkinter import messagebox 
import mysql.connector

# --- 1. FUNCIÓN DE LÓGICA DE NEGOCIO (Validación y DB) ---

def validar_y_registrar_materia(clave, nombre, horas_semana, semestre):
    """
    Función que maneja la lógica de negocio (validación, INSERT y UPDATE)
    para el registro de materias.
    """
    print(f"Iniciando validación y registro para la materia: {clave} - {nombre}...")
    conexion = None 
    cursor = None
    transaccion_exitosa = False

    if not clave or not nombre:
        messagebox.showerror("Error de Datos", "La clave y el nombre de la materia no pueden estar vacíos.")
        return False

    try:
        conexion = get_conexion() 
        if conexion is None:
            messagebox.showerror("Error de Conexión", "No se pudo establecer conexión con la base de datos.")
            return False

        cursor = conexion.cursor()
        
        sql_check = "SELECT nombre FROM materias WHERE materia_id = %s"
        cursor.execute(sql_check, (clave,))
        resultado = cursor.fetchone()
        
        if resultado:
            # --- Caso: La materia YA existe (Petición de Confirmación) ---
            nombre_db = resultado[0]
            
            mensaje_confirmacion = (
                f"La materia con clave '{clave}' (**{nombre_db}**) ya está registrada.\n\n"
                f"¿Desea actualizarla con los nuevos datos)?"
            )
            
            #Preguntar al usuario si desea actualizar
            confirmar = messagebox.askyesno("Materia Existente", mensaje_confirmacion)
            
            if confirmar:
                # El usuario confirmó la actualización
                sql_update = """
                    UPDATE materias 
                    SET nombre = %s,
                        horas_semana = %s,
                        semestre = %s
                    WHERE materia_id = %s
                """
                valores_update = (nombre, horas_semana, semestre, clave)
                
                # Ejecución del UPDATE
                cursor.execute(sql_update, valores_update)
                messagebox.showinfo("Actualización Exitosa", f"actializasion completa")
                transaccion_exitosa = True
                return True
            else:
                # El usuario canceló la actualización
                messagebox.showinfo("Actualización Cancelada", f"actualización cancelada")
                return True

        else:
            # --- Caso: La materia NO existe (Alta nueva) ---
            sql_insert = """
                INSERT INTO materias (materia_id, nombre, horas_semana, semestre) 
                VALUES (%s, %s, %s, %s)
            """
            valores_insert = (clave, nombre, horas_semana, semestre)
            
            cursor.execute(sql_insert, valores_insert)
            
            messagebox.showinfo("Éxito", f"Materia con la clave '{clave}' (**{nombre}**) guardada correctamente.")
            transaccion_exitosa = True
            return True

    except mysql.connector.Error as err:
        messagebox.showerror("Error de BD", f"Error al procesar los datos de la materia: {err}")
        return False
            
    finally:
        if transaccion_exitosa and conexion is not None:
            conexion.commit()
            print("Transacción finalizada con COMMIT.")
        
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")

# --- 2. CLASE DE DATOS (Interacción) ---

class materia:
    def __init__(self, clave, nombre, horas_semana, semestre):
        self.clave = clave
        self.nombre = nombre
        self.horas_semana = horas_semana
        self.semestre = semestre
        
        print(f"Datos de materia guardados en el objeto: {self.nombre}")
        
        self.procesar_datos()

    def procesar_datos(self):
        """
        Función que transfiere los datos del objeto a la función de validación y registro.
        """
        print("Enviando datos a la función de validación...")
        
        exito = validar_y_registrar_materia(
            self.clave, 
            self.nombre, 
            self.horas_semana, 
            self.semestre
        )
        
        if exito:
            print("Registro/Actualización de materia completado con éxito.")
        else:
            print("Fallo en el registro/actualización de materia.")

        return exito