USE cadisoft;

-- Tabla: insc_x_seccion
DROP PROCEDURE IF EXISTS CreateTable_insc_x_seccion;

DELIMITER $$
CREATE PROCEDURE CreateTable_insc_x_seccion()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'insc_x_seccion') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `insc_x_seccion` (
            `idinsc_x_seccion` INT NOT NULL AUTO_INCREMENT,
            `idInscripcion` INT NOT NULL,
            `idSeccion` INT NOT NULL,
            PRIMARY KEY (`idinsc_x_seccion`),
            KEY `inscripcion_fk` (`idInscripcion`),
            KEY `seccion_inscripcion_fk` (`idSeccion`),
            CONSTRAINT `inscripcion_fk` FOREIGN KEY (`idInscripcion`) REFERENCES `inscripcion` (`idInscripcion`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `seccion_inscripcion_fk` FOREIGN KEY (`idSeccion`) REFERENCES `secciones` (`idSeccion`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla insc_x_seccion creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'insc_x_seccion' AND column_name = 'idinsc_x_seccion') THEN
            ALTER TABLE `insc_x_seccion` ADD COLUMN `idinsc_x_seccion` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'insc_x_seccion' AND column_name = 'idInscripcion') THEN
            ALTER TABLE `insc_x_seccion` ADD COLUMN `idInscripcion` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'insc_x_seccion' AND column_name = 'idSeccion') THEN
            ALTER TABLE `insc_x_seccion` ADD COLUMN `idSeccion` INT NOT NULL;
        END IF;
        
        -- Añadir foreign keys si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'insc_x_seccion' AND constraint_name = 'inscripcion_fk') THEN
            ALTER TABLE `insc_x_seccion` ADD CONSTRAINT `inscripcion_fk` FOREIGN KEY (`idInscripcion`) REFERENCES `inscripcion` (`idInscripcion`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'insc_x_seccion' AND constraint_name = 'seccion_inscripcion_fk') THEN
            ALTER TABLE `insc_x_seccion` ADD CONSTRAINT `seccion_inscripcion_fk` FOREIGN KEY (`idSeccion`) REFERENCES `secciones` (`idSeccion`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla insc_x_seccion ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_insc_x_seccion();
DROP PROCEDURE IF EXISTS CreateTable_insc_x_seccion;