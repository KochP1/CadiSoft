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
                return render_template('usuarios/index.html', message_error = 'Credenciales incorrectas'), jsonify({'error': True, 'mensaje': 'No tienes autorización para ingresar al sistema'}), 401
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
        nombre = request.form['nombre']
        segundoNombre = request.form['segundoNombre']
        apellido = request.form['apellido']
        segundoApellido = request.form['segundoApellido']
        cedula = request.form['cedula']
        email = request.form['email']
        contraseña = request.form['contraseña']
        rol = 'administrador'
        contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        if len(nombre) > 12:
            return render_template('usuarios/regist.html', message = 'El nombre es muy largo (max 12 caracteres)')
        if len(segundoNombre) > 12:
            return render_template('usuarios/regist.html', message = 'El segundo nombre es muy largo (max 12 caracteres)')
        if len(apellido) > 20:
            return render_template('usuarios/regist.html', message = 'El apellido es muy largo (max 20 caracteres)')
        if len(segundoApellido) > 20:
            return render_template('usuarios/regist.html', message = 'El segundo apellido es muy largo (max 20 caracteres)')
        if len(cedula) > 11:
            return render_template('usuarios/regist.html', message = 'La cédula es muy larga (max 11 numeros enteros)')
        if len(email) > 12:
            return render_template('usuarios/regist.html', message = 'El email es muy largo (max 50 caracteres)')
        if len(contraseña) > 8:
            return render_template('usuarios/regist.html', message = 'La contraseña es muy larga (max 8 caracteres)')
        try:
            db = current_app.config['db']
            cur = db.cursor()
            sql = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            data = (nombre, segundoNombre, apellido, segundoApellido, cedula, email, contraseña_hash, rol)
            cur.execute(sql, data)
            db.commit()
            return render_template('usuarios/index.html', message = 'El usuario fue creado satisfactoriamente'), jsonify({'exito': True, 'mensaje': 'Usuario creado'}), 200
        except Exception as e:
            print(f'Error: {e}')
            return redirect(url_for('usuario.regist_user')), jsonify({"error": True, "mensaje": "El usuario no se puedo eliminar."}), 404
        finally:
            cur.close()

@usuario.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    return render_template('usuarios/forgot.html')

@usuario.route('/log_out')
def log_out():
    usuarioid = current_user.id
    logout_user()
    return redirect(url_for('usuario.index'))