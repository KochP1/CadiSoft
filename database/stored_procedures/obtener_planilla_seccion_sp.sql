USE `cadisoft`;
DROP PROCEDURE IF EXISTS `obtener_planilla_seccion_sp`;

DELIMITER $$
CREATE PROCEDURE `obtener_planilla_seccion_sp`(
    IN p_idSeccion VARCHAR(10),
    IN p_fecha_inscripcion DATE,
    IN p_fecha_expiracion DATE,
)
BEGIN
    SELECT 
    u.nombre, 
    u.segundoNombre, 
    u.apellido, 
    u.segundoApellido, 
    u.cedula, 
    s.seccion, 
    i.fecha_inscripcion, 
    i.fecha_expiracion 
    FROM inscripcion i 
    JOIN secciones s ON i.idSeccion = s.idSeccion
    JOIN usuarios u ON i.idusuarios = u.idusuarios
    WHERE i.idSeccion = p_idSeccion 
    AND i.fecha_inscripcion = p_fecha_inscripcion 
    AND i.fecha_expiracion = p_fecha_expiracion 
    AND i.es_activa = 1;
END$$
DELIMITER ;