USE cadisoft;

-- Tabla: horario
DROP PROCEDURE IF EXISTS CreateTable_horario;

DELIMITER $$
CREATE PROCEDURE CreateTable_horario()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'horario') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `horario` (
            `idhorario` INT NOT NULL AUTO_INCREMENT,
            `horario_dia` VARCHAR(10) NOT NULL,
            `horario_hora` TIME NOT NULL,
            `horario_hora_final` TIME NOT NULL,
            `horario_aula` VARCHAR(10) NOT NULL,
            PRIMARY KEY (`idhorario`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla horario creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario' AND column_name = 'idhorario') THEN
            ALTER TABLE `horario` ADD COLUMN `idhorario` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario' AND column_name = 'horario_dia') THEN
            ALTER TABLE `horario` ADD COLUMN `horario_dia` VARCHAR(10) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario' AND column_name = 'horario_hora') THEN
            ALTER TABLE `horario` ADD COLUMN `horario_hora` TIME NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario' AND column_name = 'horario_hora_final') THEN
            ALTER TABLE `horario` ADD COLUMN `horario_hora_final` TIME NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'horario' AND column_name = 'horario_aula') THEN
            ALTER TABLE `horario` ADD COLUMN `horario_aula` VARCHAR(10) NOT NULL;
        END IF;
        
        SELECT 'La tabla horario ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_horario();
DROP PROCEDURE IF EXISTS CreateTable_horario;