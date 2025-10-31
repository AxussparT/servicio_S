from src.conexion import get_conexion
from tkinter import messagebox
import mysql.connector
from .validacion_bd import validar_y_registrar_profesor 


class profesor:
    def __init__(self, cuenta, nombre_completo, dias, hora_entrada, hora_salida, linea):
        self.cuenta = cuenta
        self.nombre_completo = nombre_completo
        self.dias = str(dias) if dias is not None else ""
        
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.linea = linea 
        
        print(f"guardado en el constructor: {self.nombre_completo}")
        self.procesar_datos()

    def procesar_datos(self):
        """
        Método que DELEGA toda la lógica de validación e interacción con la BD 
        a la función externa.
        """
        print("Llamando a la validación de la base de datos...")
        
        exito = validar_y_registrar_profesor(
            self.cuenta, 
            self.nombre_completo, 
            self.dias, 
            self.hora_entrada, 
            self.hora_salida, 
            self.linea
        )
        return exito