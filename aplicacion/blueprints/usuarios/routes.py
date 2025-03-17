from flask import request, render_template, redirect, url_for, Blueprint, current_app
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, generate_password_hash

usuario = Blueprint('usuario', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@usuario.route('/', methods = ['GET', 'POST'])
def index():
    db = current_app.config['db']
    try:
        cur = db.cursor()
        cur.execute('SELECT u.nombre, u.apellido FROM alumnos a JOIN usuarios u ON a.idusuarios = u.idusuarios')
        alumnos = cur.fetchall()
        insertalumnos = []
        columNamnes = [column[0] for column in cur.description]
        for record in alumnos:
            insertalumnos.append(dict(zip(columNamnes, record)))
    except Exception as e:
        print(e)
    finally:
        cur.close()

    return render_template('usuarios/index.html', alumnos = insertalumnos)