USE cadisoft;

-- Tabla: cursos
DROP PROCEDURE IF EXISTS CreateTable_cursos;

DELIMITER $$
CREATE PROCEDURE CreateTable_cursos()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'cursos') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `cursos` (
            `idCurso` INT NOT NULL AUTO_INCREMENT,
            `idFacultad` INT NOT NULL,
            `nombre_curso` VARCHAR(40) NOT NULL,
            `duracionCurso` INT NULL,
            `imagen` LONGBLOB NULL,
            `inces` TINYINT(1)  NULL DEFAULT 0,
            PRIMARY KEY (`idCurso`),
            KEY `facultad_fk` (`idFacultad`),
            CONSTRAINT `facultad_fk` FOREIGN KEY (`idFacultad`) REFERENCES `facultades` (`idFacultad`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla cursos creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'cursos' AND column_name = 'idCurso') THEN
            ALTER TABLE `cursos` ADD COLUMN `idCurso` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'cursos' AND column_name = 'idFacultad') THEN
            ALTER TABLE `cursos` ADD COLUMN `idFacultad` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'cursos' AND column_name = 'nombre_curso') THEN
            ALTER TABLE `cursos` ADD COLUMN `nombre_curso` VARCHAR(40) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'cursos' AND column_name = 'duracionCurso') THEN
            ALTER TABLE `cursos` ADD COLUMN `duracionCurso` INT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'cursos' AND column_name = 'imagen') THEN
            ALTER TABLE `cursos` ADD COLUMN `imagen` LONGBLOB NULL;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'cursos' AND column_name = 'duracionCurso') THEN
            ALTER TABLE `cursos` ADD COLUMN `inces` TINYINT(1)  NULL DEFAULT 0;
        END IF;
        
        -- Añadir foreign key si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'cursos' AND constraint_name = 'facultad_fk') THEN
            ALTER TABLE `cursos` ADD CONSTRAINT `facultad_fk` FOREIGN KEY (`idFacultad`) REFERENCES `facultades` (`idFacultad`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla cursos ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_cursos();
DROP PROCEDURE IF EXISTS CreateTable_cursos;