USE cadisoft;

-- Tabla: materias
DROP PROCEDURE IF EXISTS CreateTable_materias;
DELIMITER $$
CREATE PROCEDURE CreateTable_materias()
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'materias') THEN

            CREATE TABLE `materias` (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                idCurso INT NOT NULL,
                nombre varchar(40) NOT NULL UNIQUE
            );

        ELSE

            -- Verificar y añadir columnas si no existen
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'materias' AND column_name = 'id') THEN
                ALTER TABLE `materias` ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
            END IF;
            
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'materias' AND column_name = 'idCurso') THEN
                ALTER TABLE `materias` ADD COLUMN `idCurso` INT NOT NULL;
            END IF;
            
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'materias' AND column_name = 'nombre') THEN
                ALTER TABLE `materias` ADD COLUMN `nombre` VARCHAR(40) NOT NULL;
            END IF;

            -- Verificar y modificar columnas si existen
            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'materias' AND column_name = 'id') THEN
                ALTER TABLE `materias` MODIFY `id` INT NOT NULL AUTO_INCREMENT FIRST;
            END IF;
            
            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'materias' AND column_name = 'idCurso') THEN
                ALTER TABLE `materias` MODIFY `idCurso` INT NOT NULL;
            END IF;
            
            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'materias' AND column_name = 'nombre') THEN
                ALTER TABLE `materias` MODIFY `nombre` VARCHAR(40) NOT NULL;
            END IF;

        END IF;
    END$$
    DELIMITER ;

CALL CreateTable_materias();
DROP PROCEDURE IF EXISTS CreateTable_materias;
