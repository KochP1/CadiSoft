from os import getenv
from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, Response, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
import random, datetime as dt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

import pymysql
from . model import User

load_dotenv()

usuario = Blueprint('usuario', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@usuario.route('/', methods=['GET', 'POST'])
def index():
    # Si ya está autenticado, redirigir
    if current_user.is_authenticated:
        if current_user.rol == 'administrador' or current_user.rol == 'profesor':
            return redirect(url_for('usuario.inicio'))
        elif current_user.rol == 'alumno':
            return redirect(url_for('alumnos.dashboard'))
    
    if request.method == 'POST':
        cedula = request.form['cedula']
        contraseña = request.form['contraseña']
        
        user = User.get_by_cedula(g.db, cedula)
        
        if user and bcrypt.check_password_hash(user.contraseña, contraseña):
            
            login_user(user, remember=True)
            
            #print(f"Después de login_user - Autenticado: {current_user.is_authenticated}")
            
            if user.rol == 'administrador' or current_user.rol == 'profesor':
                return redirect(url_for('usuario.inicio'))
            elif current_user.rol == 'alumno':
                return redirect(url_for('alumnos.dashboard'))
            else:
                return render_template('usuarios/index.html', message_error='Permisos insuficientes')
        else:
            return render_template('usuarios/index.html', message_error='Credenciales incorrectas')
    
    return render_template('usuarios/index.html')



@usuario.route('/inicio')
@login_required
def inicio():
    try:
        return render_template('usuarios/inicio.html')
    except Exception as e:
        print(e)
        return 'Error'



@usuario.route('/inicio_stats')
@login_required
def inicio_stats():
    try:
        with g.db.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute('SELECT COUNT(*) AS total FROM usuarios WHERE rol = %s', ('alumno',))
            alumnos = cur.fetchone()

            cur.execute('SELECT COUNT(*) AS total FROM profesores')
            profesores = cur.fetchone()


            cur.execute('SELECT COUNT(*) AS total FROM cursos')
            cursos = cur.fetchone()

            cur.execute('SELECT COUNT(*) AS total FROM facultades')
            facultades = cur.fetchone()

            sql = """
                SELECT MONTH(fecha_inscripcion) as mes, COUNT(*) as total 
                FROM inscripcion 
                WHERE YEAR(fecha_inscripcion) = YEAR(CURDATE()) 
                GROUP BY MONTH(fecha_inscripcion) 
                ORDER BY mes
            """
            cur.execute(sql)
            results = cur.fetchall()

            meses_completos = [0] * 12
            nombres_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            
            for resultado in results:
                mes = resultado['mes'] - 1 
                total = resultado['total']
                meses_completos[mes] = total

            return jsonify({
                'mensaje': 'Request exitoso', 
                'alumnos': alumnos['total'], 
                'profesores': profesores['total'], 
                'cursos': cursos['total'], 
                'facultades': facultades['total'],
                'meses': nombres_meses,
                'inscripciones': meses_completos
            }), 200

    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'Request fallido: {str(e)}'}), 500

@usuario.route('/regist_user', methods = ['GET', 'POST'])
def regist_user():
    if request.method == 'GET':
        return render_template('usuarios/regist.html')
    
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            segundoNombre = request.form.get('segundoNombre')
            apellido = request.form.get('apellido')
            segundoApellido = request.form.get('segundoApellido')
            cedula = request.form.get('cedula')
            email = request.form.get('email')
            contraseña = request.form.get('contraseña')
            contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

            with g.db.cursor() as cur:
                cur.execute('INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`) VALUES (%s, %s, %s, %s, %s, %s, %s)', (nombre, segundoNombre, apellido, segundoApellido, cedula, email, contraseña_hash))
                g.db.commit()
                return jsonify({'message': 'Usuario creado satisfactoriamente'}), 200
        except Exception as e:
            print(e)
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'Error al registrar usuario: {e}'}), 500
        finally:
            cur.close()



def generar_codigo_verificacion(usuario_id):

    codigo = str(random.randint(100000, 999999))
    
    expiracion = dt.datetime.now() + dt.timedelta(minutes=15)
    
    try:
        with g.db.cursor() as cur:
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
            g.db.commit()
            
            return codigo
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        current_app.logger.error(f"Error al guardar código: {str(e)}")
        raise


