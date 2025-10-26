from flask import jsonify, request, render_template, redirect, url_for, Blueprint, current_app, flash, g
from flask_login import login_required
from datetime import date
import pymysql

cursos = Blueprint('cursos', __name__, template_folder='templates', static_folder="static")

# ENDPOINTS DE CURSOS

@cursos.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    g.db.ping(reconnect=True)

    if request.method == 'POST':
        facultad = request.form.get('idFacultad')
        curso = request.form.get('nombre_curso')
        duracion = request.form.get('duracion_curso')

        try:
            with g.db.cursor() as cur:
                sql = 'INSERT INTO cursos (`idFacultad`, `nombre_curso`, `duracionCurso`) VALUES (%s, %s, %s)'
                data = (facultad, curso, duracion)
                cur.execute(sql, data)
                g.db.commit()
                return jsonify({'message': 'Curso creado satisfactoriamente'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'Error al crear curso: {e}'}), 400

    try:
        with g.db.cursor() as cur:
            sql = 'SELECT c.idCurso, f.idFacultad, f.facultad, c.nombre_curso, c.duracionCurso FROM cursos c JOIN facultades f ON c.idFacultad = f.idFacultad'
            cur.execute(sql)
            registros = cur.fetchall()
            insertCursos = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertCursos.append(dict(zip(columNames, record)))

            return render_template('cursos/index.html', cursos = insertCursos)
    except Exception as e:
        print(e)
        return redirect(url_for('usuario.inicio'))


@cursos.route('/buscar_curso', methods = ['GET', 'POST'])
@login_required
def buscar_curso():
    try:
        curso = request.form.get('curso')

        with g.db.cursor() as cur:
            cur.execute('SELECT c.idCurso, f.idFacultad, f.facultad, c.nombre_curso, c.duracionCurso FROM cursos c JOIN facultades f ON c.idFacultad = f.idFacultad WHERE c.nombre_curso = %s', (curso,))
            registros = cur.fetchall()
            insertCursos = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertCursos.append(dict(zip(columNames, record)))

            return render_template('cursos/index.html', cursos = insertCursos)
    except Exception as e:
        return redirect(url_for('cursos.index'))


@cursos.route('/buscar_facultades')
@login_required
def buscar_facultades():
    try:
        g.db.ping(reconnect=True)
        
        with g.db.cursor() as cur:
            sql = 'SELECT * FROM facultades'
            cur.execute(sql)
            facultades = cur.fetchall()

            if facultades:
                columNames = [column[0] for column in cur.description]
                facultades_dict = [dict(zip(columNames, row)) for row in facultades]

                return jsonify({'facultades': facultades_dict}), 200
    except Exception as e:
        return jsonify({'error': 'Error al buscar facultades'}), 400
    


@cursos.route('/edit_cursos/<int:idCurso>', methods = ['GET'])
@login_required
def edit_cursos(idCurso):
    g.db.ping(reconnect=True)

    try:
        with g.db.cursor() as cur:
            sql = 'SELECT c.idCurso, c.idFacultad, c.nombre_curso, c.duracionCurso, c.imagen, f.facultad FROM cursos c JOIN facultades f ON c.idFacultad = f.idFacultad WHERE c.idCurso = %s'
            cur.execute(sql, (idCurso,))
            registros = cur.fetchall()

            insertRegistros = []
            columNames = [column[0] for column in cur.description]

            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))

            cur.execute('SELECT * FROM facultades')
            registrosFacultades = cur.fetchall()

            insertRegistrosFacultades = []
            columNamesFacultades = [column[0] for column in cur.description]

            for record in registrosFacultades:
                insertRegistrosFacultades.append(dict(zip(columNamesFacultades, record)))

            for record in insertRegistros:
                idFacultad = record['idFacultad']
            
            for record in insertRegistrosFacultades:
                if idFacultad == record['idFacultad']:
                    record.clear()

            return render_template('cursos/editarCurso.html', cursos = insertRegistros, facultades = insertRegistrosFacultades)
    except Exception as e:
        return f'Error: {e}'



