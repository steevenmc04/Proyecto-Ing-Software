-- Archivo: database_mysql.sql
-- Descripcion: Script para crear base de datos y usuario en MySQL Workbench.
-- Autor: Martinez Steeven
-- Version: 1.0

-- Ejecutar este script en MySQL Workbench antes de iniciar FastAPI con DATABASE_URL de MySQL.

CREATE DATABASE IF NOT EXISTS caja_ahorros
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'usuario_caja'@'localhost' IDENTIFIED BY 'ClaveCaja123';

GRANT ALL PRIVILEGES ON caja_ahorros.* TO 'usuario_caja'@'localhost';

FLUSH PRIVILEGES;

USE caja_ahorros;

-- Las tablas no se crean manualmente aqui porque SQLAlchemy las genera al iniciar:
-- uvicorn app.main:app --reload
--
-- Luego puedes cargar datos de prueba con:
-- python seed.py
