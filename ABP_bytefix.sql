CREATE DATABASE ABP_bytefix;
USE ABP_bytefix;

-- EMPLEADOS
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

-- CLIENTES
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    direccion VARCHAR(200)
);

-- PRODUCTOS
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria ENUM('hardware', 'software', 'periferico') NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
);

-- REPARACIONES

CREATE TABLE reparaciones (
    id_reparacion INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    tipo_trabajo VARCHAR(100) NOT NULL,
    estado ENUM('pendiente', 'finalizada') DEFAULT 'pendiente',
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

-- TRANSACCIONES
CREATE TABLE transacciones (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    id_cliente INT NOT NULL,
    id_producto INT NULL,
    id_reparacion INT NULL,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_reparacion) REFERENCES reparaciones(id_reparacion)
);

-- datos de prueba

-- Vista SQL
CREATE OR REPLACE VIEW vista_reparaciones_pendientes AS
SELECT 
    r.id_reparacion,
    c.nombre AS cliente,
    c.apellido AS apellido_cliente,
    e.nombre AS tecnico,
    e.apellido AS apellido_tecnico,
    r.tipo_trabajo,
    r.precio,
    r.estado
FROM reparaciones r
JOIN clientes c ON r.id_cliente = c.id_cliente
JOIN empleados e ON r.id_empleado = e.id_empleado
WHERE r.estado = 'pendiente';

-- EMPLEADOS 
INSERT INTO empleados (nombre, apellido, especialidad, telefono, email) VALUES
('Carlos', 'Gómez', 'Hardware', '11111111', 'carlos@bytefix.com'),
('Ana', 'Martínez', 'Software', '22222222', 'ana@bytefix.com'),
('Luis', 'Pérez', 'Redes', '33333333', 'luis@bytefix.com'),
('María', 'López', 'Hardware', '44444444', 'maria@bytefix.com'),
('Jorge', 'Ramírez', 'Software', '55555555', 'jorge@bytefix.com');

-- CLIENTES (10 registros)

INSERT INTO clientes (nombre, apellido, telefono, email, direccion) VALUES
('Pedro', 'García', '10101010', 'pedro@mail.com', 'Calle 1 N° 123'),
('Lucía', 'Fernández', '20202020', 'lucia@mail.com', 'Calle 2 N° 456'),
('Miguel', 'Torres', '30303030', 'miguel@mail.com', 'Calle 3 N° 789'),
('Sofía', 'Castro', '40404040', 'sofia@mail.com', 'Calle 4 N° 101'),
('Diego', 'Ortiz', '50505050', 'diego@mail.com', 'Calle 5 N° 112'),
('Elena', 'Rojas', '60606060', 'elena@mail.com', 'Calle 6 N° 131'),
('Pablo', 'Mendoza', '70707070', 'pablo@mail.com', 'Calle 7 N° 415'),
('Laura', 'Silva', '80808080', 'laura@mail.com', 'Calle 8 N° 161'),
('Andrés', 'Vega', '90909090', 'andres@mail.com', 'Calle 9 N° 718'),
('Valentina', 'Díaz', '11111112', 'valentina@mail.com', 'Calle 10 N° 192');

-- PRODUCTOS (10 registros)
INSERT INTO productos (nombre, categoria, precio, stock) VALUES
('Intel i7-12700K', 'hardware', 420.00, 15),
('AMD Ryzen 7 5800X', 'hardware', 390.00, 12),
('NVIDIA RTX 3060', 'hardware', 500.00, 8),
('Microsoft Windows 11', 'software', 150.00, 25),
('Logitech MX Master 3', 'periferico', 110.00, 20),
('Teclado Mecánico RGB', 'periferico', 70.00, 18),
('SSD 1TB NVMe', 'hardware', 130.00, 10),
('Office 2021', 'software', 250.00, 15),
('Monitor LG 24"', 'periferico', 200.00, 7),
('Fuente 750W', 'hardware', 100.00, 9);

