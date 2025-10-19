USE cadisoft;

-- Tabla: preinscripcion
DROP PROCEDURE IF EXISTS CreateTable_preinscripcion;

DELIMITER $$
CREATE PROCEDURE CreateTable_preinscripcion()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `preinscripcion` (
            `idPreinscipcion` INT NOT NULL AUTO_INCREMENT,
            `nombre` VARCHAR(12) NOT NULL,
            `segundoNombre` VARCHAR(12) NULL,
            `apellido` VARCHAR(20) NOT NULL,
            `segundoApellido` VARCHAR(20) NOT NULL,
            `cedula` VARCHAR(8) NOT NULL,
            `email` VARCHAR(50) NOT NULL,
            `curso` VARCHAR(40) NOT NULL,
            PRIMARY KEY (`idPreinscipcion`),
            UNIQUE KEY `cedula` (`cedula`),
            UNIQUE KEY `email` (`email`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla preinscripcion creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'idPreinscipcion') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `idPreinscipcion` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'nombre') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `nombre` VARCHAR(12) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'segundoNombre') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `segundoNombre` VARCHAR(12) NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'apellido') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `apellido` VARCHAR(20) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'segundoApellido') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `segundoApellido` VARCHAR(20) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'cedula') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `cedula` VARCHAR(8) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'email') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `email` VARCHAR(50) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND column_name = 'curso') THEN
            ALTER TABLE `preinscripcion` ADD COLUMN `curso` VARCHAR(40) NOT NULL;
        END IF;
        
        -- Añadir constraints únicos si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND constraint_name = 'cedula') THEN
            ALTER TABLE `preinscripcion` ADD UNIQUE KEY `cedula` (`cedula`);
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'preinscripcion' AND constraint_name = 'email') THEN
            ALTER TABLE `preinscripcion` ADD UNIQUE KEY `email` (`email`);
        END IF;
        
        SELECT 'La tabla preinscripcion ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_preinscripcion();
DROP PROCEDURE IF EXISTS CreateTable_preinscripcion;