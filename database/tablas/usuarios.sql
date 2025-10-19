USE cadisoft;

-- Tabla: usuarios
DROP PROCEDURE IF EXISTS CreateTable_usuarios;

DELIMITER $$
CREATE PROCEDURE CreateTable_usuarios()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'usuarios') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `usuarios` (
            `idusuarios` INT NOT NULL AUTO_INCREMENT,
            `nombre` VARCHAR(12) NOT NULL,
            `segundoNombre` VARCHAR(12) NULL,
            `apellido` VARCHAR(20) NOT NULL,
            `segundoApellido` VARCHAR(20) NOT NULL,
            `cedula` VARCHAR(8) NOT NULL,
            `email` VARCHAR(50) NOT NULL,
            `contraseña` VARCHAR(200) NOT NULL,
            `rol` ENUM('administrador','profesor','alumno') NOT NULL,
            `imagen` LONGBLOB NULL,
            PRIMARY KEY (`idusuarios`),
            UNIQUE KEY `cedula` (`cedula`),
            UNIQUE KEY `email` (`email`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla usuarios creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'idusuarios') THEN
            ALTER TABLE `usuarios` ADD COLUMN `idusuarios` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'nombre') THEN
            ALTER TABLE `usuarios` ADD COLUMN `nombre` VARCHAR(12) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'segundoNombre') THEN
            ALTER TABLE `usuarios` ADD COLUMN `segundoNombre` VARCHAR(12) NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'apellido') THEN
            ALTER TABLE `usuarios` ADD COLUMN `apellido` VARCHAR(20) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'segundoApellido') THEN
            ALTER TABLE `usuarios` ADD COLUMN `segundoApellido` VARCHAR(20) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'cedula') THEN
            ALTER TABLE `usuarios` ADD COLUMN `cedula` VARCHAR(8) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'email') THEN
            ALTER TABLE `usuarios` ADD COLUMN `email` VARCHAR(50) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'contraseña') THEN
            ALTER TABLE `usuarios` ADD COLUMN `contraseña` VARCHAR(200) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'rol') THEN
            ALTER TABLE `usuarios` ADD COLUMN `rol` ENUM('administrador','profesor','alumno') NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND column_name = 'imagen') THEN
            ALTER TABLE `usuarios` ADD COLUMN `imagen` LONGBLOB NULL;
        END IF;
        
        -- Añadir constraints únicos si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND constraint_name = 'cedula') THEN
            ALTER TABLE `usuarios` ADD UNIQUE KEY `cedula` (`cedula`);
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'usuarios' AND constraint_name = 'email') THEN
            ALTER TABLE `usuarios` ADD UNIQUE KEY `email` (`email`);
        END IF;
        
        SELECT 'La tabla usuarios ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_usuarios();
DROP PROCEDURE IF EXISTS CreateTable_usuarios;