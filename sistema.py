import mysql.connector
import os
#from tabulate import tabulate

#CONEXION A SQL

class Conexion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost", user="root", password="root", database="ABP_bytefix"
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

# ////////       CLASES PARA LAS TABLAS SQL     ////////   

class Producto:

    def __init__(self,id_producto,nombre,categoria,precio,stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    #metodo para getear

    def get_producto(self):
        pass
        #ver de traer el producto con SQL

    #metodo para setear(modificar)

    def set_producto(self):
        pass

class Clientes:

    def __init__(self,id_cliente,nombre,apellido,telefono,email,direccion):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

class Empleados:

    def __init__(self,id_empleado,nombre,apellido,telefono,email,especialidad):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email


class Reparacion:

    def __init__(self,id_reparacion,id_cliente,id_empleado,tipo_trabajo,estado,precio):
        self.id_reparacion = id_reparacion
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
        self.tipo_trabajo = tipo_trabajo
        self.estado = estado
        self.precio = precio

class Transacciones:

    def __init__(self,id_transaccion,id_empleado,id_cliente,id_producto,id_reparacion,total):
        self.id_transaccion = id_transaccion
        self.id_empleado = id_empleado
        self.id_cliente = id_cliente
        self.id_producto = id_producto
        self.id_reparacion = id_reparacion
        self.total = total

# Funciones auxiliares (principalmente para el menu)

def limpiar(): # la bosta esta hace que el menu en la terminal se limpie y solo muestre el menu actual.
    os.system("cls" if os.name == "nt" else "clear") 

def pausar(): # esto solo muestra un mensaje y al pulsar cualquier tecla o enter la funcion termina y el programa sigue.
    input("\n Presiona cualquier tecla para continuar...") # en resumen solo le da tiempo al usuario para leer lo que se mostro antes de que el programa siga, sino se borra la pantalla xd.

def mostrar(filas, headers):
    #print(tabulate(filas, headers=headers, tablefmt="rounded_grid") if filas else "Sin registros.")
    #pausar()
    pass

# Funcion generica que gestiona las entidades: basicamente lee la opcion que elige el usuario y ejecuta la operacion que corresponda, tmb se ejecuta hasta que el ciclo se corta.

def gestionar(entidad, headers, busquedas ): #parametros q luego usare jijo
    pass
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
            
"""
Estan mergeados los dos ahora we
"""
