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
    c.logro_1,
    c.logro_2,
    c.logro_3,
    c.logro_4,
    c.logro_5,
    c.definitiva,
    i.fecha_inscripcion, 
    i.fecha_expiracion 
    FROM inscripcion i 
    JOIN insc_x_seccion ics ON i.idInscripcion = ics.idInscripcion
    JOIN secciones s ON ics.idSeccion = s.idSeccion
    JOIN usuarios u ON i.idusuarios = u.idusuarios
    JOIN calificaciones c ON c.idInscripcion = i.idInscripcion AND c.idusuarios = u.idusuarios
    WHERE s.idSeccion = p_idSeccion
    AND i.fecha_inscripcion = p_fecha_inscripcion 
    AND i.fecha_expiracion = p_fecha_expiracion
    AND i.es_activa = 1;
END$$
DELIMITER ;