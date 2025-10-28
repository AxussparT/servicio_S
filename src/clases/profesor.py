from src.conexion import get_conexion
from tkinter import messagebox
import mysql.connector

class profesor:
    def __init__(self, cuenta, nombre_completo, dias, hora_entrada, hora_salida, linea):
        # ... (todo tu código de __init__)
        self.cuenta = cuenta
        self.nombre_completo = nombre_completo
        self.dias = dias
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.linea = linea
        print(f"guardado en el constructor: {self.nombre_completo}")
        
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
            sql = "INSERT INTO profesores (profesor_id, nombre, disponible_inicio, disponible_fin, dias_disponibles, en_linea) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (self.cuenta, self.nombre_completo, self.hora_entrada, self.hora_salida, self.dias, self.linea)
            
            cursor.execute(sql, valores)
            conexion.commit()
            
            messagebox.showinfo("Éxito", f"Profesor con el número de cuenta '{self.cuenta}' guardado correctamente")
            return True
        
        except mysql.connector.Error as err:
             messagebox.showerror("Error", f"Error al guardar los datos del profesor: {err}")
             return False
            
        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
                print("Conexión cerrada.")