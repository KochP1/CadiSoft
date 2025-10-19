USE cadisoft;

-- Tabla: calificaciones
DROP PROCEDURE IF EXISTS CreateTable_calificaciones;

DELIMITER $$
CREATE PROCEDURE CreateTable_calificaciones()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `calificaciones` (
            `idCalificacion` INT NOT NULL AUTO_INCREMENT,
            `idusuarios` INT NOT NULL,
            `idSeccion` INT NOT NULL,
            `idInscripcion` INT NOT NULL,
            `logro_1` DOUBLE NULL DEFAULT 0,
            `logro_2` DOUBLE NULL DEFAULT 0,
            `logro_3` DOUBLE NULL DEFAULT 0,
            `logro_4` DOUBLE NULL DEFAULT 0,
            `logro_5` DOUBLE NULL DEFAULT 0,
            `definitiva` DOUBLE NULL DEFAULT 0,
            `aprobado` TINYINT(1) NULL DEFAULT 0,
            PRIMARY KEY (`idCalificacion`),
            KEY `curso_fk_idx` (`idSeccion`),
            KEY `alumno_fk_idx` (`idusuarios`),
            KEY `inscripcion_calificacion_fk` (`idInscripcion`),
            CONSTRAINT `alumno_fk` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `inscripcion_calificacion_fk` FOREIGN KEY (`idInscripcion`) REFERENCES `inscripcion` (`idInscripcion`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `seccion_fk` FOREIGN KEY (`idSeccion`) REFERENCES `secciones` (`idSeccion`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla calificaciones creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'idCalificacion') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `idCalificacion` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'idusuarios') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `idusuarios` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'idSeccion') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `idSeccion` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'idInscripcion') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `idInscripcion` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'logro_1') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `logro_1` DOUBLE NULL DEFAULT 0;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'logro_2') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `logro_2` DOUBLE NULL DEFAULT 0;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'logro_3') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `logro_3` DOUBLE NULL DEFAULT 0;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'logro_4') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `logro_4` DOUBLE NULL DEFAULT 0;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'logro_5') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `logro_5` DOUBLE NULL DEFAULT 0;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'definitiva') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `definitiva` DOUBLE NULL DEFAULT 0;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND column_name = 'aprobado') THEN
            ALTER TABLE `calificaciones` ADD COLUMN `aprobado` TINYINT(1) NULL DEFAULT 0;
        END IF;
        
        -- Añadir foreign keys si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND constraint_name = 'alumno_fk') THEN
            ALTER TABLE `calificaciones` ADD CONSTRAINT `alumno_fk` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND constraint_name = 'inscripcion_calificacion_fk') THEN
            ALTER TABLE `calificaciones` ADD CONSTRAINT `inscripcion_calificacion_fk` FOREIGN KEY (`idInscripcion`) REFERENCES `inscripcion` (`idInscripcion`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'calificaciones' AND constraint_name = 'seccion_fk') THEN
            ALTER TABLE `calificaciones` ADD CONSTRAINT `seccion_fk` FOREIGN KEY (`idSeccion`) REFERENCES `secciones` (`idSeccion`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla calificaciones ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_calificaciones();
DROP PROCEDURE IF EXISTS CreateTable_calificaciones;