@cursos.route('/edit_nombre_curso/<int:idCurso>', methods = ['PATCH'])
@login_required
def edit_nombre_curso(idCurso):
    g.db.ping(reconnect=True)
    curso = request.form.get('curso')

    if not curso:
        return jsonify({'error': 'Faltan campos'}), 400
    
    try:
        with g.db.cursor() as cur:
            sql = 'UPDATE cursos SET nombre_curso = %s WHERE idCurso = %s'
            data = (curso, idCurso)
            cur.execute(sql, data)
            g.db.commit()
            return jsonify({'message': 'Curso modificado satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al modificar curso'}), 500
    


@cursos.route('/edit_facultad_curso/<int:idCurso>', methods = ['PATCH'])
@login_required
def edit_facultad_curso(idCurso):
    g.db.ping(reconnect=True)
    facultad = request.form.get('facultad')

    if not facultad:
        return jsonify({'error': 'Faltan campos'}), 400
    
    try:
        with g.db.cursor() as cur:
            sql = 'UPDATE cursos SET idFacultad = %s WHERE idCurso = %s'
            data = (facultad, idCurso)
            cur.execute(sql, data)
            g.db.commit()
            return jsonify({'message': 'Curso modificado satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al modificar curso'}), 500

@cursos.route('/edit_duracion_curso/<int:idCurso>', methods = ['PATCH'])
@login_required
def edit_duracion_curso(idCurso):
    g.db.ping(reconnect=True)
    duracion = request.form.get('duracion')

    if not duracion:
        return jsonify({'error': 'Faltan campos'}), 400
    
    try:
        with g.db.cursor() as cur:
            sql = 'UPDATE cursos SET duracionCurso = %s WHERE idCurso = %s'
            data = (duracion, idCurso)
            cur.execute(sql, data)
            g.db.commit()
            return jsonify({'message': 'Curso modificado satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al modificar curso'}), 500


@cursos.route('/eliminar_curso/<int:idcurso>', methods = ['DELETE'])
@login_required
def eliminar_curso(idcurso):
    try:
        with g.db.cursor() as cur:
            cur.execute('DELETE FROM cursos WHERE idCurso = %s', (idcurso,))
            g.db.commit()
            return jsonify({'mensaje': 'curso eliminado'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'el curso no pudo ser eliminado'}), 400

# FINALIZA ENDPOINTS DE CURSOS

# ENDPOINTS DE SECCIONES POR CURSO
@cursos.route('/seccion_curso/<int:idcurso>')
@login_required
def seccion_curso(idcurso):
    with g.db.cursor() as cur:
        g.db.ping(reconnect=True)
        try:
            sql = 'SELECT s.idSeccion, s.idCurso, u.nombre, u.apellido, c.nombre_curso, s.seccion FROM secciones s JOIN cursos c ON s.idCurso = c.idCurso JOIN profesores p ON s.idProfesor = p.idProfesor JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE c.idCurso = %s'
            data = (idcurso,)
            cur.execute(sql, data)
            registros = cur.fetchall()
            insertSecciones = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertSecciones.append(dict(zip(columNames, record)))
            
            cur.execute('SELECT * FROM cursos WHERE idCurso = %s', (idcurso,))
            registro_curso = cur.fetchall()
            insertCurso = []
            columNamesCursos = [column[0] for column in cur.description]
            for record in registro_curso:
                insertCurso.append(dict(zip(columNamesCursos, record)))

            return render_template('cursos/seccionesCurso.html', secciones = insertSecciones, cursos = insertCurso)
        except Exception as e:
            print(e)
            return redirect(url_for('cursos.index'))


@cursos.route('/buscar_seccion/<int:id>', methods = ['GET', 'POST'])
@login_required
def buscar_seccion(id):
    try:
        with g.db.cursor() as cur:
            seccion = request.form.get('seccion')
            cur.execute('SELECT s.idSeccion, s.idCurso, u.nombre, u.apellido, c.nombre_curso, s.seccion FROM secciones s JOIN cursos c ON s.idCurso = c.idCurso JOIN profesores p ON s.idProfesor = p.idProfesor JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE c.idCurso = %s AND s.seccion = %s', (id, seccion))
            registros = cur.fetchall()
            insertSecciones = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertSecciones.append(dict(zip(columNames, record)))
            
            cur.execute('SELECT * FROM cursos WHERE idCurso = %s', (id,))
            registro_curso = cur.fetchall()
            insertCurso = []
            columNamesCursos = [column[0] for column in cur.description]
            for record in registro_curso:
                insertCurso.append(dict(zip(columNamesCursos, record)))

            return render_template('cursos/seccionesCurso.html', secciones = insertSecciones, cursos = insertCurso)
    except Exception as e:
        return redirect(url_for('cursos.seccion_curso', idcurso = id))

