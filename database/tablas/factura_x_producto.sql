USE cadisoft;

-- Tabla: factura_x_producto
DROP PROCEDURE IF EXISTS CreateTable_factura_x_producto;

DELIMITER $$
CREATE PROCEDURE CreateTable_factura_x_producto()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'factura_x_producto') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `factura_x_producto` (
            `idFactura_x_producto` INT NOT NULL AUTO_INCREMENT,
            `idFactura` INT NOT NULL,
            `idProducto` INT NOT NULL,
            `cantidad` INT NOT NULL,
            PRIMARY KEY (`idFactura_x_producto`),
            KEY `factura_fk` (`idFactura`),
            KEY `producto_fk` (`idProducto`),
            CONSTRAINT `factura_fk` FOREIGN KEY (`idFactura`) REFERENCES `facturas` (`idFactura`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `producto_fk` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProducto`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla factura_x_producto creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'factura_x_producto' AND column_name = 'idFactura_x_producto') THEN
            ALTER TABLE `factura_x_producto` ADD COLUMN `idFactura_x_producto` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'factura_x_producto' AND column_name = 'idFactura') THEN
            ALTER TABLE `factura_x_producto` ADD COLUMN `idFactura` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'factura_x_producto' AND column_name = 'idProducto') THEN
            ALTER TABLE `factura_x_producto` ADD COLUMN `idProducto` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'factura_x_producto' AND column_name = 'cantidad') THEN
            ALTER TABLE `factura_x_producto` ADD COLUMN `cantidad` INT NOT NULL;
        END IF;
        
        -- Añadir foreign keys si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'factura_x_producto' AND constraint_name = 'factura_fk') THEN
            ALTER TABLE `factura_x_producto` ADD CONSTRAINT `factura_fk` FOREIGN KEY (`idFactura`) REFERENCES `facturas` (`idFactura`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'factura_x_producto' AND constraint_name = 'producto_fk') THEN
            ALTER TABLE `factura_x_producto` ADD CONSTRAINT `producto_fk` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProducto`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla factura_x_producto ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_factura_x_producto();
DROP PROCEDURE IF EXISTS CreateTable_factura_x_producto;