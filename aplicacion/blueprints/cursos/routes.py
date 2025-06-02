from flask import request, render_template, redirect, url_for, Blueprint, current_app
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, generate_password_hash

cursos = Blueprint('cursos', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@cursos.route('/', methods = ['GET', 'POST'])
def index():
    db = current_app.config['db']

    with db.cursor() as cur:
        try:
            db.ping(reconnect=True)
            sql = 'SELECT c.idCurso, f.idFacultad, f.facultad, c.nombre_curso FROM cursos c JOIN facultades f ON c.idFacultad = f.idFacultad'
            cur.execute(sql)
            registros = cur.fetchall()
            insertCursos = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertCursos.append(dict(zip(columNames, record)))
            print(insertCursos)
            return render_template('cursos/index.html', cursos = insertCursos)
        except Exception as e:
            print(e)