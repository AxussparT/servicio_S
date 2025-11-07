from src.conexion import get_conexion
from tkinter import messagebox
import mysql.connector
from .Validar_materia import validar_y_registrar_materia
# IMPORTA LA NUEVA FUNCIÓN DE VALIDACIÓN
# NOTA: Asumiendo que ambas están en el mismo archivo o la importaste.
# Si están en archivos separados, asegúrate de importar correctamente la función.
# from tu_modulo_de_logica import validar_y_registrar_materia 


class materia:
    def __init__(self, clave, nombre, horas_semana, semestre):
        self.clave = clave
        self.nombre = nombre
        # Estas variables las dejo comentadas, pero puedes agregarlas si las necesitas en la BD
        '''self.grupo = grupo
        self.profesor = profesor
        self.salon = salon'''
        self.horas_semana = horas_semana
        self.semestre = semestre
        
        print(f"Datos de materia guardados en el objeto: {self.nombre}")
        
        # Llama a la nueva función de lógica de negocio
        self.procesar_datos()

    def procesar_datos(self):
        """
        Función que transfiere los datos del objeto a la función de validación y registro.
        """
        print("Enviando datos a la función de validación...")
        
        # Llama a la función externa para manejar la lógica de negocio y la DB
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

        # La clase ya no necesita manejar la conexión, commit, o cierre.
        return exito

# Nota: Debes asegurarte de que la definición de validar_y_registrar_materia (sección 1)
# esté disponible para ser importada o definida antes de la clase materia, 
# si decides mantenerlas en archivos separados.