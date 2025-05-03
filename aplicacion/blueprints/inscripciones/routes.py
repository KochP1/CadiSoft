from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, Response
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

inscripciones = Blueprint('inscripciones', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@inscripciones.route('/')
def index():
    return render_template('inscripciones/index.html')

@inscripciones.route('/alumnos_regulares')
def alumnos_regulares():
    return render_template('inscripciones/alumnosRegulares.html')

@inscripciones.route('/buscar_alumno', methods = ['POST'])
def buscar_alumno():
    cedula = request.form.get('cedula')

    if not cedula:
        return jsonify({'error': 'La cédula es requerida'}), 400

    try:
        db = current_app.config['db']
        db.ping(reconnect=True)  # Revisar y reconectar si es necesario
        
        with db.cursor() as cur:
            sql = 'SELECT a.idAlumno, a.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email FROM alumnos a JOIN usuarios u ON a.idusuarios = u.idusuarios WHERE u.cedula = %s'
            data = (cedula,)
            cur.execute(sql, data)
            alumno = cur.fetchone()

            if alumno:
                columNames = [column[0] for column in cur.description]
                alumno_dict = dict(zip(columNames, alumno))
                return jsonify({'alumno': alumno_dict}), 200
            else:
                return jsonify({'success': False, 'message': 'Alumno no encontrado'}), 404
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'error': 'Error interno al buscar alumno',
            'details': str(e)
        }), 500
