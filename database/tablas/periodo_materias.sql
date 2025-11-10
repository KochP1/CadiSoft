USE cadisoft;

-- Tabla: cursos
DROP PROCEDURE IF EXISTS CreateTable_periodo_materias;

DELIMITER $$
CREATE PROCEDURE CreateTable_periodo_materias()
BEGIN
-- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'periodo_materias') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `periodo_materias`(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            idSeccion INT NOT NULL,
            materia varchar(40) NOT NULL
        );
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'periodo_materias' AND column_name = 'id') THEN
            ALTER TABLE `periodo_materias` ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'periodo_materias' AND column_name = 'idSeccion') THEN
            ALTER TABLE `periodo_materias` ADD COLUMN `idSeccion` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'periodo_materias' AND column_name = 'materia') THEN
            ALTER TABLE `periodo_materias` ADD COLUMN `materia` varchar(40) NOT NULL;
        END IF;

        -- Verificar y modificar columnas si existen
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'periodo_materias' AND column_name = 'id') THEN
            ALTER TABLE `periodo_materias` MODIFY `id` INT NOT NULL AUTO_INCREMENT FIRST;
        END IF;

        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'periodo_materias' AND column_name = 'idSeccion') THEN
            ALTER TABLE `periodo_materias` MODIFY `idSeccion` INT NOT NULL;
        END IF;
        
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'periodo_materias' AND column_name = 'materia') THEN
            ALTER TABLE `periodo_materias` MODIFY `materia` varchar(40) NOT NULL;
        END IF;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_periodo_materias();
DROP PROCEDURE IF EXISTS CreateTable_periodo_materias;