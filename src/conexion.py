import mysql.connector
from tkinter import messagebox

def get_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOLOyolo89",
            database="Escuela",
            port='3306'
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

