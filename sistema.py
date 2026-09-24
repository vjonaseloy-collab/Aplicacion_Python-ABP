import mysql.connector
import os
from tabulate import tabulate


#comentario x jijoooo

class Conexion:
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

# Funciones auxiliares (principalmente para el menu)

def limpiar(): # la bosta esta hace que el menu en la terminal se limpie y solo muestre el menu actual.
    os.system("cls" if os.name == "nt" else "clear") 

def pausar(): # esto solo muestra un mensaje y al pulsar cualquier tecla o enter la funcion termina y el programa sigue.
    input("\n Presiona cualquier tecla para continuar...") # en resumen solo le da tiempo al usuario para leer lo que se mostro antes de que el programa siga, sino se borra la pantalla xd.

def mostrar(filas, headers):
    print(tabulate(filas, headers=headers, tablefmt="rounded_grid") if filas else "Sin registros.")
    pausar()

# Funcion generica que gestiona las entidades: basicamente lee la opcion que elige el usuario y ejecuta la operacion que corresponda, tmb se ejecuta hasta que el ciclo se corta.

def gestionar(entidad, headers, busquedas ): #parametros q luego usare jijo

# Menu principal

def Main():
    db = Conexion()
    while True:
        limpiar()
        print("=" * 50)
        print("   SISTEMA DE GESTIÓN    ")
        print("=" * 50)
        print("1. Productos")
        print("2. Clientes")
        print("3. Empleados")
        print("4. Reparaciones")
        print("5. Transacciones")
        print("6. Reporte: Reparaciones pendientes (vista)")
        print("0. Salir")
        print("=" * 50)
        op = input("Opción: ")
        
        #if op == "1":
            ###
            

""
"""
La concha de tu madre flaco, aprender a hacer las cosas
mentira te quiero, borre el import de arriba porque salia en amarillo
no se que era pero supongo que no pasa nada
toma, te mando un troyano


Pero que wachin, me borra las librerias... :c
"""