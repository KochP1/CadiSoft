USE cadisoft;

-- Tabla: registro_familiar
DROP PROCEDURE IF EXISTS CreateTable_registro_familiar;

DELIMITER $$
CREATE PROCEDURE CreateTable_registro_familiar()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `registro_familiar` (
            `idfamilia` INT NOT NULL AUTO_INCREMENT,
            `idusuarios` INT NOT NULL,
            `NombrePapa` VARCHAR(12) NOT NULL,
            `ApellidoPapa` VARCHAR(20) NOT NULL,
            `NombreMama` VARCHAR(12) NOT NULL,
            `ApellidoMama` VARCHAR(20) NOT NULL,
            `Telefono` VARCHAR(11) NOT NULL,
            PRIMARY KEY (`idfamilia`),
            KEY `alumno_familia_fk` (`idusuarios`),
            CONSTRAINT `alumno_familia_fk` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla registro_familiar creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND column_name = 'idfamilia') THEN
            ALTER TABLE `registro_familiar` ADD COLUMN `idfamilia` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND column_name = 'idusuarios') THEN
            ALTER TABLE `registro_familiar` ADD COLUMN `idusuarios` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND column_name = 'NombrePapa') THEN
            ALTER TABLE `registro_familiar` ADD COLUMN `NombrePapa` VARCHAR(12) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND column_name = 'ApellidoPapa') THEN
            ALTER TABLE `registro_familiar` ADD COLUMN `ApellidoPapa` VARCHAR(20) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND column_name = 'NombreMama') THEN
            ALTER TABLE `registro_familiar` ADD COLUMN `NombreMama` VARCHAR(12) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND column_name = 'ApellidoMama') THEN
            ALTER TABLE `registro_familiar` ADD COLUMN `ApellidoMama` VARCHAR(20) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND column_name = 'Telefono') THEN
            ALTER TABLE `registro_familiar` ADD COLUMN `Telefono` VARCHAR(11) NOT NULL;
        END IF;
        
        -- Añadir foreign key si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'registro_familiar' AND constraint_name = 'alumno_familia_fk') THEN
            ALTER TABLE `registro_familiar` ADD CONSTRAINT `alumno_familia_fk` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla registro_familiar ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_registro_familiar();
DROP PROCEDURE IF EXISTS CreateTable_registro_familiar;