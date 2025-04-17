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
        if not request.is_json:
            return jsonify({"error": "El cuerpo debe ser JSON"}), 400
            
        data = request.get_json()

        required_fields = ['nombre', 'segundoNombre', 'apellido', 'segundoApellido', 'cedula', 'email', 'contraseña', 'rol', 'especialidad']

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'faltan campos'}), 400
        
        try:
            sql_usuario = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`, `imagen`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            contraseña_hash = bcrypt.generate_password_hash(data['contraseña']).decode('utf-8')
            usuario = (
                data['nombre'], 
                data['segundoNombre'], 
                data['apellido'],
                data['segundoApellido'],
                data['cedula'],
                data['email'],
                contraseña_hash,
                data['rol'],
                data['imagen']
                )
            cur.execute(sql_usuario, usuario)
            db.commit()

            cur.execute('SELECT idusuarios FROM usuarios WHERE cedula = %s', (data['cedula'],))
            idusuario = cur.fetchone()

            sql_profesor = 'INSERT INTO profesores (`idusuarios`, `idespecialidad`) VALUES (%s, %s)'
            profesor = (idusuario, data['especialidad'])
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
        sql = 'SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, e.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios JOIN especialidad e ON p.idespecialidad = e.idespecialidad'
        cur.execute(sql)
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        cur.close()

        cur = db.cursor()
        sql_especialidades = 'SELECT * FROM especialidad'
        cur.execute(sql_especialidades)
        especialidad = cur.fetchall()
        insertEspecialidad = []
        columNamesEspecialidad = [column[0] for column in cur.description]
        for record in especialidad:
            insertEspecialidad.append(dict(zip(columNamesEspecialidad, record)))
        print(insertEspecialidad)

        return render_template('profesores/index.html', profesores = InsertRegistros, especialidades = insertEspecialidad)
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
        cur.execute('SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.segundoApellido, u.email, u.imagen, e.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios JOIN especialidad e ON p.idespecialidad = e.idespecialidad WHERE p.idusuarios = %s', (idusuarios,))
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