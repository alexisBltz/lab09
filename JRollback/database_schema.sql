-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS laboratorio_rollback;

-- Usar la base de datos
USE laboratorio_rollback;

-- Estructura de tabla para la tabla 'mitabla'
CREATE TABLE IF NOT EXISTS mitabla (
    DNI varchar(12) DEFAULT NULL,
    correo varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Estructura de tabla para la tabla 'miotratabla'
CREATE TABLE IF NOT EXISTS miotratabla (
    nombre varchar(20) DEFAULT NULL,
    apellido varchar(20) DEFAULT NULL,
    edad int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- IMPORTANTE: Se utiliza ENGINE=InnoDB y no MyISAM porque InnoDB tiene
-- soporte para transacciones, bloqueo de registros y nos permite tener 
-- las características ACID garantizando la integridad de nuestras tablas.
