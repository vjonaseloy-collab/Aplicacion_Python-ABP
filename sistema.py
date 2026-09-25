
# ABP Integrador: Programación I / BD II - Entrega 2
import mysql.connector
import os
from tabulate import tabulate

#CONEXION A SQL

class Conexion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost", user="root", password="root1024", database="ABP_bytefix"
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
    """Clase base para todas las entidades del sistema."""

    def __init__(self, db, tabla, id_col, campos):
        self.db = db
        self.tabla = tabla
        self.id_col = id_col
        self.campos = campos

    def guardar(self, valores):
        try:
            ph = ", ".join(["%s"] * len(self.campos))
            self.db.ejecutar(
                f"INSERT INTO {self.tabla} ({', '.join(self.campos)}) VALUES ({ph})",
                valores
            )
            print(f"\n Registro agregado correctamente en '{self.tabla}'.")
        except mysql.connector.Error as e:
            print(f"\n Error al agregar: {e}")
        pausar()

    def eliminar(self, id_val):
        try:
            self.db.ejecutar(f"DELETE FROM {self.tabla} WHERE {self.id_col} = %s", (id_val,))
            print(f"\n Registro con ID {id_val} eliminado de '{self.tabla}'.")
        except mysql.connector.Error as e:
            print(f"\n Error al eliminar: {e}")
        pausar()

    def actualizar(self, id_val, valores):
        try:
            sets = ", ".join([f"{c}=%s" for c in self.campos])
            self.db.ejecutar(
                f"UPDATE {self.tabla} SET {sets} WHERE {self.id_col} = %s",
                valores + [id_val]
            )
            print(f"\n Registro con ID {id_val} modificado en '{self.tabla}'.")
        except mysql.connector.Error as e:
            print(f"\n Error al modificar: {e}")
        pausar()

    def listar(self):
        return self.db.consultar(f"SELECT * FROM {self.tabla}")

    def buscar_id(self, id_val):  #"Al menos 2 búsquedas con criterios diferentes." estos dos metodos de abajo cumplen con esa parte de la consigna.
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

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")  # type: ignore


def pausar():
    input("\nPresione ENTER para continuar...")


def mostrar(filas, headers):
    """Muestra una tabla formateada con tabulate."""
    limpiar()
    if not filas:
        print("No se encontraron registros.")
    else:
        print(tabulate(filas, headers=headers, tablefmt="grid"))
    pausar()



# Valicdaciones por entidad para categoria, estado, email, etc. 
# Esto lo agregue por lo que dijiste que te exploto el sistema al pasarle una categoria invalida jajaja

def pedir_campos(entidad):
    """Pide los campos al usuario con validaciones específicas."""
    valores = []
    for c in entidad.campos:
        if c == "categoria":
            print("\nCategorías permitidas: hardware, software, periferico")
            while True:
                val = input(f"{c}: ").strip().lower()
                if val in ["hardware", "software", "periferico"]:
                    valores.append(val)
                    break
                print(" Categoría inválida. Intente de nuevo.")

        elif c == "estado":
            print("\nEstados permitidos: pendiente, finalizada")
            while True:
                val = input(f"{c}: ").strip().lower()
                if val in ["pendiente", "finalizada"]:
                    valores.append(val)
                    break
                print(" Estado inválido. Intente de nuevo.")

        elif c == "email":
            while True:
                val = input(f"{c}: ").strip()
                if "@" in val and "." in val:
                    valores.append(val)
                    break
                print(" Email inválido. Debe contener '@' y '.'.")

        elif c in ["precio", "total"]:
            while True:
                try:
                    val = float(input(f"{c}: "))
                    valores.append(val)
                    break
                except ValueError:
                    print(" Debe ingresar un número válido.")

        elif c == "stock":
            while True:
                try:
                    val = int(input(f"{c}: "))
                    valores.append(val)
                    break
                except ValueError:
                    print(" Debe ingresar un número entero.")

        elif c in ["id_cliente", "id_empleado", "id_producto", "id_reparacion"]:
            val = input(f"{c} (o vacío): ").strip()
            valores.append(val if val else None)

        else:
            while True:
                val = input(f"{c}: ").strip()
                if val:
                    valores.append(val)
                    break
                print(f" El campo '{c}' no puede estar vacío.")
    return valores



# Funcion generica que gestiona las entidades: basicamente lee la opcion que elige el usuario y ejecuta la operacion que corresponda, tmb se ejecuta hasta que el ciclo se corta.

def gestionar(entidad, headers, busquedas):
    while True:
        limpiar()
        print(f"\n--- GESTIÓN DE {entidad.tabla.upper()} ---")
        print("1. Alta")
        print("2. Baja")
        print("3. Modificar")
        print("4. Listar")
        print("5. Buscar por ID")
        for op, etiqueta, _, _ in busquedas:
            print(f"{op}. Buscar por {etiqueta}")
        print("0. Volver")
        op = pedir_opcion()

        if op == "1":
            limpiar()
            print(f"\n--- ALTA DE {entidad.tabla.upper()} ---")
            valores = pedir_campos(entidad)
            entidad.guardar(valores)

        elif op == "2":
            limpiar()
            print(f"\n--- BAJA DE {entidad.tabla.upper()} ---")
            entidad.eliminar(input("ID a eliminar: "))

        elif op == "3":
            limpiar()
            print(f"\n--- MODIFICAR {entidad.tabla.upper()} ---")
            id_val = input("ID a modificar: ")
            valores = pedir_campos(entidad)
            entidad.actualizar(id_val, valores)

        elif op == "4":
            mostrar(entidad.listar(), headers)

        elif op == "5":
            limpiar()
            print(f"\n--- BUSCAR {entidad.tabla.upper()} POR ID ---")
            mostrar(entidad.buscar_id(input("ID: ")), headers)

        elif any(op == b[0] for b in busquedas):
            for b in busquedas:
                if op == b[0]:
                    _, etiqueta, columna, criterio = b
                    limpiar()
                    print(f"\n--- BUSCAR {entidad.tabla.upper()} POR {etiqueta.upper()} ---")
                    valor = input(f"{etiqueta}: ")
                    mostrar(entidad.buscar(columna, valor, criterio), headers)

        elif op == "0":
            break
        else:
            print("Opción inválida.")
            pausar()



###     Vista SQL en Python     ###

def reporte_vista(db):
    limpiar()
    print("\n--- REPORTE: REPARACIONES PENDIENTES ---")
    filas = db.consultar("SELECT * FROM vista_reparaciones_pendientes")
    mostrar(filas, ["ID", "Cliente", "Apellido", "Técnico", "Apellido", "Trabajo", "Precio", "Estado"])


# validador de opcion (debe ser solo entero)

def pedir_opcion():
    """Pide una opción y valida que sea un número."""
    while True:
        op = input("Opción: ").strip()
        if op.isdigit():
            return op
        print("Debe ingresar un número válido.")

# MENÚ PRINCIPAL

def main():
    db = Conexion()
    while True:
        limpiar()
        print("=" * 50)
        print("   SISTEMA DE GESTIÓN - BYTEFIX")
        print("=" * 50)
        print("1. Productos")
        print("2. Clientes")
        print("3. Empleados")
        print("4. Reparaciones")
        print("5. Transacciones")
        print("6. Reporte: Reparaciones pendientes (vista)")
        print("0. Salir")
        print("=" * 50)
        op = pedir_opcion()

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