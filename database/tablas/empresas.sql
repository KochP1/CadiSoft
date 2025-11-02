USE cadisoft;

-- Tabla: cursos
DROP PROCEDURE IF EXISTS CreateTable_cursos;

DELIMITER $$
CREATE PROCEDURE CreateTable_empresas()
BEGIN
-- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'cursos') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `empresas`(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            nombre varchar(30) NOT NULL UNIQUE
        );
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'empresas' AND column_name = 'id') THEN
            ALTER TABLE `empresas` ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'empresas' AND column_name = 'nombre') THEN
            ALTER TABLE `empresas` ADD COLUMN `nombre` varchar(30) NOT NULL;
        END IF;

        -- Verificar y modificar columnas si existen
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'empresas' AND column_name = 'id') THEN
            ALTER TABLE `empresas` MODIFY `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'empresas' AND column_name = 'nombre') THEN
            ALTER TABLE `empresas` MODIFY `nombre` varchar(30) NOT NULL;
        END IF;
    END IF
END$$
DELIMITER ;

CALL CreateTable_empresas();
DROP PROCEDURE IF EXISTS CreateTable_empresas;