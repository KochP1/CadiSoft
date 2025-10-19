USE cadisoft;

-- Tabla: horario_x_curso
DROP PROCEDURE IF EXISTS CreateTable_horario_x_curso;

DELIMITER $$
CREATE PROCEDURE CreateTable_horario_x_curso()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'horario_x_curso') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `horario_x_curso` (
            `idhorario_x_curso` INT NOT NULL AUTO_INCREMENT,
            `idhorario` INT NOT NULL,
            `idSeccion` INT NOT NULL,
            PRIMARY KEY (`idhorario_x_curso`),
            KEY `horario_fk_idx` (`idhorario`),
            KEY `seccion_horario_fk` (`idSeccion`),
            CONSTRAINT `horario_fk` FOREIGN KEY (`idhorario`) REFERENCES `horario` (`idhorario`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `seccion_horario_fk` FOREIGN KEY (`idSeccion`) REFERENCES `secciones` (`idSeccion`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla horario_x_curso creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario_x_curso' AND column_name = 'idhorario_x_curso') THEN
            ALTER TABLE `horario_x_curso` ADD COLUMN `idhorario_x_curso` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario_x_curso' AND column_name = 'idhorario') THEN
            ALTER TABLE `horario_x_curso` ADD COLUMN `idhorario` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario_x_curso' AND column_name = 'idSeccion') THEN
            ALTER TABLE `horario_x_curso` ADD COLUMN `idSeccion` INT NOT NULL;
        END IF;
        
        -- Añadir foreign keys si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'horario_x_curso' AND constraint_name = 'horario_fk') THEN
            ALTER TABLE `horario_x_curso` ADD CONSTRAINT `horario_fk` FOREIGN KEY (`idhorario`) REFERENCES `horario` (`idhorario`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'horario_x_curso' AND constraint_name = 'seccion_horario_fk') THEN
            ALTER TABLE `horario_x_curso` ADD CONSTRAINT `seccion_horario_fk` FOREIGN KEY (`idSeccion`) REFERENCES `secciones` (`idSeccion`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla horario_x_curso ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_horario_x_curso();
DROP PROCEDURE IF EXISTS CreateTable_horario_x_curso;