@cursos.route('/filtrar_seccion_cantidad/<int:id>', methods = ['GET', 'POST'])
def filtrar_seccion_cantidad(id):
    cantidad = request.form.get('cantidad')
    filtro = request.form.get('filtro-participantes')

    with g.db.cursor() as cur:
        if (filtro == 'mayor'):
            cur.callproc('secciones_cantidad_sp', [id, cantidad, 1])  
        elif (filtro == 'menor'):
            cur.callproc('secciones_cantidad_sp', [id, cantidad, 0])
        else:
            cur.callproc('secciones_cantidad_sp', [id, cantidad, None])
        registros = cur.fetchall()
        secciones = []
        columNames = [column[0] for column in cur.description]

        for record in registros:
            secciones.append(dict(zip(columNames, record)))

        cur.execute('SELECT * FROM cursos WHERE idCurso = %s', (id,))
        regist = cur.fetchall()
        cursos = []
        columNames = [column[0] for column in cur.description]
        for record in regist:
            cursos.append(dict(zip(columNames, record)))
        

        if (len(secciones) > 0):
            return render_template('cursos/secciones_filtradas_cantidad.html', secciones = secciones, cantidad = cantidad, cursos = cursos, filtro = filtro)
        else:
            flash('No hay secciones para filtrar con estos parámetros')
            return redirect(url_for('cursos.seccion_curso', idcurso = id))

@cursos.route('/edit_seccion/<int:id>/<int:idCurso>',methods = ['GET'])
@login_required
def edit_seccion(id, idCurso):
    if request.method == 'GET':
        try:
            with g.db.cursor() as cur:
                cur.execute('SELECT s.idSeccion, s.seccion, s.aula, p.idProfesor, u.nombre, u.apellido FROM secciones s JOIN profesores p ON s.idProfesor = p.idProfesor JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE s.idSeccion = %s', (id))
                registros = cur.fetchall()
                insertSecciones = []
                columNames = [column[0] for column in cur.description]
                for record in registros:
                    insertSecciones.append(dict(zip(columNames, record)))
                
                idProfesor = insertSecciones[0]['idProfesor']
                
                sql = 'SELECT u.idusuarios, u.nombre, u.apellido, u.cedula, p.idProfesor, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE p.idProfesor != %s'
                cur.execute(sql, (idProfesor,))
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]
                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                
                cur.execute('SELECT * FROM cursos WHERE idCurso = %s', (idCurso,))
                registro_curso = cur.fetchall()
                insertCurso = []
                columNamesCursos = [column[0] for column in cur.description]
                for record in registro_curso:
                    insertCurso.append(dict(zip(columNamesCursos, record)))
                
                return render_template('cursos/editSeccion.html', secciones = insertSecciones, profesores = insertRegistros, cursos = insertCurso)
        except Exception as e:
            return f'Error: {e}'


@cursos.route('/edit_seccion_campos/<int:id>', methods = ['PATCH'])
@login_required
def edit_seccion_campos(id):
    if request.method == 'PATCH':
        try:
            with g.db.cursor() as cur:
                seccion = request.form.get('seccion')
                profesor = request.form.get('profesor')

                if not seccion and not profesor:
                    return jsonify({'error': 'No hay campos para actualizar'}), 400

                if seccion:
                    cur.execute('UPDATE secciones SET seccion = %s WHERE idSeccion = %s', (seccion, id))
                
                if profesor:
                    cur.execute('UPDATE secciones SET idProfesor = %s WHERE idSeccion = %s', (profesor, id))
                
                g.db.commit()
                return jsonify({'mensaje': 'Seccion actualizada'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'Error: {e}'}), 500
        
