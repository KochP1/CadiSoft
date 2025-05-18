from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash, Response
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

from . model import User

usuario = Blueprint('usuario', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@usuario.route('/', methods = ['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('usuario.inicio'))
    if request.method == 'POST':
        db = current_app.config['db']
        cedula = request.form['cedula']
        contraseña = request.form['contraseña']

        user = User.get_by_cedula(db, cedula)

        if user and bcrypt.check_password_hash(user.contraseña, contraseña):
            if user.rol == 'administrador':
                login_user(user)
                return redirect(url_for('usuario.inicio'))
            else:
                return render_template('usuarios/index.html', message_error = 'Permisos insuficientes')
        else:
            return render_template('usuarios/index.html', message_error = 'Credenciales incorrectas')


    return render_template('usuarios/index.html')

@usuario.route('/inicio')
def inicio():
    return render_template('usuarios/inicio.html')

@usuario.route('/inicio_stats')
def inicio_stats():
    db = current_app.config['db']
    db.ping(reconnect=True)
    
    alumnosArray = []
    profesoresArray = []
    cursosArray = []
    facultadesArray = []

    try:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM alumnos')
            alumnos = cur.fetchall()

            cur.execute('SELECT * FROM profesores')
            profesores = cur.fetchall()

            cur.execute('SELECT * FROM cursos')
            cursos = cur.fetchall()

            cur.execute('SELECT * FROM facultades')
            facultades = cur.fetchall()

            for data in alumnos:
                alumnosArray.append(data)
            
            for data in profesores:
                profesoresArray.append(data)
            
            for data in cursos:
                cursosArray.append(data)
            
            for data in facultades:
                facultadesArray.append(data)

            return jsonify({'mensaje': 'Request exitoso', 'alumnos': f'{len(alumnosArray)}', 'profesores': f'{len(profesoresArray)}', 'cursos': f'{len(cursosArray)}', 'facultades': f'{len(facultadesArray)}',}), 200

    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': 'Request fallido'}), 400

@usuario.route('/regist_user', methods = ['GET', 'POST'])
def regist_user():
    if request.method == 'GET':
        return render_template('usuarios/regist.html')
    
    if request.method == 'POST':

        try:
            db = current_app.config['db']
            cur = db.cursor()

            campos = {
                'nombre': (request.form['nombre'], 12),
                'segundoNombre': (request.form['segundoNombre'], 12),
                'apellido': (request.form['apellido'], 20),
                'segundoApellido': (request.form['segundoApellido'], 20),
                'cedula': (request.form['cedula'], 11),
                'email': (request.form['email'], 50),
                'contraseña': (request.form['contraseña'], 8)
            }
            for campo, (valor, max_len) in campos.items():
                if len(valor) > max_len:
                    return render_template('usuarios/regist.html', message_error=f'El campo {campo.replace("Nombre", "nombre")} es muy largo (máx {max_len} caracteres)')
                elif len(valor) == 0:
                    return render_template('usuarios/regist.html', message_error=f'El campo {campo.replace("Nombre", "nombre")} esta vacio')
            
            nombre = request.form['nombre']
            segundoNombre = request.form['segundoNombre']
            apellido = request.form['apellido']
            segundoApellido = request.form['segundoApellido']
            cedula = request.form['cedula']
            email = request.form['email']
            contraseña = request.form['contraseña']
            rol = 'administrador'
            contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

            sql = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            data = (nombre, segundoNombre, apellido, segundoApellido, cedula, email, contraseña_hash, rol)
            cur.execute(sql, data)
            db.commit()
            flash('Usuario creado satisfactoriamente')
            return redirect(url_for('usuario.index'))
        except Exception as e:
            print(f'Error: {e}')
            return redirect(url_for('usuario.regist_user'))
        finally:
            cur.close()

@usuario.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    return render_template('usuarios/forgot.html')

@usuario.route('/ajustes_usuario')
def ajustes_usuario():
    return render_template('usuarios/ajustes.html')

@usuario.route('/get_profile_image/<int:idusuarios>')
def get_profile_image(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    cur.execute('SELECT imagen FROM usuarios WHERE idusuarios = %s', (idusuarios,))
    image_data = cur.fetchone()[0]

    # Determinar el tipo MIME basado en los primeros bytes
    mime_type = 'image/jpeg'
    if image_data.startswith(b'\x89PNG'):
        mime_type = 'image/png'
    elif image_data.startswith(b'\xff\xd8'):
        mime_type = 'image/jpeg'
    
    return Response(image_data, mimetype=mime_type)

@usuario.route('/update_foto/<int:idusuarios>', methods = ['PATCH'])
def update_foto(idusuarios):
    imagen = request.files['imagen']  # Archivo binario
        
    # Convertir imagen a Base64 o guardarla como BLOB
    imagen_blob = imagen.read()  # Binario puro (para MySQL LONGBLOB)

    db = current_app.config['db']
    cur = db.cursor()

    try:
        cur.execute('UPDATE usuarios SET imagen = %s WHERE idusuarios = %s', (imagen_blob, idusuarios))
        db.commit()
        return jsonify({'mensaje': 'imagen de perfil actualizada', 'usuario': f'{idusuarios}'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()

@usuario.route('/update_email/<int:idusuarios>', methods = ['PATCH'])
def update_email(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400
            
    data = request.get_json()

    required_fields = ['email']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400
    
    try:
        cur.execute('UPDATE usuarios SET email = %s WHERE idusuarios = %s', (data['email'], idusuarios))
        db.commit()
        return jsonify({'mensaje': 'email actualizado', 'usuario': f'{idusuarios}'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()

@usuario.route('/edit_nombres/<int:idusuarios>', methods = ['PATCH'])
def edit_nombres(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400
            
    data = request.get_json()

    required_fields = ['nombre', 'segundoNombre']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400
    
    try:
        cur.execute('UPDATE usuarios SET nombre = %s, segundoNombre = %s WHERE idusuarios = %s', (data['nombre'], data['segundoNombre'], idusuarios))
        db.commit()
        return jsonify({'mensaje': 'nombres actualizados', 'usuario': f'{idusuarios}'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()

@usuario.route('/edit_apellidos/<int:idusuarios>', methods = ['PATCH'])
def edit_apellidos(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400
            
    data = request.get_json()

    required_fields = ['apellido', 'segundoApellido']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400
    
    try:
        cur.execute('UPDATE usuarios SET apellido = %s, segundoApellido = %s WHERE idusuarios = %s', (data['apellido'], data['segundoApellido'], idusuarios))
        db.commit()
        return jsonify({'mensaje': 'apellidos actualizados', 'usuario': f'{idusuarios}'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()

@usuario.route('/edit_cedula/<int:idusuarios>', methods = ['PATCH'])
def edit_cedula(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400
            
    data = request.get_json()

    required_fields = ['cedula']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400
    
    try:
        cur.execute('UPDATE usuarios SET cedula = %s WHERE idusuarios = %s', (data['cedula'], idusuarios))
        db.commit()
        return jsonify({'mensaje': 'cedula actualizada', 'usuario': f'{idusuarios}'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()

@usuario.route('/edit_contraseña/<int:idusuarios>', methods = ['PATCH'])
def edit_contraseña(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    if not request.json:
        return jsonify({'error': 'el cuerpo debe ser JSON'}), 400
    
    data = request.get_json()

    required_fields = ['contraseñaActual', 'contraseñaNueva']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'faltan campos'}), 400
    
    try:
        if bcrypt.check_password_hash(current_user.contraseña, data['contraseñaActual']):
            contraseñaNueva = bcrypt.generate_password_hash(data['contraseñaNueva']).decode('utf-8')
            cur.execute('UPDATE usuarios SET contraseña = %s WHERE idusuarios = %s', (contraseñaNueva, idusuarios))
            db.commit()
            return jsonify({'mensaje': 'contraseña actualizada', 'usuario': f'{idusuarios}'})
        else:
            return jsonify({'error': 'la contraseña actual es incorrecta'}), 401
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()

@usuario.route('/log_out', methods = ['POST'])
def log_out():
    try:
        usuarioid = current_user.id
        logout_user()
        return jsonify({'mensaje': 'sesión cerrada', 'usuario': usuarioid}), 200
    except Exception as e:
        print(e)
        return jsonify({'mensaje': 'Error al cerrar sesión'}), 400