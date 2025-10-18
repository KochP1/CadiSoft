from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

alumnos = Blueprint('alumnos', __name__, template_folder='templates', static_folder="static")

# ALUMNOS 
@alumnos.route('/', methods = ['GET'])
@login_required
def index():
    try:
        db = current_app.config['db']
        cur = db.cursor()
        sql = 'SELECT u.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email FROM usuarios u WHERE u.rol = %s'
        cur.execute(sql, ('alumno',))
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        return render_template('alumnos/index.html', alumnos = InsertRegistros)
    except Exception as e:
        return render_template('alumnos/index.html')
    finally:
        cur.close()

@alumnos.route('/buscar_alumno', methods = ['POST'])
@login_required
def buscar_alumno():
    db = current_app.config['db']
    cedula = request.form['cedula']
    rol = 'alumno'
    cur = db.cursor()
    sql = 'SELECT u.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email FROM usuarios u WHERE u.rol = %s AND u.cedula = %s'
    data = (rol, cedula)
    cur.execute(sql, data)
    registros = cur.fetchall()
    if len(registros) == 0:
        flash('Cédula incorrecta', 'error')
        return redirect(url_for('alumnos.index'))
    insertRegistros = []
    columNames = [column[0] for column in cur.description]
    for record in registros:
        insertRegistros.append(dict(zip(columNames, record)))
    return render_template('alumnos/index.html', alumnos = insertRegistros)



@alumnos.route('/eliminar_alumno/<int:idusuarios>', methods = ['DELETE'])
@login_required
def eliminar_alumno(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    try:
        cur.execute('DELETE FROM usuarios WHERE idusuarios = %s', (idusuarios))
        db.commit()
        return jsonify({'mensaje': 'alumno eliminado'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()



@alumnos.route('/edit_alumno/<int:idusuarios>')
@login_required
def edit_alumno(idusuarios):
    try:
        db = current_app.config['db']
        cur = db.cursor()
        sql = 'SELECT u.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, u.imagen FROM usuarios u WHERE u.idusuarios = %s'
        data = (idusuarios,)
        cur.execute(sql, data)
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        return render_template('alumnos/edit_alumno.html', alumnos = InsertRegistros)
    except Exception as e:
        return url_for('alumnos.index')
    finally:
        cur.close()

@alumnos.route('/constancia_estudio/<int:idAlumno>', methods = ['GET'])
@login_required
def constancia_estudio(idAlumno):
    db = current_app.config['db']

    with db.cursor() as cur:
        try:
            cur.execute('SELECT * FROM usuarios WHERE idusuarios = %s', (idAlumno,))
            registroAlumno = cur.fetchall()
            insertAlumno = []
            columNamesAlumno = [column[0] for column in cur.description]

            for record in registroAlumno:
                insertAlumno.append(dict(zip(columNamesAlumno, record)))

            cur.execute('SELECT c.nombre_curso, s.seccion, ca.definitiva FROM calificaciones ca JOIN secciones s ON ca.idSeccion = s.idSeccion JOIN cursos c ON s.idCurso = c.idCurso JOIN usuarios u ON ca.idusuarios = u.idusuarios WHERE ca.idusuarios = %s AND ca.definitiva > 9.6 AND ca.aprobado = 1', (idAlumno,))
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [column[0] for column in cur.description]

            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))

            return render_template('alumnos/constancia.html', constancia = insertRegistros, alumno = insertAlumno)
        except Exception as e:
            return f'Error: {e}'

# FINALIZAN ENDPOINTS DE ALUMNOS

# REGISTRO FAMILIAR

@alumnos.route('/crear_registro_familiar/<int:idusuarios>', methods = ['POST'])
@login_required
def crear_registro_familiar(idusuarios):
    db = current_app.config['db']
    db.ping(reconnect=True)

    nombrePapa = request.form.get('nombrePapa')
    apellidoPapa = request.form.get('apellidoPapa')
    nombreMama = request.form.get('nombreMama')
    apellidoMama = request.form.get('apellidoMama')
    contacto = request.form.get('contacto')

    try:
        with db.cursor() as cur:
            sql = 'INSERT INTO registro_familiar (`idusuarios`, `NombrePapa`, `ApellidoPapa`, `NombreMama`, `ApellidoMama`, `Telefono`) VALUES (%s, %s, %s, %s, %s, %s)'
            data = (idusuarios, nombrePapa, apellidoPapa, nombreMama, apellidoMama, contacto)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar creado satisfactoriamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error al crear registro familiar'}), 400




@alumnos.route('/registro_familiar', methods = ['GET'])
@login_required
def registro_familiar():
    db = current_app.config['db']
    if request.method == 'GET':
        cur = db.cursor()
        sql = 'SELECT f.idFamilia, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, f.NombrePapa, f.ApellidoPapa, f.NombreMama, f.ApellidoMama, f.Telefono FROM registro_familiar f JOIN usuarios u ON f.idusuarios = u.idusuarios'
        cur.execute(sql)
        registros = cur.fetchall()
        insertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            insertRegistros.append(dict(zip(columNames, record)))
        cur.close()
        return render_template('alumnos/registFamiliar.html', familias = insertRegistros)




@alumnos.route('/edit_registro_familiar/<int:idFamilia>')
@login_required
def edit_registro_familiar(idFamilia):
    db = current_app.config['db']
    try:
        with db.cursor() as cur:
            sql = 'SELECT f.idFamilia, u.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, f.NombrePapa, f.ApellidoPapa, f.NombreMama, f.ApellidoMama, f.Telefono FROM registro_familiar f JOIN usuarios u ON f.idusuarios = u.idusuarios WHERE f.idFamilia = %s'
            cur.execute(sql, (idFamilia,))
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))
            return render_template('alumnos/edit_registro_familiar.html', familia = insertRegistros)
    except Exception as e:
        return f'Error: {e}'




