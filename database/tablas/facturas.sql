USE cadisoft;

-- Tabla: facturas
DROP PROCEDURE IF EXISTS CreateTable_facturas;

DELIMITER $$
CREATE PROCEDURE CreateTable_facturas()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'facturas') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `facturas` (
            `idFactura` INT NOT NULL AUTO_INCREMENT,
            `cliente` VARCHAR(50) NOT NULL,
            `telefono` VARCHAR(11) NOT NULL,
            `cedula` VARCHAR(8) NOT NULL,
            `direccion` VARCHAR(30) NOT NULL,
            `fecha` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `total` DOUBLE NOT NULL,
            PRIMARY KEY (`idFactura`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla facturas creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facturas' AND column_name = 'idFactura') THEN
            ALTER TABLE `facturas` ADD COLUMN `idFactura` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facturas' AND column_name = 'cliente') THEN
            ALTER TABLE `facturas` ADD COLUMN `cliente` VARCHAR(50) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facturas' AND column_name = 'telefono') THEN
            ALTER TABLE `facturas` ADD COLUMN `telefono` VARCHAR(11) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facturas' AND column_name = 'cedula') THEN
            ALTER TABLE `facturas` ADD COLUMN `cedula` VARCHAR(8) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facturas' AND column_name = 'direccion') THEN
            ALTER TABLE `facturas` ADD COLUMN `direccion` VARCHAR(30) NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facturas' AND column_name = 'fecha') THEN
            ALTER TABLE `facturas` ADD COLUMN `fecha` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'facturas' AND column_name = 'total') THEN
            ALTER TABLE `facturas` ADD COLUMN `total` DOUBLE NOT NULL;
        END IF;
        
        SELECT 'La tabla facturas ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_facturas();
DROP PROCEDURE IF EXISTS CreateTable_facturas;