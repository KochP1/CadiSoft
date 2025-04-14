from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

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
            return render_template('usuarios/index.html', message = 'El usuario fue creado satisfactoriamente')
        except Exception as e:
            print(f'Error: {e}')
            return redirect(url_for('usuario.regist_user'))
        finally:
            cur.close()

@usuario.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    return render_template('usuarios/forgot.html')

@usuario.route('/log_out', methods = ['POST'])
def log_out():
    usuarioid = current_user.id
    logout_user()
    return jsonify({'mensaje': 'sesión cerrada', 'usuario': usuarioid}), 200