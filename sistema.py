import mysql.connector


#comentario x jijoooo

class conexion:
        
    def __init__(self):
        self.host = "localhost"
        self.usuario = "root"
        self.password = "root124"  # pone tu contraseña acá
        self.base_datos = "ABP_bytefix"
        self.conexion = None
        self.cursor = None

#hola mi amor