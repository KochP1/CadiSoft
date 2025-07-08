from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, Response
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

profesores = Blueprint('profesores', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@profesores.route('/', methods = ['GET', 'POST'])
def index():
    db = current_app.config['db']
    cur = db.cursor()

    # POST profesor
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        segundoNombre = request.form.get('segundoNombre')
        apellido = request.form.get('apellido')
        segundoApellido = request.form.get('segundoApellido')
        cedula = request.form.get('cedula')
        email = request.form.get('email')
        contraseña = request.form.get('email')
        rol = request.form.get('rol')
        especialidad = request.form.get('especialidad')
        contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        try:
            imagen = request.files['imagen']
        except KeyError as e:
            imagen = None

        try:
            if imagen == None:
                sql_usuario = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
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
            db.commit()

            cur.execute('SELECT idusuarios FROM usuarios WHERE cedula = %s', (cedula,))
            idusuario = cur.fetchone()

            sql_profesor = 'INSERT INTO profesores (`idusuarios`, `especialidad`) VALUES (%s, %s)'
            profesor = (idusuario, especialidad)
            cur.execute(sql_profesor, profesor)
            db.commit()
            return jsonify({'mensaje': 'profesor creado satisfactiramente'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'Error al crear el usuario'}), 400
        finally:
            cur.close()

    # GET PROFESORES
    try:
        sql = 'SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios'
        cur.execute(sql)
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))

        return render_template('profesores/index.html', profesores = InsertRegistros)
    except Exception as e:
        print(e)
        return render_template('profesores/index.html')
    finally:
        cur.close()

@profesores.route('/eliminar_profesor/<int:idusuarios>', methods = ['DELETE'])
def eliminar_profesor(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    try:
        cur.execute('DELETE FROM usuarios WHERE idusuarios = %s', (idusuarios,))
        db.commit()
        return jsonify({'mensaje': 'profesor eliminado'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'el profesor no pudo ser eliminado'}), 400
    finally:
        cur.close()


@profesores.route('edit_profesores/<int:idusuarios>')
def edit_profesores(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    try:
        cur.execute('SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.segundoApellido, u.cedula, u.email, u.imagen, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE p.idusuarios = %s', (idusuarios,))
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        
        return render_template('profesores/editProfesor.html', profesor = InsertRegistros)
    except Exception as e:
        print(e)
        return redirect(url_for('profesores.index'))
    finally:
        cur.close()

@profesores.route('/filtrar_profesor', methods = ['POST'])
def filtrar_profesor():
    db = current_app.config['db']
    cur = db.cursor()

    cedula = request.form['cedula']

    try:
        cur.execute('SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, p.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios WHERE u.cedula = %s', (cedula,))
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        return render_template('profesores/index.html', profesores = InsertRegistros)
    except Exception as e:
        print(e)
        return url_for('profesores.index')
    finally:
        cur.close()

@profesores.route('/mis_secciones')
def mis_secciones():
    db = current_app.config['db']
    if request.method == 'GET':
        try:
            return render_template('profesores/secciones.html')
        except Exception as e:
            print(e)
            return 'Error'