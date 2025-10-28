from src.conexion import get_conexion
from tkinter import messagebox
import mysql.connector

class salon:
    def __init__(self, numero_aula, capacidad, tipo):
        self.numero_aula = numero_aula
        self.capacidad = capacidad
        self.tipo = tipo
        print(f"guardado en el constructor: {self.numero_aula}")
        
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
                sql = "INSERT INTO salones (salon_id, capacidad, tipo) VALUES (%s, %s, %s)"
                valores = (self.numero_aula, self.capacidad, self.tipo)
                
                cursor.execute(sql, valores)
                conexion.commit()
                
                messagebox.showinfo("Éxito", f"Salón con el número '{self.numero_aula}' guardado correctamente")
                return True
            
            except mysql.connector.Error as err:
                 messagebox.showerror("Error", f"Error al guardar los datos del salón: {err}")
                 return False
                
            finally:
                if cursor is not None:
                    cursor.close()
                if conexion is not None and conexion.is_connected():
                    conexion.close()
                    print("Conexión cerrada.")