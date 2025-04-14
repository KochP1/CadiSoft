from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

profesores = Blueprint('profesores', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@profesores.route('/', methods = ['GET', 'POST'])
def index():
    db = current_app.config['db']
    cur = db.cursor()
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "El cuerpo debe ser JSON"}), 400
            
        data = request.get_json()

        required_fields = ['']

        if not all(field in data for field in required_fields):
            return jsonify({'error', 'faltan campos'}), 400
        
        try:
            pass

        except Exception as e:
            print(e)
            return redirect(url_for('profesores.index'))
        finally:
            cur.close()
    try:
        sql = 'SELECT p.idProfesor, p.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, e.especialidad FROM profesores p JOIN usuarios u ON p.idusuarios = u.idusuarios JOIN especialidad e ON p.idespecialidad = e.idespecialidad'
        cur.execute(sql)
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        print(InsertRegistros)
        return render_template('profesores/index.html', profesores = InsertRegistros)
    except Exception as e:
        print(e)
        return render_template('profesores/index.html')
    finally:
        cur.close()