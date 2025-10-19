USE `cadisoft`;
ALTER PROCEDURE `calificaciones_sp`(
    IN p_idSeccion INT
)
BEGIN
    DECLARE v_fecha_inscripcion DATE;
    DECLARE v_fecha_expiracion DATE;
    
    -- 1. Buscar períodos activos
    SELECT i.fecha_inscripcion, i.fecha_expiracion 
    INTO v_fecha_inscripcion, v_fecha_expiracion
    FROM insc_x_seccion 
    JOIN inscripcion i ON insc_x_seccion.idInscripcion = i.idInscripcion 
    WHERE insc_x_seccion.idSeccion = p_idSeccion 
    AND i.fecha_inscripcion <= CURDATE() 
    AND i.fecha_expiracion >= CURDATE()
    ORDER BY i.fecha_inscripcion DESC 
    LIMIT 1;
    
    
    IF v_fecha_inscripcion IS NULL THEN
        
        SELECT i.fecha_inscripcion, i.fecha_expiracion 
        INTO v_fecha_inscripcion, v_fecha_expiracion
        FROM insc_x_seccion 
        JOIN inscripcion i ON insc_x_seccion.idInscripcion = i.idInscripcion 
        WHERE insc_x_seccion.idSeccion = p_idSeccion 
        AND i.fecha_inscripcion > CURDATE()
        ORDER BY i.fecha_inscripcion ASC
        LIMIT 1;
    END IF;
    
	SELECT 
        c.idCalificacion, 
        c.idusuarios, 
        u.nombre, 
        u.segundoNombre, 
        u.apellido, 
        u.segundoApellido, 
        u.cedula, 
        i.fecha_inscripcion, 
        i.fecha_expiracion, 
        i.es_activa, 
        i.asistencia, 
        i.inasistencia, 
        i.idInscripcion,
        c.logro_1, 
        c.logro_2, 
        c.logro_3, 
        c.logro_4, 
        c.logro_5, 
        c.definitiva
    FROM calificaciones c 
    JOIN inscripcion i ON c.idInscripcion = i.idInscripcion 
    JOIN usuarios u ON c.idusuarios = u.idusuarios 
    WHERE c.idSeccion = p_idSeccion 
    AND i.fecha_inscripcion = v_fecha_inscripcion 
    AND i.fecha_expiracion = v_fecha_expiracion;
    
    

END
