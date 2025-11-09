USE `cadisoft`;
DROP PROCEDURE IF EXISTS `inscripcion_inces_sp`;

DELIMITER $$
CREATE PROCEDURE `inscripcion_inces_sp`(
    IN p_idusuarios INT,
    IN p_fecha_inscripcion DATE,
    IN p_idSeccion INT,
    IN p_fecha_expiracion DATE,
    IN p_tipo ENUM('Privada','Inces'),
    IN p_idEmpresa INT
)
BEGIN
    DECLARE v_idInscripcion INT DEFAULT NULL;
    
    -- Verificar si ya existe una inscripción activa para este usuario en las fechas
    IF NOT EXISTS (
        SELECT 1 FROM inscripcion 
        WHERE idusuarios = p_idusuarios 
        AND fecha_inscripcion = p_fecha_inscripcion 
        AND fecha_expiracion = p_fecha_expiracion 
        AND es_activa = 1
    ) THEN

        -- Insertar nueva inscripción
        INSERT INTO inscripcion 
        (`idusuarios`, `fecha_inscripcion`, `fecha_expiracion`, `tipo`, `es_activa`, `idEmpresa`) 
        VALUES (p_idusuarios, p_fecha_inscripcion, p_fecha_expiracion, p_tipo, 1, p_idEmpresa);

        -- Obtener el ID de la inscripción recién insertada
        SET v_idInscripcion = LAST_INSERT_ID();

        -- Verificar que se obtuvo el ID correctamente
        IF v_idInscripcion IS NOT NULL AND v_idInscripcion > 0 THEN
            -- Insertar en insc_x_seccion
            INSERT INTO insc_x_seccion (`idInscripcion`, `idSeccion`) 
            VALUES (v_idInscripcion, p_idSeccion);

            -- Insertar en calificaciones
            INSERT INTO calificaciones (`idusuarios`, `idSeccion`, `idInscripcion`) 
            VALUES (p_idusuarios, p_idSeccion, v_idInscripcion);
        END IF;
    END IF;
END$$
DELIMITER ;