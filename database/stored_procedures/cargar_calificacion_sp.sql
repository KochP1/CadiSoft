USE `cadisoft`;
DROP PROCEDURE IF EXISTS `cargar_calificacion_sp`;

DELIMITER $$
CREATE PROCEDURE `cargar_calificacion_sp`(
    IN p_cedula VARCHAR(8),
    IN p_seccion VARCHAR(10),
    IN p_fecha_inscripcion DATE,
    IN p_fecha_expiracion DATE,
    IN p_logro_1 DOUBLE,
    IN p_logro_2 DOUBLE,
    IN p_logro_3 DOUBLE,
    IN p_logro_4 DOUBLE,
    IN p_logro_5 DOUBLE,
    IN p_definitiva DOUBLE
)
BEGIN
    DECLARE p_idusuarios INT;
    DECLARE p_idSeccion INT;
    DECLARE p_idInscripcion INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    -- Obtener el idusuarios
    SELECT idusuarios INTO p_idusuarios FROM usuarios WHERE cedula = p_cedula;
    SELECT idSeccion INTO p_idSeccion FROM secciones WHERE seccion = p_seccion;
    
    START TRANSACTION;
    
    IF p_idusuarios IS NULL OR p_idSeccion IS NULL THEN
        -- Lanzar error personalizado
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error: No se encontró el usuario con la cédula proporcionada';
    ELSE
        SELECT idInscripcion INTO p_idInscripcion FROM inscripcion WHERE fecha_inscripcion = p_fecha_inscripcion AND fecha_expiracion = p_fecha_expiracion AND es_activa = 1 AND idusuarios = p_idusuarios;
        
        IF p_idInscripcion IS NULL THEN
            -- Lanzar error personalizado
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Error: No se la inscripción del alumno';
		END IF;

        UPDATE calificaciones 
            SET `logro_1` = p_logro_1, 
                `logro_2` = p_logro_2, 
                `logro_3` = p_logro_3, 
                `logro_4` = p_logro_4, 
                `logro_5` = p_logro_5, 
                `definitiva` = p_definitiva 
            WHERE idusuarios = p_idusuarios 
            AND idSeccion = p_idSeccion 
            AND idInscripcion = p_idInscripcion;
    END IF;
    
    COMMIT;
END$$
DELIMITER ;