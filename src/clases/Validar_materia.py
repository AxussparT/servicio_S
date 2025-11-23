from src.conexion import get_conexion
from tkinter import messagebox
import mysql.connector

def validar_y_registrar_materia(clave, nombre, horas_semana, semestre):
    """
    Función que maneja la lógica de validación, INSERT y UPDATE para materias.
    """
    print(f"Iniciando registro/actualización para: {clave} - {nombre}...")
    conexion = None 
    cursor = None
    transaccion_exitosa = False

    # Prepara y limpia las variables de entrada
    clave = str(clave).strip()
    nombre = str(nombre).strip()
    horas_semana_str = str(horas_semana).strip()
    
    # Asigna el ID del semestre o None si el valor no es un dígito
    semestre_id = int(semestre) if str(semestre).strip().isdigit() else None
    
    # Validación simple de campos obligatorios
    if not clave or not nombre:
        messagebox.showerror("Error de Datos", "La clave y el nombre de la materia no pueden estar vacíos.")
        return False

    try:
        conexion = get_conexion() 
        if conexion is None:
            messagebox.showerror("Error de Conexión", "No se pudo establecer conexión con la base de datos.")
            return False

        cursor = conexion.cursor()
        
        # 1. BÚSQUEDA: Verificar si la materia ya existe usando la clave
        sql_check = "SELECT nombre FROM materias WHERE materia_id = %s"
        cursor.execute(sql_check, (clave,))
        resultado = cursor.fetchone()
        
        if resultado:
            # --- Materia YA existe: Preguntar para actualizar ---
            nombre_db = resultado[0]
            
            mensaje_confirmacion = (
                f"La materia con clave '{clave}' ({nombre_db}) ya está registrada.\n\n"
                f"¿Desea actualizarla con los nuevos datos?"
            )
            
            # Pedir confirmación al usuario (askyesno devuelve True/False)
            if messagebox.askyesno("Materia Existente", mensaje_confirmacion):
                # El usuario confirmó la actualización
                sql_update = """
                    UPDATE materias 
                    SET nombre = %s,
                        horas_semana = %s,
                        semestre_id = %s
                    WHERE materia_id = %s
                """
                # Se utiliza el ID numérico del semestre o None
                valores_update = (nombre, horas_semana_str, semestre_id, clave) 
                
                cursor.execute(sql_update, valores_update)
                messagebox.showinfo("Actualización Exitosa", f"Actualización completa.")
                transaccion_exitosa = True
                return True
            else:
                # El usuario canceló la actualización
                messagebox.showinfo("Actualización Cancelada", f"Actualización cancelada.")
                return True

        else:
            # --- Materia NO existe: Insertar nuevo registro ---
            sql_insert = """
                INSERT INTO materias (materia_id, nombre, horas_semana, semestre_id) 
                VALUES (%s, %s, %s, %s)
            """
            # Se utiliza el ID numérico del semestre o None
            valores_insert = (clave, nombre, horas_semana_str, semestre_id)
            
            cursor.execute(sql_insert, valores_insert)
            
            messagebox.showinfo("Éxito", f"Materia con la clave '{clave}' ({nombre}) guardada correctamente.")
            transaccion_exitosa = True
            return True

    except mysql.connector.Error as err:
        # Manejo de errores de base de datos (ej. violación de FK, formato incorrecto)
        messagebox.showerror("Error de BD", f"Error al procesar los datos de la materia: {err}")
        return False
            
    finally:
        # Asegurar el COMMIT si la operación fue exitosa
        if transaccion_exitosa and conexion is not None:
            conexion.commit()
            print("Transacción finalizada con COMMIT.")
        
        # Cerrar recursos
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")