def send_mail(email, id):
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
            <img src="https://cadisoft-production.up.railway.app/images/Cadi_logo-removeBG.png" alt="Logo cadiSoft" width="150">
            </div>
        </body>
        </html>
        """
    
    sendgrid_api_key = getenv('SENDGRID_API_KEY')
    from_email = getenv('FROM_EMAIL')

    message = Mail(
        from_email=from_email,
        to_emails=email,
        subject='Recuperación de cuenta cadisoft',
        html_content=html_body
    )
    
    if not sendgrid_api_key:
        current_app.logger.error("SENDGRID_API_KEY no encontrada en configuración")
        return False
    
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        # sg.set_sendgrid_data_residency("eu")
        # uncomment the above line if you are sending mail using a regional EU subuser
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        print(e.message)
        return False



@usuario.route('/ajustes_usuario')
@login_required
def ajustes_usuario():
    return render_template('usuarios/ajustes.html')



@usuario.route('/verificacion_dos_pasos/<int:idusuario>', methods = ['GET', 'POST'])
def verificacion_dos_pasos(idusuario):
    if request.method == 'POST':
        codigo = request.form.get('codigo')

        try:
            with g.db.cursor() as cur:
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
                    g.db.commit()
                    return jsonify({'message': 'Codigo verificado exitosamente', 'user': idusuario}), 200
                else: 
                    return jsonify({'error': 'Codigo invalido'}), 400
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': 'Error al validar codigo'}), 400
    
    return render_template('usuarios/2fv.html', user = idusuario)



@usuario.route('/recuperar_contraseña/<int:idusuario>', methods = ['GET', 'PATCH'])
def recuperar_contraseña(idusuario):
    if request.method == 'PATCH':

        contraseñaNueva = request.form.get('contraseñaNueva')
        
        if not contraseñaNueva:
            return jsonify({'error': 'Se deben llenar todos los campos'}), 400
        contraseña_hash = bcrypt.generate_password_hash(contraseñaNueva).decode('utf-8')

        try:
            with g.db.cursor() as cur:
                sql = 'UPDATE usuarios SET contraseña = %s WHERE idusuarios = %s'
                data = (contraseña_hash, idusuario)
                cur.execute(sql, data)
                g.db.commit()
                return jsonify({'message': 'contraseña actualizada satisfactoriamente', 'user': idusuario}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'{e}'}), 500
    
    if request.method == 'GET':
        return render_template('usuarios/recuperar.html', user = idusuario)


@usuario.route('/get_profile_image/<int:idusuarios>')
@login_required
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
@login_required
def update_foto(idusuarios):
    imagen = request.files['imagen']
        
    imagen_blob = imagen.read()

    try:
        with g.db.cursor () as cur:
            cur.execute('UPDATE usuarios SET imagen = %s WHERE idusuarios = %s', (imagen_blob, idusuarios))
            g.db.commit()
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
        if hasattr(g, 'db'):
            g.db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 500



@usuario.route('/update_email/<int:idusuarios>', methods = ['PATCH'])
@login_required
def update_email(idusuarios):
    with g.db.cursor() as cur:
        if not request.is_json:
            return jsonify({"error": "El cuerpo debe ser JSON"}), 400
                
        data = request.get_json()

        required_fields = ['email']

        if not all(field in data for field in required_fields):
            return jsonify({"error": "faltan campos"}), 400
        
        try:
            cur.execute('UPDATE usuarios SET email = %s WHERE idusuarios = %s', (data['email'], idusuarios))
            g.db.commit()
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
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'{e}'}), 500



@usuario.route('/edit_nombres/<int:idusuarios>', methods = ['PATCH'])
@login_required
def edit_nombres(idusuarios):
    with g.db.cursor() as cur:

        if not request.is_json:
            return jsonify({"error": "El cuerpo debe ser JSON"}), 400
                
        data = request.get_json()

        required_fields = ['nombre', 'segundoNombre']

        if not all(field in data for field in required_fields):
            return jsonify({"error": "faltan campos"}), 400
        
        try:
            cur.execute('UPDATE usuarios SET nombre = %s, segundoNombre = %s WHERE idusuarios = %s', (data['nombre'], data['segundoNombre'], idusuarios))
            g.db.commit()
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
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'{e}'}), 500

@usuario.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        g.db.ping(reconnect=True)
        email = request.form.get('email')

        try:
            with g.db.cursor() as cur:
                sql = 'SELECT idusuarios, email FROM usuarios WHERE email = %s'
                data = (email,)
                cur.execute(sql, data)
                found_email = cur.fetchall()

                if not found_email:
                    return jsonify({'error':'El correo electrónico no existe'}), 400

                try:
                    columNames = [column[0] for column in cur.description]
                    record = [dict(zip(columNames, row)) for row in found_email]

                    for item in record:
                        idusuarios = item['idusuarios']

                    sendMail = send_mail(email, idusuarios)
                    if not sendMail:
                        return jsonify({'message': 'Error al enviar correo electrónico'}), 400

                    return jsonify({'message': 'Revise su bandeja de correo electrónico', 'idusuario': idusuarios}), 200

                except Exception as e:
                    print(e)
                    return jsonify({'error': 'Error, servidor de correo no disponible'}), 500
        except Exception as e:
            print(e)
            return jsonify({'error': 'Error al buscar correo electrónico'}), 400
    return render_template('usuarios/forgot.html')


@usuario.route('/edit_apellidos/<int:idusuarios>', methods = ['PATCH'])
@login_required
def edit_apellidos(idusuarios):
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    data = request.get_json()

    required_fields = ['apellido', 'segundoApellido']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400

    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE usuarios SET apellido = %s, segundoApellido = %s WHERE idusuarios = %s', (data['apellido'], data['segundoApellido'], idusuarios))
            g.db.commit()
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
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'{e}'}), 500


@usuario.route('/edit_cedula/<int:idusuarios>', methods = ['PATCH'])
@login_required
def edit_cedula(idusuarios):
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON"}), 400

    data = request.get_json()

    required_fields = ['cedula']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400

    try:
        with g.db.cursor() as cur:
            cur.execute('UPDATE usuarios SET cedula = %s WHERE idusuarios = %s', (data['cedula'], idusuarios))
            g.db.commit()
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
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'{e}'}), 500


@usuario.route('/edit_contraseña/<int:idusuarios>', methods = ['PATCH'])
@login_required
def edit_contraseña(idusuarios):
    if not request.json:
        return jsonify({'error': 'el cuerpo debe ser JSON'}), 400

    data = request.get_json()

    required_fields = ['contraseñaActual', 'contraseñaNueva']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'faltan campos'}), 400

    try:
        if bcrypt.check_password_hash(current_user.contraseña, data['contraseñaActual']):
            contraseñaNueva = bcrypt.generate_password_hash(data['contraseñaNueva']).decode('utf-8')
            with g.db.cursor() as cur:
                cur.execute('UPDATE usuarios SET contraseña = %s WHERE idusuarios = %s', (contraseñaNueva, idusuarios))
                g.db.commit()
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
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'{e}'}), 400

from flask import send_file, abort
from werkzeug.utils import safe_join
import os
@usuario.route('/descargar-pdf/<nombre_archivo>')
@login_required
def descargar_pdf(nombre_archivo):
    try:
        carpeta_pdfs = os.path.join(current_app.root_path, 'static', 'util')
        ruta_archivo = safe_join(carpeta_pdfs, nombre_archivo)
        
        if not os.path.exists(ruta_archivo):
            abort(404, description="Archivo no encontrado")
        
        if not nombre_archivo.lower().endswith('.pdf'):
            abort(400, description="Solo se permiten archivos PDF")
        
        return send_file(
            ruta_archivo,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error descargando PDF: {e}")
        abort(500, description="Error al descargar el archivo")

@usuario.route('/log_out', methods = ['POST'])
@login_required
def log_out():
    try:
        logout_user()
        return jsonify({'mensaje': 'sesión cerrada'}), 200
    except Exception as e:
        print(e)
        return jsonify({'mensaje': 'Error al cerrar sesión'}), 400