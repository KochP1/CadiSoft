from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, Response, g
from flask_login import current_user, login_required
from flask_bcrypt import Bcrypt
import pymysql

profesores = Blueprint('profesores', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@profesores.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    # POST profesor
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        segundoNombre = request.form.get('segundoNombre')
        apellido = request.form.get('apellido')
        segundoApellido = request.form.get('segundoApellido')
        cedula = request.form.get('cedula')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')
        especialidad = request.form.get('especialidad')
        contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        try:
            imagen = request.files['imagen']
        except KeyError as e:
            imagen = None

        try:
            with g.db.cursor() as cur:
                if imagen == None:
                    sql_usuario = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    usuario = (
                        nombre,
                        segundoNombre,
                        apellido,
                        segundoApellido,
                        cedula,
                        email,
                        contraseña_hash,
                        rol
                        )
                
                else:
                    sql_usuario = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`, `imagen`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    imagen_blob = imagen.read()
                    usuario = (
                        nombre,
                        segundoNombre,
                        apellido,
                        segundoApellido,
                        cedula,
                        email,
                        contraseña_hash,
                        rol,
                        imagen_blob
                        )
                
                cur.execute(sql_usuario, usuario)
                g.db.commit()

                cur.execute('SELECT idusuarios FROM usuarios WHERE cedula = %s', (cedula,))
                idusuario = cur.fetchone()

                sql_profesor = 'INSERT INTO profesores (`idusuarios`, `especialidad`) VALUES (%s, %s)'
                profesor = (idusuario, especialidad)
                cur.execute(sql_profesor, profesor)
                g.db.commit()
                return jsonify({'mensaje': 'profesor creado satisfactiramente'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': 'Error al crear el usuario'}), 400

    # GET PROFESORES
    try:
        with g.db.cursor() as cur:
            sql = 'SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios'
            cur.execute(sql)
            registros = cur.fetchall()
            InsertRegistros = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                InsertRegistros.append(dict(zip(columNames, record)))

            return render_template('profesores/index.html', profesores = InsertRegistros)
    except Exception as e:
        return render_template('profesores/index.html')

@profesores.route('/eliminar_profesor/<int:idusuarios>', methods = ['DELETE'])
@login_required
def eliminar_profesor(idusuarios):
    try:
        with g.db.cursor() as cur:
            cur.execute('DELETE FROM usuarios WHERE idusuarios = %s', (idusuarios,))
            g.db.commit()
            return jsonify({'mensaje': 'profesor eliminado'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'el profesor no pudo ser eliminado'}), 400

@profesores.route('edit_profesores/<int:idusuarios>')
@login_required
def edit_profesores(idusuarios):
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.segundoApellido, u.cedula, u.email, u.imagen, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE p.idusuarios = %s', (idusuarios,))
            registros = cur.fetchall()
            InsertRegistros = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                InsertRegistros.append(dict(zip(columNames, record)))
            
            return render_template('profesores/editProfesor.html', profesor = InsertRegistros)
    except Exception as e:
        return redirect(url_for('profesores.index'))

@profesores.route('/filtrar_profesor', methods = ['POST'])
@login_required
def filtrar_profesor():
    cedula = request.form['cedula']

    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE u.cedula = %s', (cedula,))
            registros = cur.fetchall()
            InsertRegistros = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                InsertRegistros.append(dict(zip(columNames, record)))
            return render_template('profesores/index.html', profesores = InsertRegistros)
    except Exception as e:
        return url_for('profesores.index')

# MIS SECCIONES ROUTES

@profesores.route('/mis_secciones')
@login_required
def mis_secciones():
    if request.method == 'GET':
        try:
            with g.db.cursor() as cur:
                sql = 'SELECT s.idSeccion, s.idProfesor, s.idCurso, c.nombre_curso, c.duracionCurso, s.seccion FROM secciones s JOIN profesores p ON s.idProfesor = p.idProfesor JOIN usuarios u ON p.idusuarios = u.idusuarios JOIN cursos c ON s.idCurso = c.idCurso WHERE u.idusuarios = %s'
                cur.execute(sql, current_user.idusuarios)
                registros = cur.fetchall()
                insertSecciones = []
                columNames = [columns[0] for columns in cur.description]

                for record in registros:
                    insertSecciones.append(dict(zip(columNames, record)))

                for seccion in insertSecciones:
                    cur.execute('''SELECT COUNT(*) FROM insc_x_seccion isc 
                        JOIN inscripcion i ON isc.idInscripcion = i.idInscripcion 
                        JOIN secciones s ON isc.idSeccion = s.idSeccion 
                        JOIN usuarios u ON i.idUsuarios = u.idUsuarios
                        WHERE s.idSeccion = %s''', (seccion['idSeccion'],))
                    registrosParticipantes = cur.fetchone()
                    print(registrosParticipantes)
                    seccion['participantes'] = registrosParticipantes[0]

                print(insertSecciones)
                return render_template('profesores/secciones.html', secciones = insertSecciones)
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return f'Error: {e}'
        
@profesores.route('/carga_profesor/<int:profesor_id>')
def carga_profesor(profesor_id):
    try:
        with g.db.cursor() as cur:
            cur.execute('''
                SELECT 
                    COUNT(*) as total_secciones,
                    SUM(c.duracionCurso) as total_horas,
                    ROUND(SUM(c.duracionCurso) / COUNT(*), 1) as promedio
                FROM secciones s 
                INNER JOIN cursos c ON s.idCurso = c.idCurso 
                WHERE s.idProfesor = %s
            ''', (profesor_id,))
            
            metricas = cur.fetchone()
            
            cur.execute('''
                SELECT 
                    s.idSeccion,
                    c.nombre_curso,
                    s.seccion,
                    c.duracionCurso as horas_semanales
                FROM secciones s 
                INNER JOIN cursos c ON s.idCurso = c.idCurso 
                WHERE s.idProfesor = %s
                ORDER BY c.nombre_curso, s.seccion
            ''', (profesor_id,))
            
            secciones = cur.fetchall()
            
            return jsonify({
                'metricas': {
                    'total_secciones': metricas[0],
                    'total_horas': metricas[1],
                    'promedio_horas_seccion': float(metricas[2]) if metricas[2] else 0
                },
                'secciones': [
                    {
                        'idSeccion': seccion[0],
                        'curso': seccion[1],
                        'seccion': seccion[2],
                        'horas': seccion[3]
                    } for seccion in secciones
                ]
            })
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'Error al obtener carga de trabajo: {e}'})