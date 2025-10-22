USE `cadisoft`;
DROP PROCEDURE IF EXISTS `secciones_cantidad_sp`;
CREATE PROCEDURE `secciones_cantidad_sp`(
	IN id_curso INT,
    IN cantidad INT,
    IN mayorMenor TINYINT
)
BEGIN
	IF mayormenor IS NULL THEN
		SELECT sc.* 
		FROM secciones sc 
		WHERE sc.idCurso = id_curso
            AND (
                SELECT COUNT(*) 
                FROM insc_x_seccion isc 
                INNER JOIN inscripcion i ON isc.idInscripcion = i.idInscripcion 
                WHERE isc.idSeccion = sc.idSeccion
            ) = cantidad;
	ELSEIF mayorMenor IS TRUE THEN
		SELECT sc.* 
		FROM secciones sc 
		WHERE sc.idCurso = id_curso
            AND (
                SELECT COUNT(*) 
                FROM insc_x_seccion isc 
                INNER JOIN inscripcion i ON isc.idInscripcion = i.idInscripcion 
                WHERE isc.idSeccion = sc.idSeccion
            ) > cantidad;
	ELSE
		SELECT sc.* 
		FROM secciones sc 
		WHERE sc.idCurso = id_curso
            AND (
            SELECT COUNT(*) 
            FROM insc_x_seccion isc 
            INNER JOIN inscripcion i ON isc.idInscripcion = i.idInscripcion 
            WHERE isc.idSeccion = sc.idSeccion
            ) < cantidad;
    END IF;
END