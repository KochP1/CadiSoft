USE cadisoft;

-- Tabla: codigos_verificacion
DROP PROCEDURE IF EXISTS CreateTable_codigos_verificacion;

DELIMITER $$
CREATE PROCEDURE CreateTable_codigos_verificacion()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `codigos_verificacion` (
            `idCodigos` INT NOT NULL AUTO_INCREMENT,
            `idusuarios` INT NOT NULL,
            `codigo` VARCHAR(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            `expiracion` DATETIME NOT NULL,
            `usado` TINYINT(1) NULL,
            `creado_en` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`idCodigos`),
            KEY `idusuarios_v2p` (`idusuarios`),
            CONSTRAINT `idusuarios_v2p` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla codigos_verificacion creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion' AND column_name = 'idCodigos') THEN
            ALTER TABLE `codigos_verificacion` ADD COLUMN `idCodigos` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion' AND column_name = 'idusuarios') THEN
            ALTER TABLE `codigos_verificacion` ADD COLUMN `idusuarios` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion' AND column_name = 'codigo') THEN
            ALTER TABLE `codigos_verificacion` ADD COLUMN `codigo` VARCHAR(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion' AND column_name = 'expiracion') THEN
            ALTER TABLE `codigos_verificacion` ADD COLUMN `expiracion` DATETIME NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion' AND column_name = 'usado') THEN
            ALTER TABLE `codigos_verificacion` ADD COLUMN `usado` TINYINT(1) NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion' AND column_name = 'creado_en') THEN
            ALTER TABLE `codigos_verificacion` ADD COLUMN `creado_en` DATETIME NULL DEFAULT CURRENT_TIMESTAMP;
        END IF;
        
        -- Añadir foreign key si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'codigos_verificacion' AND constraint_name = 'idusuarios_v2p') THEN
            ALTER TABLE `codigos_verificacion` ADD CONSTRAINT `idusuarios_v2p` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla codigos_verificacion ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_codigos_verificacion();
DROP PROCEDURE IF EXISTS CreateTable_codigos_verificacion;