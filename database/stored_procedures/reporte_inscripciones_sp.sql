USE `cadisoft`;
DROP PROCEDURE IF EXISTS `reporte_inscripciones_sp`;

DELIMITER $$
CREATE PROCEDURE `reporte_inscripciones_sp`(
    IN p_cedula VARCHAR(8),
    IN p_fecha_inscripcion DATE,
    IN p_idSeccion INT,
    IN p_fecha_expiracion DATE,
    IN p_tipo VARCHAR(20),
    IN p_es_activa TINYINT(1)
)
BEGIN
    DECLARE v_where_clause VARCHAR(1000) DEFAULT '';
    DECLARE v_sql_query VARCHAR(2000);
    
    
    IF p_cedula IS NOT NULL THEN
        SET v_where_clause = CONCAT(v_where_clause, ' AND u.cedula = ', p_cedula);
    END IF;

    IF p_es_activa IS NOT NULL THEN
        SET v_where_clause = CONCAT(v_where_clause, ' AND i.es_activa = ', p_es_activa);
    END IF;

    IF p_fecha_inscripcion IS NOT NULL THEN
        SET v_where_clause = CONCAT(v_where_clause, ' AND i.fecha_inscripcion >= ''', p_fecha_inscripcion, '''');
    END IF;

    IF p_fecha_expiracion IS NOT NULL THEN
        SET v_where_clause = CONCAT(v_where_clause, ' AND i.fecha_expiracion <= ''', p_fecha_expiracion, '''');
    END IF;

    IF p_idSeccion IS NOT NULL THEN
        SET v_where_clause = CONCAT(v_where_clause, ' AND s.idSeccion = ', p_idSeccion);
    END IF;

    IF p_tipo IS NOT NULL THEN
        SET v_where_clause = CONCAT(v_where_clause, ' AND i.tipo = ''', p_tipo, '''');
    END IF;
    
    
    SET v_sql_query = CONCAT(
        'SELECT
            i.idInscripcion, u.idusuarios, u.nombre, u.apellido, u.cedula,
            i.fecha_inscripcion, i.fecha_expiracion, i.tipo,
            c.nombre_curso AS curso, s.seccion, i.es_activa AS status,
            CASE 
                WHEN u.imagen IS NOT NULL AND LENGTH(u.imagen) > 0 THEN TRUE
                ELSE FALSE
            END AS imagen
        FROM inscripcion i
        JOIN usuarios u ON i.idusuarios = u.idusuarios
        JOIN insc_x_seccion ixs ON i.idInscripcion = ixs.idInscripcion
        JOIN secciones s ON ixs.idSeccion = s.idSeccion
        JOIN cursos c ON s.idCurso = c.idCurso'
    );
    
    
    IF v_where_clause != '' THEN
        SET v_sql_query = CONCAT(v_sql_query, ' WHERE ', SUBSTRING(v_where_clause, 6));
    END IF;
    
    
    SET v_sql_query = CONCAT(v_sql_query, ' ORDER BY i.fecha_inscripcion DESC, u.apellido, u.nombre');
    
    
    SET @dynamic_query = v_sql_query;
    PREPARE stmt FROM @dynamic_query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$
DELIMITER ;