@alumnos.route('/edit_registro_fam_papa/<int:idFamilia>', methods = ['PATCH'])
@login_required
def edit_registro_fam_papa(idFamilia):
    db = current_app.config['db']
    NombrePapa = request.form.get('NombrePapa')
    ApellidoPapa = request.form.get('ApellidoPapa')

    if not NombrePapa or not ApellidoPapa:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    try:
        with db.cursor() as cur:
            sql = 'UPDATE registro_familiar SET NombrePapa = %s, ApellidoPapa = %s WHERE idFamilia = %s'
            data = (NombrePapa, ApellidoPapa, idFamilia)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar actualizado satisfactoriamente'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al actualizar datos del papa: {e}'}), 500




@alumnos.route('/edit_registro_fam_mama/<int:idFamilia>', methods = ['PATCH'])
@login_required
def edit_registro_fam_mama(idFamilia):
    db = current_app.config['db']
    NombreMama = request.form.get('NombreMama')
    ApellidoMama = request.form.get('ApellidoMama')
    try:
        with db.cursor() as cur:
            sql = 'UPDATE registro_familiar SET NombreMama = %s, ApellidoMama = %s WHERE idFamilia = %s'
            data = (NombreMama, ApellidoMama, idFamilia)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar actualizado satisfactoriamente'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al actualizar datos de la mama: {e}'}), 500




@alumnos.route('/edit_registro_fam_contacto/<int:idFamilia>', methods = ['PATCH'])
@login_required
def edit_registro_fam_contacto(idFamilia):
    db = current_app.config['db']
    contacto = request.form.get('contacto')
    try:
        with db.cursor() as cur:
            sql = 'UPDATE registro_familiar SET Telefono = %s WHERE idFamilia = %s'
            data = (contacto, idFamilia)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar actualizado satisfactoriamente'}), 200
    except Exception as e:
        return jsonify({'error': f'Error al actualizar contacto de la familia: {e}'}), 500




@alumnos.route('/eliminar_registro_familiar/<int:idRegistro>', methods = ['DELETE'])
@login_required
def eliminar_registro_familiar(idRegistro):
    db = current_app.config['db']
    try:
        with db.cursor() as cur:
            sql = 'DELETE FROM registro_familiar WHERE idFamilia = %s'
            cur.execute(sql, (idRegistro,))
            db.commit()
            return jsonify({'message': 'Registro familiar eliminado satisfactoriamente'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'Error al eliminar registro familiar: {e}'}), 500




@alumnos.route('/buscar_registro_familiar', methods = ['POST'])
@login_required
def buscar_registro_familiar():
    try:
        db = current_app.config['db']
        cedula = request.form['cedula']
        cur = db.cursor()
        sql = 'SELECT f.idFamilia, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, f.NombrePapa, f.ApellidoPapa, f.NombreMama, f.ApellidoMama, f.Telefono FROM registro_familiar f JOIN usuarios u ON f.idusuarios = u.idusuarios WHERE u.cedula = %s'
        data = (cedula,)
        cur.execute(sql, data)
        registros = cur.fetchall()

        if len(registros) == 0:
            flash('Cédula incorrecta', 'error')
            return redirect(url_for('alumnos.registro_familiar'))
        insertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            insertRegistros.append(dict(zip(columNames, record)))
        return render_template('alumnos/registFamiliar.html', familias = insertRegistros)
    except Exception as e:
        return redirect(url_for('alumnos.registro_familiar'))

# FINALIZA REGISTRO FAMILIAR

# DASHBOARD DE ALUMNOS

@alumnos.route('/dashboard')
def dashboard():
    try:
        db = current_app.config['db']
        with db.cursor() as cur:
            cur.execute("""
                SELECT 
                    sum(c.definitiva) as sumaPromedio, COUNT(*) as cantidad
                FROM calificaciones c 
                JOIN inscripcion i ON c.idInscripcion = i.idInscripcion 
                JOIN usuarios u ON c.idusuarios = u.idusuarios 
                WHERE u.idusuarios = %s AND c.aprobado = 1;
            """, (current_user.idusuarios,))
            sumaPromedio = cur.fetchone()

            cur.execute("""
                SELECT sum(asistencia) as asistencias FROM inscripcion i INNER JOIN usuarios u ON i.idusuarios = u.idusuarios 
                        WHERE u.idusuarios = %s;
            """, (current_user.idusuarios,))
            asistencias = cur.fetchone()

            cur.execute("""
                SELECT sum(inasistencia) as inasistencias FROM inscripcion i INNER JOIN usuarios u ON i.idusuarios = u.idusuarios 
                        WHERE u.idusuarios = %s;
            """, (current_user.idusuarios,))
            inasistencias = cur.fetchone()

            promedio = sumaPromedio[0]/sumaPromedio[1]
            cursos = sumaPromedio[1]
        return render_template('alumnos/dashboard.html', promedio = promedio, cursos = cursos, asistencias = asistencias[0], inasistencias = inasistencias[0])
    except Exception as e:
        db.rollback()
        print(e)
        return f'{e}'

@alumnos.route('/mis_calificaciones')
def mis_calificaciones():
    return render_template('alumnos/calificaciones.html')

# FINALIZA DAHSBOARD DE ALUMNOS