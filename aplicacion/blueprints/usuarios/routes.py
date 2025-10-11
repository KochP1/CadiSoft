from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash, Response, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from flask_bcrypt import Bcrypt
import random, datetime as dt

import pymysql
from . model import User

usuario = Blueprint('usuario', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@usuario.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        db = current_app.config['db']
        cedula = request.form['cedula']
        contraseña = request.form['contraseña']

        user = User.get_by_cedula(db, cedula)

        if user and bcrypt.check_password_hash(user.contraseña, contraseña):
            if user.rol == 'administrador':
                login_user(user, remember=True, force=True)
                return redirect(url_for('usuario.inicio'))
            
            if user.rol == 'profesor':
                print('Cumpliendo ', user.rol)
                login_user(user)
                return redirect(url_for('profesores.mis_secciones'))
            

            return render_template('usuarios/index.html', message_error = 'Permisos insuficientes')
        else:
            return render_template('usuarios/index.html', message_error = 'Credenciales incorrectas')


    return render_template('usuarios/index.html')



@usuario.route('/inicio')
def inicio():
    try:
        return render_template('usuarios/inicio.html')
    except Exception as e:
        print(e)
        return 'Error'



@usuario.route('/inicio_stats')
def inicio_stats():
    db = current_app.config['db']
    db.ping(reconnect=True)

    try:
        with db.cursor() as cur:
            cur.execute('SELECT COUNT(*) AS total FROM usuarios WHERE rol = %s', ('alumno',))
            alumnos = cur.fetchone()

            cur.execute('SELECT COUNT(*) AS total FROM profesores')
            profesores = cur.fetchone()

            cur.execute('SELECT COUNT(*) AS total FROM cursos')
            cursos = cur.fetchone()

            cur.execute('SELECT COUNT(*) AS total FROM facultades')
            facultades = cur.fetchone()

        with db.cursor(pymysql.cursors.DictCursor) as cur:

            sql = "SELECT MONTH(fecha_inscripcion) as mes, COUNT(*) as total FROM inscripcion WHERE YEAR(fecha_inscripcion) = YEAR(CURDATE()) GROUP BY MONTH(fecha_inscripcion) ORDER BY mes "
            cur.execute(sql)
            results = cur.fetchall()

            meses_completos = [0] * 12
            nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            
            for resultado in results:
                mes = resultado['mes'] - 1
                total = resultado['total']
                meses_completos[mes] = total

            return jsonify(
                {'mensaje': 'Request exitoso', 
                'alumnos': f'{alumnos[0]}', 
                'profesores': f'{profesores[0]}', 
                'cursos': f'{cursos[0]}', 
                'facultades': f'{facultades[0]}',
                'meses': nombres_meses,
                'inscripciones': meses_completos
                }), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': 'Request fallido'}), 500

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
            return redirect(url_for('usuario.regist_user'))
        finally:
            cur.close()



def generar_codigo_verificacion(usuario_id):
    db = current_app.config['db']
    db.ping(reconnect=True)

    codigo = str(random.randint(100000, 999999))
    
    expiracion = dt.datetime.now() + dt.timedelta(minutes=15)
    
    try:
        with db.cursor() as cur:
            cur.execute(
                """ UPDATE codigos_verificacion 
                    SET usado = TRUE 
                    WHERE idusuarios = %s 
                    AND usado = FALSE 
                    AND expiracion > NOW() """,
                (usuario_id,)
            )
            
            cur.execute(
                """ DELETE FROM codigos_verificacion 
                    WHERE idusuarios = %s 
                    AND expiracion < NOW() - INTERVAL 7 DAY """,
                (usuario_id,)
            )
            
            
            cur.execute(
                """ INSERT INTO codigos_verificacion 
                    (idusuarios, codigo, expiracion) 
                    VALUES (%s, %s, %s) """,
                (usuario_id, codigo, expiracion)
            )
            db.commit()
            
            return codigo
    except Exception as e:
        db.rollback()
        current_app.logger.error(f"Error al guardar código: {str(e)}")
        raise


from threading import Thread
def send_mail_async(app, email, id):
    with app.app_context():
        try:
            mail = current_app.config['mail']
            codigo = generar_codigo_verificacion(id)

            html_body = f"""
                <html>
                <head>
                    <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ 
                        background-color: #833d3d;
                        color: white;
                        padding: 20px;
                        text-align: center;
                    }}
                    .code {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #833d3d;
                        margin: 20px 0;
                        text-align: center;
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 12px;
                        color: #777;
                        text-align: center;
                    }}
                    </style>
                </head>
                <body>
                    <div class="header">
                    <h1>Recuperación de cuenta cadiSoft</h1>
                    </div>
                    
                    <p>Hola,</p>
                    <p>Has solicitado un código de verificación para recuperar tu cuenta.</p>
                    
                    <div class="code">
                    Tu código es: {codigo}
                    </div>
                    
                    <p>Este código expirará en 15 minutos.</p>
                    
                    <div class="footer">
                    <p>© {dt.datetime.now().year} CadiSoft - Todos los derechos reservados</p>
                    <img src="http://127.0.0.1:5000/images/Cadi_logo-removeBG.png" alt="Logo cadiSoft" width="150">
                    </div>
                </body>
                </html>
                """
            
            msg = Message(
            "Recuperación de cuenta cadiSoft",
            recipients=[email],
            html = html_body,
            body=f"Tu codigo de verifiación es: {codigo}"
            )
            mail.send(msg)
        except Exception as e:
            print(f'Error al enviar correo: {e}')

def send_mail(email, idusuarios):
    thread = Thread(target=send_mail_async, args=(current_app._get_current_object(), email, idusuarios))
    thread.start()

@usuario.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        db = current_app.config['db']
        db.ping(reconnect=True)
        email = request.form.get('email')

        try:
            with db.cursor() as cur:
                sql = 'SELECT idusuarios, email FROM usuarios WHERE email = %s'
                data = (email,)
                cur.execute(sql, data)
                found_email = cur.fetchall()

                if found_email:
                    try:
                        columNames = [column[0] for column in cur.description]
                        record = [dict(zip(columNames, row)) for row in found_email]

                        for item in record:
                            idusuarios = item['idusuarios']

                        send_mail(email, idusuarios)
                        return jsonify({'message': 'Revise su bandeja de correo electrónico', 'idusuario': idusuarios}), 200
                    
                    except Exception as e:
                        return jsonify({'error': 'Error, servidor de correo no disponible'}), 400
                else:
                    return jsonify({'error':'El correo electrónico no existe'}), 400
        except Exception as e:
            return jsonify({'error': 'Error al buscar correo electrónico'}), 400
    return render_template('usuarios/forgot.html')



@usuario.route('/ajustes_usuario')
def ajustes_usuario():
    return render_template('usuarios/ajustes.html')



@usuario.route('/verificacion_dos_pasos/<int:idusuario>', methods = ['GET', 'POST'])
def verificacion_dos_pasos(idusuario):
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        db = current_app.config['db']
        db.ping(reconnect=True)

        try:
            with db.cursor() as cur:
                sql = 'SELECT * FROM codigos_verificacion WHERE codigo = %s AND idusuarios = %s AND (usado IS NULL OR usado = FALSE)'
                data = (codigo, idusuario)
                cur.execute(sql, data)
                record = cur.fetchone()

                if record:
                    cur.execute(
                        """ UPDATE codigos_verificacion 
                            SET usado = TRUE 
                            WHERE idusuarios = %s """,
                        (idusuario,)
                    )
                    db.commit()
                    return jsonify({'message': 'Codigo verificado exitosamente', 'user': idusuario}), 200
                else: 
                    return jsonify({'error': 'Codigo invalido'}), 400
        except Exception as e:
            return jsonify({'error': 'Error al validar codigo'}), 400
    
    return render_template('usuarios/2fv.html', user = idusuario)



@usuario.route('/recuperar_contraseña/<int:idusuario>', methods = ['GET', 'PATCH'])
def recuperar_contraseña(idusuario):
    if request.method == 'PATCH':
        db = current_app.config['db']
        db.ping(reconnect=True)

        contraseñaNueva = request.form.get('contraseñaNueva')
        
        if not contraseñaNueva:
            return jsonify({'error': 'Se deben llenar todos los campos'}), 400
        contraseña_hash = bcrypt.generate_password_hash(contraseñaNueva).decode('utf-8')

        try:
            with db.cursor() as cur:
                sql = 'UPDATE usuarios SET contraseña = %s WHERE idusuarios = %s'
                data = (contraseña_hash, idusuario)
                cur.execute(sql, data)
                db.commit()
                return jsonify({'message': 'contraseña actualizada satisfactoriamente', 'user': idusuario}), 200
        except Exception as e:
            db.rollback()
            return jsonify({'error': f'{e}'}), 500
    
    if request.method == 'GET':
        return render_template('usuarios/recuperar.html', user = idusuario)


@usuario.route('/get_profile_image/<int:idusuarios>')
def get_profile_image(idusuarios):
    db = current_app.config['db']

    with db.cursor() as cur:
        db.ping(reconnect=True)
        cur.execute('SELECT imagen FROM usuarios WHERE idusuarios = %s', (idusuarios,))
        image_data = cur.fetchone()[0]

        mime_type = 'image/jpeg'
        if image_data.startswith(b'\x89PNG'):
            mime_type = 'image/png'
        elif image_data.startswith(b'\xff\xd8'):
            mime_type = 'image/jpeg'
        
        return Response(image_data, mimetype=mime_type)



@usuario.route('/update_foto/<int:idusuarios>', methods = ['PATCH'])
def update_foto(idusuarios):
    imagen = request.files['imagen']
        
    imagen_blob = imagen.read()

    db = current_app.config['db']
    cur = db.cursor()

    try:
        cur.execute('UPDATE usuarios SET imagen = %s WHERE idusuarios = %s', (imagen_blob, idusuarios))
        db.commit()
        response = jsonify({
            'mensaje': 'imagen de perfil actualizada', 
            'usuario': f'{idusuarios}'
        })
        
        # LUEGO AGREGAR LOS HEADERS
        response.headers.extend({
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0',
            'X-Accel-Expires': '0'
        })
        
        return response, 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 500
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
        response = jsonify({
            'mensaje': 'email actualizado', 
            'usuario': f'{idusuarios}'
        })
        
        # LUEGO AGREGAR LOS HEADERS
        response.headers.extend({
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0',
            'X-Accel-Expires': '0'
        })
        
        return response, 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'{e}'}), 500
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
        response = jsonify({
            'mensaje': 'nombres actualizados', 
            'usuario': f'{idusuarios}'
        })
        
        # LUEGO AGREGAR LOS HEADERS
        response.headers.extend({
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0',
            'X-Accel-Expires': '0'
        })
        
        return response, 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'{e}'}), 500
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
        response = jsonify({
            'mensaje': 'apellidos actualizados', 
            'usuario': f'{idusuarios}'
        })
        
        # LUEGO AGREGAR LOS HEADERS
        response.headers.extend({
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0',
            'X-Accel-Expires': '0'
        })
        
        return response, 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'{e}'}), 500
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
        response = jsonify({
            'mensaje': 'cedula actualizada', 
            'usuario': f'{idusuarios}'
        })
        
        # LUEGO AGREGAR LOS HEADERS
        response.headers.extend({
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0',
            'X-Accel-Expires': '0'
        })
        
        return response, 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'{e}'}), 500
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
            response = jsonify({
            'mensaje': 'contraseña actualizada', 
            'usuario': f'{idusuarios}'
            })
        
            # LUEGO AGREGAR LOS HEADERS
            response.headers.extend({
                'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
                'Pragma': 'no-cache',
                'Expires': '0',
                'X-Accel-Expires': '0'
            })
            
            return response, 200
        else:
            return jsonify({'error': 'la contraseña actual es incorrecta'}), 400
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()



@usuario.route('/log_out', methods = ['POST'])
def log_out():
    try:
        logout_user()
        return jsonify({'mensaje': 'sesión cerrada'}), 200
    except Exception as e:
        print(e)
        return jsonify({'mensaje': 'Error al cerrar sesión'}), 400