@cursos.route('/edit_horario_seccion/<int:idSeccion>', methods=['PATCH'])
@login_required
def edit_horario_seccion(idSeccion):
    try:
        data = request.get_json()
        horarios = data.get('horarios', [])
        profesor = data.get('idProfesor')
        
        # VALIDACIÓN DE DATOS
        if not horarios:
            return jsonify({'error': 'No se recibieron horarios'}), 400
        
        # Filtrar horarios válidos
        horarios_validos = []
        for horario in horarios:
            # Validar que tenga todos los campos necesarios
            if (horario and 
                horario.get('celdaId') and 
                horario.get('dia') and 
                horario.get('horaInicio') and 
                horario.get('horaFin') and 
                horario.get('curso')):
                
                horarios_validos.append(horario)
                print(horarios_validos)

        with g.db.cursor(pymysql.cursors.DictCursor) as cur:
            regist = 0
            for horario in horarios_validos:
                cur.execute('''
                SELECT s.idSeccion, s.seccion, h.horario_dia, h.horario_hora, h.horario_hora_final
                FROM horario_x_curso hc 
                JOIN horario h ON hc.idhorario = h.idhorario 
                JOIN secciones s ON hc.idSeccion = s.idSeccion 
                WHERE s.idProfesor = %s 
                AND hc.idSeccion != %s
                AND h.horario_dia = %s 
                AND (
                    (h.horario_hora <= %s AND h.horario_hora_final > %s) OR
                    (h.horario_hora < %s AND h.horario_hora_final >= %s) OR
                    (h.horario_hora >= %s AND h.horario_hora_final <= %s)
                )''', (profesor, idSeccion,
                    horario['dia'], 
                    horario['horaInicio'], horario['horaInicio'],
                    horario['horaFin'], horario['horaFin'],
                    horario['horaInicio'], horario['horaFin']
                    )
                )
                print(profesor)
                regist = cur.fetchone()
                print(regist)
                print(horario['horario'])
                print(horario['dia'])
                print(horario['horaInicio'])
                print(horario['horaFin'])
                if regist:
                    return jsonify({
                        'error': 'El profesor ya tiene una sección en el mismo horario',
                        'detalles': {
                            'seccion_existente': regist['seccion'],
                            'dia': regist['horario_dia'],
                            'hora_inicio': str(regist['horario_hora']),
                            'hora_fin': str(regist['horario_hora_final'])
                        }
                    }), 400
        with g.db.cursor() as cur:
            cur.execute('DELETE h FROM horario h JOIN horario_x_curso hc ON hc.idhorario = h.idhorario WHERE hc.idSeccion = %s', (idSeccion,))
            g.db.commit()
            for horario in horarios_validos:
                try:
                    cur.execute('''
                        INSERT INTO horario (horario_dia, horario_hora, horario_hora_final, horario_aula)
                        VALUES (%s, %s, %s, %s)
                    ''', (
                        horario['dia'],
                        horario['horaInicio'],
                        horario['horaFin'],
                        horario.get('horario_aula', ''),
                    ))

                    cur.execute('SELECT idhorario FROM horario ORDER BY idhorario DESC LIMIT 1')
                    idhorario = cur.fetchone()
                    cur.execute('INSERT INTO horario_x_curso (`idhorario`, `idSeccion`) VALUES (%s, %s)', (idhorario, idSeccion))
                    
                except Exception as e:
                    print(f"Error insertando horario {horario}: {e}")
                    continue
            
            g.db.commit()
        
        return jsonify({'mensaje': 'Horario actualizado correctamente'}), 200
        
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        print(f"Error general en edit_horario_seccion: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@cursos.route('/craer_seccion/<int:idCurso>', methods = ['GET', 'POST'])
@login_required
def crear_seccion(idCurso):
    g.db.ping(reconnect=True)

    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'seccion' not in data or 'profesor' not in data or 'horarios' not in data or 'aula' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        seccion = data['seccion']
        profesor = data['profesor']
        aula = data['aula']
        horarios = data['horarios']
        
        if not isinstance(horarios, list) or len(horarios) == 0:
            return jsonify({'error': 'El horario no es válido'}), 400

        if not seccion or not profesor:
            return jsonify({'error': 'Faltan campos'}), 400
        try:
            with g.db.cursor(pymysql.cursors.DictCursor) as cur: 
                regist = 0
                for record in horarios:
                    cur.execute('''
                                SELECT s.idSeccion, s.seccion, h.horario_dia, h.horario_hora, h.horario_hora_final
                                FROM horario_x_curso hc 
                                JOIN horario h ON hc.idhorario = h.idhorario 
                                JOIN secciones s ON hc.idSeccion = s.idSeccion 
                                WHERE s.idProfesor = %s 
                                AND h.horario_dia = %s 
                                AND (
                                    (h.horario_hora <= %s AND h.horario_hora_final > %s) OR
                                    (h.horario_hora < %s AND h.horario_hora_final >= %s) OR
                                    (h.horario_hora >= %s AND h.horario_hora_final <= %s)
                                )''', (profesor, 
                                    record['dia'], 
                                    record['hora_inicio'], record['hora_inicio'],
                                    record['hora_fin'], record['hora_fin'],
                                    record['hora_inicio'], record['hora_fin']
                                    )
                                )

                    regist = cur.fetchone()
                    if regist:
                        return jsonify({
                            'error': 'El profesor ya tiene una sección en el mismo horario',
                            'detalles': {
                                'seccion_existente': regist['seccion'],
                                'dia': regist['horario_dia'],
                                'hora_inicio': str(regist['horario_hora']),
                                'hora_fin': str(regist['horario_hora_final'])
                            }
                        }), 400
                
            with g.db.cursor() as cur:    
                cur.execute('INSERT INTO secciones (`idCurso`, `idProfesor`, `seccion`, `aula`) VALUES (%s, %s, %s, %s)', (idCurso, profesor, seccion, aula))
                g.db.commit()

                cur.execute('SELECT idSeccion FROM secciones WHERE seccion = %s', (seccion,))
                idSeccion = cur.fetchone()

                for record in horarios:
                    cur.execute('INSERT INTO horario (`horario_dia`, `horario_hora`, `horario_hora_final`, `horario_aula`) VALUES (%s, %s, %s, %s)', (record['dia'], record['hora_inicio'], record['hora_fin'], aula))
                    g.db.commit()
                    idhorario = cur.lastrowid

                    cur.execute('INSERT INTO horario_x_curso (`idhorario`, `idSeccion`) VALUES (%s, %s)', (idhorario, idSeccion))
                    g.db.commit()

                return jsonify({'message': 'Sección creada satisfactoriamente'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            print(e)
            return jsonify({'error': 'Error al crear sección'}), 500

    if request.method == 'GET':
        try:
            with g.db.cursor() as cur:
                sql = 'SELECT u.idusuarios, u.nombre, u.apellido, u.cedula, p.idProfesor, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios'
                cur.execute(sql)
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]
                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                
                cur.execute('SELECT * FROM cursos WHERE idCurso = %s', (idCurso,))
                registro_curso = cur.fetchall()
                insertCurso = []
                columNamesCursos = [column[0] for column in cur.description]
                for record in registro_curso:
                    insertCurso.append(dict(zip(columNamesCursos, record)))
            
            return render_template('cursos/crearSeccion.html', profesores = insertRegistros, cursos = insertCurso)
        except Exception as e:
            return redirect(url_for('cursos.index'))


@cursos.route('/elim_seccion/<int:idSeccion>', methods = ['DELETE'])
@login_required
def elim_seccion(idSeccion):
    g.db.ping(reconnect=True)

    if not idSeccion:
        return jsonify({'error': 'Faltan campos'})

    try:
        with g.db.cursor() as cur:
            cur.execute('SET SQL_SAFE_UPDATES = 0;')
            cur.execute("""
                        DELETE h 
                        FROM horario h 
                        JOIN horario_x_curso hc ON hc.idhorario = h.idhorario 
                        WHERE hc.idSeccion = %s;""", (idSeccion,))
            cur.execute('SET SQL_SAFE_UPDATES = 1;')
            sql = 'DELETE FROM secciones WHERE idSeccion = %s'
            cur.execute(sql, (idSeccion,))
            g.db.commit()
            return jsonify({'message': 'Sección eliminada satisfactoriamente'})
    except Exception as e:
        print(e)
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al eliminar seccion'}), 500

# FINALIZA ENDPOINTS DE SECCIONES

# ENDPOINTS DE CALIFICACIONES

def dateToString(fecha: date) -> str:
    return f"{fecha.day:02d}/{fecha.month:02d}/{fecha.year}"

@cursos.route('/calificaciones/<idSeccion>', methods = ['GET'])
@login_required
def calificaciones(idSeccion):
    g.db.ping(reconnect=True)

    if request.method == 'GET':

        try:
            with g.db.cursor() as cur:
                cur.execute('SELECT s.idSeccion, c.nombre_curso, s.seccion FROM secciones s JOIN cursos c ON s.idCurso = c.idCurso WHERE s.idSeccion = %s', (idSeccion,))
                registro = cur.fetchall()

                insertRegistro = []
                columNames = [column[0] for column in cur.description]
                for record in registro:
                    insertRegistro.append(dict(zip(columNames, record)))

                cur.callproc('calificaciones_sp', [idSeccion])
                registro_calificaciones = cur.fetchall()

                insertCalificaciones = []
                columNamesCalificaciones = [column[0] for column in cur.description]
                for record in registro_calificaciones:
                    insertCalificaciones.append(dict(zip(columNamesCalificaciones, record)))

                for record in insertCalificaciones:
                    record['fecha_inscripcion'] = dateToString(record['fecha_inscripcion'])
                    record['fecha_expiracion'] = dateToString(record['fecha_expiracion'])
                
                return render_template('cursos/calificaciones.html', data = insertRegistro, calificaciones = insertCalificaciones)
        except Exception as e:
            flash('No hay alumnos inscritos en esta sección')
            with g.db.cursor() as cursor:
                cursor.execute('SELECT idCurso FROM secciones WHERE idSeccion = %s', (idSeccion))
                curso = cursor.fetchone()
            print(e)
            return redirect(url_for('cursos.seccion_curso', idcurso = curso[0]))

@cursos.route('/filtrar_periodos/<idSeccion>', methods=['POST'])
@login_required
def filtrar_periodos(idSeccion):
    g.db.ping(reconnect=True)

    if request.method == 'POST':
        try:
            # Obtener las fechas del formulario
            fecha_desde = request.form.get('fecha_desde')
            fecha_hasta = request.form.get('fecha_hasta')
            
            # Validar que se recibieron ambas fechas
            if not fecha_desde or not fecha_hasta:
                flash('Por favor, selecciona ambas fechas')
                return redirect(url_for('cursos.calificaciones', idSeccion=idSeccion))
            
            # Validar que fecha_desde no sea mayor que fecha_hasta
            if fecha_desde > fecha_hasta:
                flash('La fecha "Desde" no puede ser mayor que la fecha "Hasta"')
                return redirect(url_for('cursos.calificaciones', idSeccion=idSeccion))

            with g.db.cursor() as cur:
                # Obtener información básica de la sección (igual al endpoint original)
                cur.execute('''
                    SELECT s.idSeccion, c.nombre_curso, s.seccion 
                    FROM secciones s 
                    JOIN cursos c ON s.idCurso = c.idCurso 
                    WHERE s.idSeccion = %s
                ''', (idSeccion,))
                registro = cur.fetchall()

                insertRegistro = []
                columNames = [column[0] for column in cur.description]
                for record in registro:
                    insertRegistro.append(dict(zip(columNames, record)))
                
                # Obtener períodos dentro del rango de fechas seleccionado
                cur.execute('''
                    SELECT DISTINCT i.fecha_inscripcion, i.fecha_expiracion, i.idInscripcion
                    FROM insc_x_seccion 
                    JOIN inscripcion i ON insc_x_seccion.idInscripcion = i.idInscripcion 
                    WHERE insc_x_seccion.idSeccion = %s 
                    AND i.fecha_inscripcion = %s AND i.fecha_expiracion = %s
                    ORDER BY i.fecha_inscripcion DESC
                ''', (idSeccion, fecha_desde, fecha_hasta))
                registro_periodos = cur.fetchall()

                periodoArray = []
                columPeriodo = [column[0] for column in cur.description]
                for record in registro_periodos:
                    periodoArray.append(dict(zip(columPeriodo, record)))
                
                # Si no hay períodos en el rango seleccionado
                if not periodoArray:
                    flash('No se encontraron períodos en el rango de fechas seleccionado')
                    return redirect(url_for('cursos.calificaciones', idSeccion=idSeccion))
                
                # Obtener calificaciones para TODOS los períodos en el rango
                cur.execute('''
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
                    WHERE c.idSeccion = %s 
                    AND i.fecha_inscripcion = %s AND i.fecha_expiracion = %s
                    ORDER BY i.fecha_inscripcion DESC, u.nombre, u.apellido
                ''', (idSeccion, fecha_desde, fecha_hasta))
                
                registro_calificaciones = cur.fetchall()

                insertCalificaciones = []
                columNamesCalificaciones = [column[0] for column in cur.description]
                for record in registro_calificaciones:
                    insertCalificaciones.append(dict(zip(columNamesCalificaciones, record)))

                # Formatear fechas para mostrar en el template
                for record in insertCalificaciones:
                    record['fecha_inscripcion'] = dateToString(record['fecha_inscripcion'])
                    record['fecha_expiracion'] = dateToString(record['fecha_expiracion'])
                
                # Pasar también las fechas seleccionadas al template para mostrarlas
                return render_template('cursos/calificaciones.html', 
                                    data=insertRegistro, 
                                    calificaciones=insertCalificaciones,
                                    periodoArray=periodoArray,
                                    fecha_desde_seleccionada=fecha_desde,
                                    fecha_hasta_seleccionada=fecha_hasta)
                
        except Exception as e:
            print(f"Error en filtrar_periodos: {e}")
            return redirect(url_for('cursos.calificaciones', idSeccion=idSeccion))
        


@cursos.route('/subir_logro_uno/<int:idSeccion>', methods = ['PATCH'])
@login_required
def subir_logro_uno(idSeccion):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    idInscripcion = data['idInscripcion']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_1 = %s WHERE idSeccion = %s AND idusuarios = %s AND idInscripcion = %s', (logro, idSeccion, idAlumno, idInscripcion))
            g.db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner calificación'}), 500
    


@cursos.route('/subir_logro_dos/<int:idSeccion>', methods = ['PATCH'])
@login_required
def subir_logro_dos(idSeccion):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    idInscripcion = data['idInscripcion']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_2 = %s WHERE idSeccion = %s AND idusuarios = %s AND idInscripcion = %s', (logro, idSeccion, idAlumno, idInscripcion))
            g.db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner calificación'}), 500

@cursos.route('/subir_logro_tres/<int:idSeccion>', methods = ['PATCH'])
@login_required
def subir_logro_tres(idSeccion):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    idInscripcion = data['idInscripcion']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_3 = %s WHERE idSeccion = %s AND idusuarios = %s AND idInscripcion = %s', (logro, idSeccion, idAlumno, idInscripcion))
            g.db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner calificación'}), 500
    


@cursos.route('/subir_logro_cuatro/<int:idSeccion>', methods = ['PATCH'])
def subir_logro_cuatro(idSeccion):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    idInscripcion = data['idInscripcion']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_4 = %s WHERE idSeccion = %s AND idusuarios = %s AND idInscripcion = %s', (logro, idSeccion, idAlumno, idInscripcion))
            g.db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner calificación'}), 500



@cursos.route('/subir_logro_cinco/<int:idSeccion>', methods = ['PATCH'])
@login_required
def subir_logro_cinco(idSeccion):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    idInscripcion = data['idInscripcion']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_5 = %s WHERE idSeccion = %s AND idusuarios = %s AND idInscripcion = %s', (logro, idSeccion, idAlumno, idInscripcion))
            g.db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner calificación'}), 500

@cursos.route('/subir_definitiva/<int:idSeccion>', methods = ['PATCH'])
@login_required
def subir_definitiva(idSeccion):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'definitiva' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    definitiva = data['definitiva']
    idAlumno = data['idAlumno']
    idInscripcion = data['idInscripcion']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET definitiva = %s WHERE idSeccion = %s AND idusuarios = %s AND idInscripcion = %s', (definitiva, idSeccion, idAlumno, idInscripcion))
            g.db.commit()

            double_def = float(definitiva)
            if (double_def > 14):
                cur.execute('UPDATE calificaciones SET aprobado = 1 WHERE idSeccion = %s AND idusuarios = %s AND idInscripcion = %s', (idSeccion, idAlumno, idInscripcion))
                g.db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        print(e)
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner calificación'}), 500

# FINALIZA ENDPOINTS DE CALIFICACIONES

@cursos.route('/asistencia/<int:id>', methods = ['PATCH'])
@login_required
def asistencia(id):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'asistencia' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    asist = data['asistencia']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE inscripcion SET asistencia = %s WHERE idInscripcion = %s', (asist, id))
            g.db.commit()
            return jsonify({'message': 'Asistencia actualizada satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner asistencia'}), 500
    
@cursos.route('/inasistencia/<int:id>', methods = ['PATCH'])
@login_required
def inasistencia(id):
    g.db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'inasistencia' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    asist = data['inasistencia']
    
    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE inscripcion SET inasistencia = %s WHERE idInscripcion = %s', (asist, id))
            g.db.commit()
            return jsonify({'message': 'Inasistencia actualizada satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al poner inasistencia'}), 500