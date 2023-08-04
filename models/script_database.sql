CREATE DATABASE recetario;

USE recetario;

CREATE TABLE IF NOT EXISTS recetas (
    id_receta INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    nombre_receta VARCHAR(80) NOT NULL UNIQUE,
    tiempo_coccion TINYINT NOT NULL,
    tiempo_preparacion TINYINT NOT NULL,
    creacion  DATETIME NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingredientes (
    id_ingrediente INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    nombre_ing VARCHAR(50) NOT NULL UNIQUE,
    unidad VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS ingrediente_receta (
    id_ing_receta INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
    id_receta INT UNSIGNED NOT NULL,
    id_ingrediente INT UNSIGNED NOT NULL,
    cantidad FLOAT NOT NULL,
    CONSTRAINT receta_fk FOREIGN KEY (id_receta)
    REFERENCES recetas (id_receta),
    CONSTRAINT ingredientes_fk FOREIGN KEY (id_ingrediente)
    REFERENCES ingredientes (id_ingrediente)
);