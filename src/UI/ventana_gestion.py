import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# from src.clases.salon import salon # Descomenta si lo necesitas
from PIL import Image, ImageTk

class VentanaGestion:
    def __init__(self, master_window):
        
        #ESTILOS
        estilo =ttk.Style()
        estilo.configure('blue.TFrame', background='#0A0F1E')
        
        # 1. CREACIÓN DE LA VENTANA
        # La nueva ventana se llama 'self.ventana'
        self.ventana = tk.Toplevel(master_window)
        self.ventana.title("Ventana de Gestión")
        
        # --- CORRECCIÓN 1 ---
        # Usa 'self.ventana', no 'self.master'
        self.ventana.state('zoomed')
        
        self.ventana.grab_set()  
        self.ventana.transient(master_window) 
        
        # 2. CARGA DE LA IMAGEN DE FONDO
        try:
            image = Image.open(r"assets/fondo.png")
            self.original_image = image
            
            # --- CORRECCIÓN 2 ---
            # El padre del Label es 'self.ventana'
            self.background_label = tk.Label(self.ventana)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # --- CORRECCIÓN 3 ---
            # El evento 'bind' se aplica a 'self.ventana'
            self.ventana.bind("<Configure>", self.redimensionar_fondo)
            
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            # --- CORRECCIÓN 4 ---
            # El 'config' de fallback es para 'self.ventana'
            self.ventana.config(bg="grey")
            
        # 3. CREACIÓN DE COMPONENTES
        # (Esto se movió fuera del 'except' para que siempre se ejecute)
        
        # El padre del frame es 'self.ventana'
        # --- ERROR CORREGIDO: Cambiado de tk.Frame a ttk.Frame ---
        self.frame_principal = ttk.Frame(self.ventana, borderwidth=0, relief="solid", style='blue.TFrame')
        
        # --- CAMBIO PARA CENTRAR EL FRAME ---
        # En lugar de .pack(), usamos .place() para centrar el frame
        # self.frame_principal.pack(fill='both', expand=True, padx=50, pady=50) 
        
        # Definimos un ancho y alto para el frame (ajusta según necesites)
        frame_ancho = 1100
        frame_alto = 700
        
        # Colocamos el frame en el centro de la ventana
        # relx=0.5, rely=0.5 -> Posiciona en el 50% horizontal y 50% vertical
        # anchor='center' -> Indica que el punto (relx, rely) es el CENTRO del frame
        self.frame_principal.place(relx=0.5, rely=0.5, anchor='center', width=frame_ancho, height=frame_alto)
        
        
        # --- CORRECCIÓN DE CONSISTENCIA: Cambiado de tk.Button a ttk.Button ---
        boton_cerrar = ttk.Button(self.frame_principal, text="Cerrar", command=self.ventana.destroy)
        boton_cerrar.pack(pady=20)
        
        # 4. ESPERAR CIERRE
        self.ventana.wait_window() 
        
    # --- CORRECCIÓN 5 ---
    # Este método faltaba en tu clase
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