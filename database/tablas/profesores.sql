USE cadisoft;

-- Tabla: profesores
DROP PROCEDURE IF EXISTS CreateTable_profesores;

DELIMITER $$
CREATE PROCEDURE CreateTable_profesores()
BEGIN
    -- Verificar si la tabla existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cadisoft' AND table_name = 'profesores') THEN
        -- Crear la tabla si no existe
        CREATE TABLE `profesores` (
            `idProfesor` INT NOT NULL AUTO_INCREMENT,
            `idusuarios` INT NOT NULL,
            `especialidad` VARCHAR(20) NOT NULL,
            PRIMARY KEY (`idProfesor`),
            KEY `usuario_p_idx` (`idusuarios`),
            CONSTRAINT `usuario_p` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
        
        SELECT 'Tabla profesores creada exitosamente.' AS Resultado;
    ELSE
        -- Verificar y añadir columnas si no existen
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'profesores' AND column_name = 'idProfesor') THEN
            ALTER TABLE `profesores` ADD COLUMN `idProfesor` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'profesores' AND column_name = 'idusuarios') THEN
            ALTER TABLE `profesores` ADD COLUMN `idusuarios` INT NOT NULL;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'cadisoft' AND table_name = 'profesores' AND column_name = 'especialidad') THEN
            ALTER TABLE `profesores` ADD COLUMN `especialidad` VARCHAR(20) NOT NULL;
        END IF;
        
        -- Añadir foreign key si no existe
        IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE table_schema = 'cadisoft' AND table_name = 'profesores' AND constraint_name = 'usuario_p') THEN
            ALTER TABLE `profesores` ADD CONSTRAINT `usuario_p` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
        END IF;
        
        SELECT 'La tabla profesores ya existe. Columnas verificadas y añadidas si era necesario.' AS Resultado;
    END IF;
END$$
DELIMITER ;

CALL CreateTable_profesores();
DROP PROCEDURE IF EXISTS CreateTable_profesores;