-- REPARACIONES (15 registros)
INSERT INTO reparaciones (id_cliente, id_empleado, tipo_trabajo, estado, precio) VALUES
(1, 1, 'Cambio de fuente', 'finalizada', 150.00),
(2, 2, 'Instalación de SO', 'finalizada', 120.00),
(3, 3, 'Configuración de red', 'finalizada', 100.00),
(4, 1, 'Limpieza interna', 'finalizada', 80.00),
(5, 2, 'Recuperación de datos', 'finalizada', 250.00),
(6, 3, 'Revisión de seguridad', 'finalizada', 130.00),
(7, 1, 'Cambio de pasta térmica', 'finalizada', 70.00),
(8, 2, 'Eliminación de virus', 'finalizada', 110.00),
(9, 3, 'Configuración de impresora', 'finalizada', 95.00),
(10, 1, 'Cambio de RAM', 'finalizada', 90.00),
(1, 2, 'Actualización de BIOS', 'pendiente', 80.00),
(2, 3, 'Problemas de conectividad', 'pendiente', 120.00),
(3, 1, 'Ruido en ventilador', 'pendiente', 110.00),
(4, 2, 'Pantalla azul', 'pendiente', 160.00),
(5, 3, 'Reinstalación de drivers', 'pendiente', 70.00);


-- NOTITA(curioso fusionar 2 tablas): 
-- por que seria curioso? es jorge
-- - Si id_producto NO es NULL → es VENTA
-- - Si id_reparacion NO es NULL → es REPARACION

-- VENTAS
INSERT INTO transacciones (id_empleado, id_cliente, id_producto, id_reparacion, total) VALUES
-- Empleado 1 (Carlos) - 10 ventas por ejemplo, para poner algo.
(1, 1, 1, NULL, 420.00),
(1, 2, 2, NULL, 390.00),
(1, 3, 3, NULL, 500.00),
(1, 4, 4, NULL, 150.00),
(1, 5, 5, NULL, 110.00),
(1, 6, 6, NULL, 70.00),
(1, 7, 7, NULL, 130.00),
(1, 8, 8, NULL, 250.00),
(1, 9, 9, NULL, 200.00),
(1, 10, 10, NULL, 100.00),

-- Empleado 2 (Ana) - 10 ventas etc
(2, 1, 2, NULL, 390.00),
(2, 2, 3, NULL, 500.00),
(2, 3, 4, NULL, 150.00),
(2, 4, 5, NULL, 110.00),
(2, 5, 6, NULL, 70.00),
(2, 6, 7, NULL, 130.00),
(2, 7, 8, NULL, 250.00),
(2, 8, 9, NULL, 200.00),
(2, 9, 10, NULL, 100.00),
(2, 10, 1, NULL, 420.00),

-- Empleado 3 (Luis) - 10 ventas etc
(3, 1, 3, NULL, 500.00),
(3, 2, 4, NULL, 150.00),
(3, 3, 5, NULL, 110.00),
(3, 4, 6, NULL, 70.00),
(3, 5, 7, NULL, 130.00),
(3, 6, 8, NULL, 250.00),
(3, 7, 9, NULL, 200.00),
(3, 8, 10, NULL, 100.00),
(3, 9, 1, NULL, 420.00),
(3, 10, 2, NULL, 390.00),

-- Empleado 4 (María) - 5 ventas etc
(4, 1, 4, NULL, 150.00),
(4, 2, 5, NULL, 110.00),
(4, 3, 6, NULL, 70.00),
(4, 4, 7, NULL, 130.00),
(4, 5, 8, NULL, 250.00),

-- Empleado 5 (Jorge, el que es curioso) - 5 ventas etc
(5, 6, 9, NULL, 200.00),
(5, 7, 10, NULL, 100.00),
(5, 8, 1, NULL, 420.00),
(5, 9, 2, NULL, 390.00),
(5, 10, 3, NULL, 500.00),

-- REPARACIONES (15 registros)
(1, 1, NULL, 1, 150.00),
(2, 2, NULL, 2, 120.00),
(3, 3, NULL, 3, 100.00),
(1, 4, NULL, 4, 80.00),
(2, 5, NULL, 5, 250.00),
(3, 6, NULL, 6, 130.00),
(1, 7, NULL, 7, 70.00),
(2, 8, NULL, 8, 110.00),
(3, 9, NULL, 9, 95.00),
(1, 10, NULL, 10, 90.00),
(2, 1, NULL, 11, 80.00),
(3, 2, NULL, 12, 120.00),
(1, 3, NULL, 13, 110.00),
(2, 4, NULL, 14, 160.00),
(3, 5, NULL, 15, 70.00);

