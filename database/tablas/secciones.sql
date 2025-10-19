USE cadisoft;

-- Tabla: secciones
DROP PROCEDURE IF EXISTS CreateTable_secciones;

DELIMITER $$
CREATE PROCEDURE CreateTable_secciones()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'secciones') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `secciones` (
            `idSeccion` INT NOT NULL AUTO_INCREMENT,
            `idCurso` INT NOT NULL,
            `idProfesor` INT NOT NULL,
            `seccion` VARCHAR(10) NOT NULL,
            `aula` VARCHAR(10) NOT NULL,
            PRIMARY KEY (`idSeccion`),
            UNIQUE KEY `seccion` (`seccion`),
            KEY `profesor_seccion_fk` (`idProfesor`),
            KEY `curso_seccion_fk` (`idCurso`),
            CONSTRAINT `curso_seccion_fk` FOREIGN KEY (`idCurso`) REFERENCES `cursos` (`idCurso`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `profesor_seccion_fk` FOREIGN KEY (`idProfesor`) REFERENCES `profesores` (`idProfesor`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla secciones creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND column_name = 'idSeccion') THEN
            ALTER TABLE `secciones` ADD COLUMN `idSeccion` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND column_name = 'idCurso') THEN
            ALTER TABLE `secciones` ADD COLUMN `idCurso` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND column_name = 'idProfesor') THEN
            ALTER TABLE `secciones` ADD COLUMN `idProfesor` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND column_name = 'seccion') THEN
            ALTER TABLE `secciones` ADD COLUMN `seccion` VARCHAR(10) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND column_name = 'aula') THEN
            ALTER TABLE `secciones` ADD COLUMN `aula` VARCHAR(10) NOT NULL;
        END IF;
        
        -- Añadir constraints únicos si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND constraint_name = 'seccion') THEN
            ALTER TABLE `secciones` ADD UNIQUE KEY `seccion` (`seccion`);
        END IF;
        
        -- Añadir foreign keys si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND constraint_name = 'curso_seccion_fk') THEN
            ALTER TABLE `secciones` ADD CONSTRAINT `curso_seccion_fk` FOREIGN KEY (`idCurso`) REFERENCES `cursos` (`idCurso`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'secciones' AND constraint_name = 'profesor_seccion_fk') THEN
            ALTER TABLE `secciones` ADD CONSTRAINT `profesor_seccion_fk` FOREIGN KEY (`idProfesor`) REFERENCES `profesores` (`idProfesor`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla secciones ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_secciones();
DROP PROCEDURE IF EXISTS CreateTable_secciones;