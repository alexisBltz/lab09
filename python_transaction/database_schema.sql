-- Crear la base de datos para la tienda de productos alimenticios
CREATE DATABASE IF NOT EXISTS tienda_alimenticia;

-- Usar la base de datos
USE tienda_alimenticia;

-- Tabla de productos alimenticios
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de ventas (cabecera)
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    estado VARCHAR(20) DEFAULT 'completada',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de detalle de ventas
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertar algunos productos de ejemplo
INSERT INTO productos (nombre, categoria, precio, stock) VALUES
('Arroz Blanco 1kg', 'Granos', 2.50, 100),
('Frijoles Negros 500g', 'Granos', 1.80, 80),
('Aceite de Cocina 1L', 'Aceites', 3.20, 50),
('Azúcar Blanca 1kg', 'Endulzantes', 1.50, 120),
('Sal de Mesa 500g', 'Condimentos', 0.80, 200),
('Leche Entera 1L', 'Lácteos', 1.20, 60),
('Pan Integral', 'Panadería', 2.00, 30),
('Huevos x12', 'Proteínas', 2.80, 40);

-- Insertar algunos clientes de ejemplo
INSERT INTO clientes (nombre, email, telefono) VALUES
('Juan Pérez', 'juan.perez@email.com', '555-1234'),
('María García', 'maria.garcia@email.com', '555-5678'),
('Carlos López', 'carlos.lopez@email.com', '555-9012');

-- IMPORTANTE: Se utiliza ENGINE=InnoDB porque:
-- 1. Soporta transacciones ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad)
-- 2. Permite rollback en caso de errores
-- 3. Maneja bloqueo de registros para concurrencia
-- 4. Garantiza la integridad referencial con foreign keys
