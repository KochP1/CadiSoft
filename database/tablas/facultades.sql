USE cadisoft;

-- Tabla: facultades
DROP PROCEDURE IF EXISTS CreateTable_facultades;

DELIMITER $$
CREATE PROCEDURE CreateTable_facultades()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'facultades') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `facultades` (
            `idFacultad` INT NOT NULL AUTO_INCREMENT,
            `facultad` VARCHAR(40) NOT NULL,
            PRIMARY KEY (`idFacultad`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla facultades creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facultades' AND column_name = 'idFacultad') THEN
            ALTER TABLE `facultades` ADD COLUMN `idFacultad` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facultades' AND column_name = 'facultad') THEN
            ALTER TABLE `facultades` ADD COLUMN `facultad` VARCHAR(40) NOT NULL;
        END IF;
        
        SELECT 'La tabla facultades ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_facultades();
DROP PROCEDURE IF EXISTS CreateTable_facultades;