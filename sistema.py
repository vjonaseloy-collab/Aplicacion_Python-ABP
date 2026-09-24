import mysql.connector

class conexion:
        
    def __init__(self):
        self.host = "localhost"
        self.usuario = "root"
        self.password = "root"  # pone tu contraseña acá
        self.base_datos = "ABP_bytefix"
        self.conexion = None
        self.cursor = None


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