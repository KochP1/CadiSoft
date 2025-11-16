USE `cadisoft`;
DROP PROCEDURE IF EXISTS `obtener_planilla_seccion_sp`;

DELIMITER $$
CREATE PROCEDURE `obtener_planilla_seccion_sp`(
    IN p_idSeccion VARCHAR(10),
    IN p_fecha_inscripcion DATE,
    IN p_fecha_expiracion DATE
)
BEGIN
    SELECT 
    u.nombre, 
    u.segundoNombre, 
    u.apellido, 
    u.segundoApellido, 
    u.cedula, 
    s.seccion,
    '' as logro_1,
    '' as logro_2,
    '' as logro_3,
    '' as logro_4,
    '' as logro_5,
    '' as definitiva,
    i.fecha_inscripcion, 
    i.fecha_expiracion 
    FROM inscripcion i 
    JOIN insc_x_seccion ics ON i.idInscripcion = ics.idInscripcion
    JOIN secciones s ON ics.idSeccion = s.idSeccion
    JOIN usuarios u ON i.idusuarios = u.idusuarios
    WHERE s.idSeccion = p_idSeccion
    AND i.fecha_inscripcion = p_fecha_inscripcion 
    AND i.fecha_expiracion = p_fecha_expiracion
    AND i.es_activa = 1;
END$$
DELIMITER ;