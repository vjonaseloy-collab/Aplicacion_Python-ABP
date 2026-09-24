import mysql.connector
import os
from tabulate import tabulate

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


# ////////       CLASE ENTIDAD PADRE PARA LAS DEMAS CLASES (hijos)     ////////   

class Entidad:

    def __init__(self, db, tabla, id_col, campos):
        self.db = db
        self.tabla = tabla
        self.id_col = id_col
        self.campos = campos

    def guardar(self, valores):
        ph = ", ".join(["%s"] * len(self.campos))
        self.db.ejecutar(
            f"INSERT INTO {self.tabla} ({', '.join(self.campos)}) VALUES ({ph})",
            valores
        )

    def eliminar(self, id_val):
        self.db.ejecutar(f"DELETE FROM {self.tabla} WHERE {self.id_col} = %s", (id_val,))

    def actualizar(self, id_val, valores):
        sets = ", ".join([f"{c}=%s" for c in self.campos])
        self.db.ejecutar(
            f"UPDATE {self.tabla} SET {sets} WHERE {self.id_col} = %s",
            valores + [id_val]
        )

    def listar(self):
        return self.db.consultar(f"SELECT * FROM {self.tabla}")

    def buscar_id(self, id_val):       #"Al menos 2 búsquedas con criterios diferentes." estos dos metodos de abajo cumplen con esa parte de la consigna jijo
        return self.db.consultar(
            f"SELECT * FROM {self.tabla} WHERE {self.id_col} = %s", (id_val,) #EXACT acá la busqueda es con criterio exacto pq pide un ID especifico.
        )

    def buscar(self, columna, valor, criterio="exacto"):
        if criterio == "like":
            return self.db.consultar(
                f"SELECT * FROM {self.tabla} WHERE {columna} LIKE %s", (f"%{valor}%",) #LIKE es como... una busqueda parcial, no exacta, ya que busca valores con una parte de la informacion y te arroja todos los valores que coincidan.
            )
        return self.db.consultar(
            f"SELECT * FROM {self.tabla} WHERE {columna} = %s", (valor,)
        )

# ////////       CLASES PARA LAS TABLAS SQL     ////////   

class Producto(Entidad):
    def __init__(self, db):
        super().__init__(db, "productos", "id_producto",
                         ["nombre", "categoria", "precio", "stock"])
        
class Cliente(Entidad):
    def __init__(self, db):
        super().__init__(db, "clientes", "id_cliente",
                         ["nombre", "apellido", "telefono", "email", "direccion"])


class Empleado(Entidad):
    def __init__(self, db):
        super().__init__(db, "empleados", "id_empleado",
                         ["nombre", "apellido", "especialidad", "telefono", "email"])


class Reparacion(Entidad):
    def __init__(self, db):
        super().__init__(db, "reparaciones", "id_reparacion",
                         ["id_cliente", "id_empleado", "tipo_trabajo", "estado", "precio"])


class Transaccion(Entidad):
    def __init__(self, db):
        super().__init__(db, "transacciones", "id_transaccion",
                         ["id_empleado", "id_cliente", "id_producto", "id_reparacion", "total"])


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
    while True:
        limpiar()
        print(f"\n--- {entidad.tabla.upper()} ---")
        print("1. Alta")
        print("2. Baja")
        print("3. Modificar")
        print("4. Listar")
        print("5. Buscar por ID")
        for op, etiqueta, _, _ in busquedas:
            print(f"{op}. Buscar por {etiqueta}")
        print("0. Volver")
        op = input("Opción: ")

        if op == "1":
            valores = [input(f"{c}: ") for c in entidad.campos]
            entidad.guardar(valores)
            
        elif op == "2":
            entidad.eliminar(input("ID: "))

        elif op == "3":
            id_val = input("ID a modificar: ")
            valores = [input(f"Nuevo {c}: ") for c in entidad.campos]
            entidad.actualizar(id_val, valores)

        elif op == "4":
            mostrar(entidad.listar(), headers)

        elif op == "5":
            mostrar(entidad.buscar_id(input("ID: ")), headers)

        elif any(op == b[0] for b in busquedas):
            for b in busquedas:
                if op == b[0]:
                    _, etiqueta, columna, criterio = b
                    valor = input(f"{etiqueta}: ")
                    mostrar(entidad.buscar(columna, valor, criterio), headers)

        elif op == "0":
            break


###     Vista SQL en Python     ###

def reporte_vista(db):
    limpiar()
    print("\n--- REPORTE: REPARACIONES PENDIENTES ---") # al final hice el ejemplo que di en el documento.
    filas = db.consultar("SELECT * FROM vista_reparaciones_pendientes")
    mostrar(filas, ["ID", "Cliente", "Apellido", "Técnico", "Apellido", "Trabajo", "Precio", "Estado"])

###     Menu principal     ###

# def verificar(mensaje): # y esta funcion de virgo momo ? tkm papu
    
#     while True:
#         numero = input(mensaje)
#         if numero.isdigit():
#             numero = int(numero)
#             return numero

#         else:
#             print("El, dato ingresado no es valido, intente de nuevo.\n")

def main():
    db = Conexion()
    while True:

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
        op = input("Opción: ") #y ese verificar de virgo momo ? tkm papu
        if op == "1":
            gestionar(
                Producto(db),
                ["ID", "Nombre", "Categoría", "Precio", "Stock"],
                [("6", "nombre", "nombre", "like"),
                 ("7", "categoría", "categoria", "exacto")]
            )
        elif op == "2":
            gestionar(
                Cliente(db),
                ["ID", "Nombre", "Apellido", "Teléfono", "Email", "Dirección"],
                [("6", "email", "email", "exacto")]
            )
        elif op == "3":
            gestionar(
                Empleado(db),
                ["ID", "Nombre", "Apellido", "Especialidad", "Teléfono", "Email"],
                []
            )
        elif op == "4":
            gestionar(
                Reparacion(db),
                ["ID", "ID Cliente", "ID Empleado", "Tipo", "Estado", "Precio"],
                [("6", "estado", "estado", "exacto")]
            )
        elif op == "5":
            gestionar(
                Transaccion(db),
                ["ID", "ID Empleado", "ID Cliente", "ID Producto", "ID Reparación", "Total"],
                []
            )
        elif op == "6":
            reporte_vista(db)
        elif op == "0":
            db.cerrar()
            print("Gracias por usar el sistema!")
            break
        else:
            print("Opción inválida.")
            pausar()

if __name__ == "__main__":
    main() 
#tengo q terminar el menu todavia xd
#para eso me falta terminar la clase padre y las demas clases para reutilizar metodos jijo