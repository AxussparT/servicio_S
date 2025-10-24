class profesor:
    # El constructor empieza aquí
    def __init__(self, nombre, apellido, dias, hora_entrada, hora_salida, linea):
        # Todo lo que está aquí DENTRO debe ir indentado

        print("guardando datos")
        self.nombre = nombre
        self.apellido = apellido
        self.dias = dias
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.linea = linea
        print("guardado del maestro exitoso")
        print(f"guardado en el constructor: {self.nombre} {self.apellido}")
    #def procesar_datos(self):
        