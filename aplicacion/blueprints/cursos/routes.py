from flask import jsonify, request, render_template, redirect, url_for, Blueprint, current_app
from datetime import date

cursos = Blueprint('cursos', __name__, template_folder='templates', static_folder="static")

# ENDPOINTS DE CURSOS

@cursos.route('/', methods = ['GET', 'POST'])
def index():
    db = current_app.config['db']
    db.ping(reconnect=True)

    if request.method == 'POST':
        facultad = request.form.get('idFacultad')
        curso = request.form.get('nombre_curso')

        try:
            with db.cursor() as cur:
                sql = 'INSERT INTO cursos (`idFacultad`, `nombre_curso`) VALUES (%s, %s)'
                data = (facultad, curso)
                cur.execute(sql, data)
                return jsonify({'message': 'Curso creado satisfactoriamente'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'Error al crear curso'}), 400

    try:
        with db.cursor() as cur:
            sql = 'SELECT c.idCurso, f.idFacultad, f.facultad, c.nombre_curso FROM cursos c JOIN facultades f ON c.idFacultad = f.idFacultad'
            cur.execute(sql)
            registros = cur.fetchall()
            insertCursos = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertCursos.append(dict(zip(columNames, record)))
            print(insertCursos)
            return render_template('cursos/index.html', cursos = insertCursos)
    except Exception as e:
        print(e)



@cursos.route('/buscar_facultades')
def buscar_facultades():
    try:
        db = current_app.config['db']
        db.ping(reconnect=True)
        
        with db.cursor() as cur:
            sql = 'SELECT * FROM facultades'
            cur.execute(sql)
            facultades = cur.fetchall()

            if facultades:
                columNames = [column[0] for column in cur.description]
                facultades_dict = [dict(zip(columNames, row)) for row in facultades]

                return jsonify({'facultades': facultades_dict}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al buscar facultades'}), 400
    


@cursos.route('/edit_cursos/<int:idCurso>', methods = ['GET'])
def edit_cursos(idCurso):
    db = current_app.config['db']
    db.ping(reconnect=True)

    try:
        with db.cursor() as cur:
            sql = 'SELECT c.idCurso, c.idFacultad, c.nombre_curso, c.imagen, f.facultad FROM cursos c JOIN facultades f ON c.idFacultad = f.idFacultad WHERE c.idCurso = %s'
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
                print(idFacultad)
            
            for record in insertRegistrosFacultades:
                if idFacultad == record['idFacultad']:
                    record.clear()

            return render_template('cursos/editarCurso.html', cursos = insertRegistros, facultades = insertRegistrosFacultades)
    except Exception as e:
        print(e)



@cursos.route('/edit_nombre_curso/<int:idCurso>', methods = ['PATCH'])
def edit_nombre_curso(idCurso):
    db = current_app.config['db']
    db.ping(reconnect=True)
    curso = request.form.get('curso')

    if not curso:
        return jsonify({'error': 'Faltan campos'}), 400
    
    try:
        with db.cursor() as cur:
            sql = 'UPDATE cursos SET nombre_curso = %s WHERE idCurso = %s'
            data = (curso, idCurso)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Curso modificado satisfactoriamente'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al modificar curso'}), 500
    


@cursos.route('/edit_facultad_curso/<int:idCurso>', methods = ['PATCH'])
def edit_facultad_curso(idCurso):
    db = current_app.config['db']
    db.ping(reconnect=True)
    facultad = request.form.get('facultad')

    if not facultad:
        return jsonify({'error': 'Faltan campos'}), 400
    
    try:
        with db.cursor() as cur:
            sql = 'UPDATE cursos SET idFacultad = %s WHERE idCurso = %s'
            data = (facultad, idCurso)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Curso modificado satisfactoriamente'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al modificar curso'}), 500


@cursos.route('/eliminar_curso/<int:idcurso>', methods = ['DELETE'])
def eliminar_curso(idcurso):
    db = current_app.config['db']
    cur = db.cursor()

    try:
        cur.execute('DELETE FROM cursos WHERE idCurso = %s', (idcurso,))
        db.commit()
        return jsonify({'mensaje': 'curso eliminado'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'el curso no pudo ser eliminado'}), 400
    finally:
        cur.close()

# FINALIZA ENDPOINTS DE CURSOS

# ENDPOINTS DE SECCIONES POR CURSO
@cursos.route('/seccion_curso/<int:idcurso>')
def seccion_curso(idcurso):
    db = current_app.config['db']

    with db.cursor() as cur:
        db.ping(reconnect=True)
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
            print(f'\nError!!!: {e}\n')
            return redirect(url_for('cursos.index'))



@cursos.route('/craer_seccion/<int:idCurso>', methods = ['GET', 'POST'])
def crear_seccion(idCurso):
    db = current_app.config['db']
    db.ping(reconnect=True)

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
            
            with db.cursor() as cur:
                cur.execute('INSERT INTO secciones (`idCurso`, `idProfesor`, `seccion`) VALUES (%s, %s, %s)', (idCurso, profesor, seccion))
                db.commit()

                cur.execute('SELECT idSeccion FROM secciones WHERE seccion = %s', (seccion,))
                idSeccion = cur.fetchone()

                for record in horarios:
                    cur.execute('INSERT INTO horario (`horario_dia`, `horario_hora`, `horario_hora_final`, `horario_aula`) VALUES (%s, %s, %s, %s)', (record['dia'], record['hora_inicio'], record['hora_fin'], aula))
                    db.commit()

                    cur.execute('SELECT idhorario FROM horario ORDER BY idhorario DESC LIMIT 1')
                    idhorario = cur.fetchone()

                    cur.execute('INSERT INTO horario_x_curso (`idhorario`, `idSeccion`) VALUES (%s, %s)', (idhorario, idSeccion))
                    db.commit()

                return jsonify({'message': 'Sección creada satisfactoriamente'}), 200
        except Exception as e:
            db.rollback()
            print(e)
            return jsonify({'error': 'Error al crear sección'}), 500

    if request.method == 'GET':
        try:
            with db.cursor() as cur:
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
            print(e)
            return redirect(url_for('cursos.index'))




