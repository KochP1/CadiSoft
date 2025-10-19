USE cadisoft;

-- Tabla: inscripcion
DROP PROCEDURE IF EXISTS CreateTable_inscripcion;

DELIMITER $$
CREATE PROCEDURE CreateTable_inscripcion()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `inscripcion` (
            `idInscripcion` INT NOT NULL AUTO_INCREMENT,
            `idusuarios` INT NOT NULL,
            `fecha_inscripcion` DATE NOT NULL,
            `fecha_expiracion` DATE NOT NULL,
            `tipo` ENUM('Privada','Inces') NOT NULL,
            `es_activa` TINYINT(1) NOT NULL DEFAULT 1,
            `asistencia` INT NULL DEFAULT 0,
            `inasistencia` INT NULL DEFAULT 0,
            PRIMARY KEY (`idInscripcion`),
            KEY `alumno_inscripcion_idx` (`idusuarios`),
            CONSTRAINT `alumno_inscripcion` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla inscripcion creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'idInscripcion') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `idInscripcion` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'idusuarios') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `idusuarios` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'fecha_inscripcion') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `fecha_inscripcion` DATE NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'fecha_expiracion') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `fecha_expiracion` DATE NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'tipo') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `tipo` ENUM('Privada','Inces') NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'es_activa') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `es_activa` TINYINT(1) NOT NULL DEFAULT 1;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'asistencia') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `asistencia` INT NULL DEFAULT 0;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND column_name = 'inasistencia') THEN
            ALTER TABLE `inscripcion` ADD COLUMN `inasistencia` INT NULL DEFAULT 0;
        END IF;
        
        -- Añadir foreign key si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'inscripcion' AND constraint_name = 'alumno_inscripcion') THEN
            ALTER TABLE `inscripcion` ADD CONSTRAINT `alumno_inscripcion` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla inscripcion ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_inscripcion();
DROP PROCEDURE IF EXISTS CreateTable_inscripcion;