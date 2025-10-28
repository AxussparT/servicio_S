from src.conexion import get_conexion
from tkinter import messagebox
import mysql.connector

class materia:
    def __init__(self, clave, nombre, grupo, profesor, horas_semana, semestre, salon):
        self.clave = clave
        self.nombre = nombre
        self.grupo = grupo
        self.profesor = profesor
        self.horas_semana = horas_semana
        self.semestre = semestre
        self.salon = salon
        print(f"guardado en el constructor: {self.nombre}")
        
        # Esta línea ya está correcta
        self.procesar_datos()

    def procesar_datos(self):
        print("Subiendo datos a la base de datos...")
        conexion = None # Variable local
        cursor = None
        
        try:
            # 2. ¡AQUÍ ESTÁ LA CORRECCIÓN!
            # Llama a la función 'get_conexion()' que importaste
            conexion = get_conexion() 
            
            # Si la conexión falló (ej. DB apagada), get_conexion() retorna None
            if conexion is None:
                print("Error: No se pudo obtener conexión.")
                return False

            cursor = conexion.cursor()
            
            # ... (el resto de tu código SQL) ...
            sql = "INSERT INTO materias (materia_id, nombre, horas_semana) VALUES (%s, %s, %s)"
            valores = (self.clave, self.nombre, self.horas_semana)
            
            cursor.execute(sql, valores)
            conexion.commit()
            
            messagebox.showinfo("Éxito", f"Materia con la clave '{self.clave}' guardada correctamente")
            return True
        
        except mysql.connector.Error as err:
             messagebox.showerror("Error", f"Error al guardar los datos de la materia: {err}")
             return False
            
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
                print("Conexión cerrada.")