@cursos.route('/elim_seccion/<int:idSeccion>', methods = ['DELETE'])
def elim_seccion(idSeccion):
    db = current_app.config['db']
    db.ping(reconnect=True)

    if not idSeccion:
        return jsonify({'error': 'Faltan campos'})

    try:
        with db.cursor() as cur:
            sql = 'DELETE FROM secciones WHERE idSeccion = %s'
            cur.execute(sql, (idSeccion,))
            db.commit()
            return jsonify({'message': 'Sección eliminada satisfactoriamente'})
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'Error al eliminar seccion'}), 500

# FINALIZA ENDPOINTS DE SECCIONES

# ENDPOINTS DE CALIFICACIONES

def dateToString(fecha: date) -> str:
    return f"{fecha.day:02d}/{fecha.month:02d}/{fecha.year}"

@cursos.route('/calificaciones/<idSeccion>', methods = ['GET'])
def calificaciones(idSeccion):
    db = current_app.config['db']
    db.ping(reconnect=True)

    if request.method == 'GET':
        try:
            with db.cursor() as cur:
                cur.execute('SELECT s.idSeccion, c.nombre_curso, s.seccion FROM secciones s JOIN cursos c ON s.idCurso = c.idCurso WHERE s.idSeccion = %s', (idSeccion,))
                registro = cur.fetchall()

                insertRegistro = []
                columNames = [column[0] for column in cur.description]
                for record in registro:
                    insertRegistro.append(dict(zip(columNames, record)))
                
                cur.execute('SELECT fecha_inscripcion, fecha_expiracion FROM inscripcion WHERE fecha_inscripcion <= CURDATE() ORDER BY fecha_inscripcion DESC LIMIT 1')
                registro_periodo = cur.fetchall()
                print(registro_periodo)


                periodoArray = []
                columPeriodo = [column[0] for column in cur.description]
                for record in registro_periodo:
                    periodoArray.append(dict(zip(columPeriodo, record)))
                
                for record in periodoArray:
                    inicioPeriodo = record['fecha_inscripcion']
                
                cur.execute('SELECT c.idCalificacion, c.idAlumno, u.nombre, u.segundoNombre, u.apellido, u.segundoApellido, u.cedula, i.fecha_inscripcion, i.fecha_expiracion, i.es_activa, c.logro_1, c.logro_2, c.logro_3, c.logro_4, c.logro_5, c.definitiva FROM calificaciones c JOIN inscripcion i ON c.idInscripcion = i.idInscripcion JOIN alumnos a ON c.idAlumno = a.idAlumno JOIN usuarios u ON u.idusuarios = a.idusuarios WHERE c.idSeccion = %s AND i.fecha_inscripcion = %s', (idSeccion, inicioPeriodo))
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
            print(e)
            return redirect(url_for('cursos.index'))
        


@cursos.route('/subir_logro_uno/<int:idSeccion>', methods = ['PATCH'])
def subir_logro_uno(idSeccion):
    db = current_app.config['db']
    db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    
    try:
        with db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_1 = %s WHERE idSeccion = %s AND idAlumno = %s', (logro, idSeccion, idAlumno))
            db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'Error al poner calificación'}), 500
    


@cursos.route('/subir_logro_dos/<int:idSeccion>', methods = ['PATCH'])
def subir_logro_dos(idSeccion):
    db = current_app.config['db']
    db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    
    try:
        with db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_2 = %s WHERE idSeccion = %s AND idAlumno = %s', (logro, idSeccion, idAlumno))
            db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'Error al poner calificación'}), 500

@cursos.route('/subir_logro_tres/<int:idSeccion>', methods = ['PATCH'])
def subir_logro_tres(idSeccion):
    db = current_app.config['db']
    db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    
    try:
        with db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_3 = %s WHERE idSeccion = %s AND idAlumno = %s', (logro, idSeccion, idAlumno))
            db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'Error al poner calificación'}), 500
    


@cursos.route('/subir_logro_cuatro/<int:idSeccion>', methods = ['PATCH'])
def subir_logro_cuatro(idSeccion):
    db = current_app.config['db']
    db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    
    try:
        with db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_4 = %s WHERE idSeccion = %s AND idAlumno = %s', (logro, idSeccion, idAlumno))
            db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'Error al poner calificación'}), 500



@cursos.route('/subir_logro_cinco/<int:idSeccion>', methods = ['PATCH'])
def subir_logro_cinco(idSeccion):
    db = current_app.config['db']
    db.ping(reconnect=True)

    data = request.get_json()

    if not data or 'logro' not in data or 'idAlumno' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400
    
    logro = data['logro']
    idAlumno = data['idAlumno']
    
    try:
        with db.cursor() as cur:
            cur.execute('UPDATE calificaciones SET logro_5 = %s WHERE idSeccion = %s AND idAlumno = %s', (logro, idSeccion, idAlumno))
            db.commit()
            return jsonify({'message': 'Calificación actualizada satisfactoriamente'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'Error al poner calificación'}), 500



# FINALIZA ENDPOINTS DE CALIFICACIONES
