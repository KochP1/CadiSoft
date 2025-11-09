USE `cadisoft`;
DROP PROCEDURE IF EXISTS `secciones_cantidad_sp`;
DELIMITER $$
CREATE PROCEDURE `secciones_cantidad_sp`(
	IN id_curso INT,
    IN cantidad INT,
    IN mayorMenor TINYINT
)
BEGIN
	IF mayormenor IS NULL THEN
		SELECT sc.*, u.nombre, u.apellido, u.cedula
		FROM secciones sc 
        INNER JOIN profesores p ON sc.idProfesor = p.idProfesor
        INNER JOIN usuarios u ON p.idusuarios = u.idusuarios
		WHERE sc.idCurso = id_curso
            AND (
                SELECT COUNT(*) 
                FROM insc_x_seccion isc 
                INNER JOIN inscripcion i ON isc.idInscripcion = i.idInscripcion 
                WHERE isc.idSeccion = sc.idSeccion
            ) = cantidad;
	ELSEIF mayorMenor IS TRUE THEN
		SELECT sc.*, u.nombre, u.apellido, u.cedula
		FROM secciones sc 
        INNER JOIN profesores p ON sc.idProfesor = p.idProfesor
        INNER JOIN usuarios u ON p.idusuarios = u.idusuarios
		WHERE sc.idCurso = id_curso
            AND (
                SELECT COUNT(*) 
                FROM insc_x_seccion isc 
                INNER JOIN inscripcion i ON isc.idInscripcion = i.idInscripcion 
                WHERE isc.idSeccion = sc.idSeccion
            ) > cantidad;
	ELSE
		SELECT sc.*, u.nombre, u.apellido, u.cedula
		FROM secciones sc 
        INNER JOIN profesores p ON sc.idProfesor = p.idProfesor
        INNER JOIN usuarios u ON p.idusuarios = u.idusuarios 
		WHERE sc.idCurso = id_curso
            AND (
            SELECT COUNT(*) 
            FROM insc_x_seccion isc 
            INNER JOIN inscripcion i ON isc.idInscripcion = i.idInscripcion 
            WHERE isc.idSeccion = sc.idSeccion
            ) < cantidad;
    END IF;
END$$
DELIMITER ;