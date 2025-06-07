from flask import jsonify, request, render_template, redirect, url_for, Blueprint, current_app

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
            print(insertSecciones)
            return render_template('cursos/seccionesCurso.html', secciones = insertSecciones)
        except Exception as e:
            print(f'\nError!!!: {e}\n')
            return redirect(url_for('cursos.index'))