import mysql.connector
from tabulate import tabulate


#comentario x jijoooo

class conexion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost", user="root", password="root124", database="ABP_bytefix"
        )
        self.cursor = self.conexion.cursor()

    def ejecutar(self, q, p=None):
        self.cursor.execute(q, p or ())
        self.conexion.commit()

    def consultar(self, q, p=None):
        self.cursor.execute(q, p or ())
        return self.cursor.fetchall()

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()


#hola mi amor

""
"""
La concha de tu madre flaco, aprender a hacer las cosas
mentira te quiero, borre el import de arriba porque salia en amarillo
no se que era pero supongo que no pasa nada
toma, te mando un troyano


Pero que wachin, me borra las librerias... :c
"""