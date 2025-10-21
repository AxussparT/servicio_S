import sqlite3
import os

DB_FILE="data/Dump20251015.bd"

def conectar():
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        conn=sqlite3.connect(DB_FILE)
        print("Conexion exitosa '{DB_FILE}'")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None