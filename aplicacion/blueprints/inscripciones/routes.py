from datetime import timedelta
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
        db.ping(reconnect=True)
        
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
    
@inscripciones.route('/buscar_curso', methods = ['POST'])
def buscar_curso():

    if not request.json:
        return jsonify({'error': 'La cédula es requerida'}), 400
    
    data = request.get_json()

    required_fields = ['curso']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400

    try:
        db = current_app.config['db']
        db.ping(reconnect=True)
        
        with db.cursor() as cur:
            sql = 'SELECT s.idSeccion, s.seccion, s.idCurso, c.idFacultad, c.nombre_curso, s.idProfesor FROM secciones s JOIN cursos c ON s.idCurso = c.idCurso WHERE c.nombre_curso = %s '
            data = (data['curso'],)
            cur.execute(sql, data)
            curso = cur.fetchall()

            if curso:
                columNames = [column[0] for column in cur.description]
                curso_dict = [dict(zip(columNames, row)) for row in curso]
                return jsonify({'cursos': curso_dict}), 200
            else:
                return jsonify({'success': False, 'message': 'Curso no encontrado'}), 404
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'error': 'Error interno al buscar curso',
            'details': str(e)
        }), 500

@inscripciones.route('mostar_horario', methods = ['POST'])
def mostrar_horario():
    if not request.json:
        return jsonify({'error': 'La cédula es requerida'}), 400
    
    data = request.get_json()

    required_fields = ['idSeccion']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400
    
    try:
        db = current_app.config['db']
        db.ping(reconnect=True)
        
        with db.cursor() as cur:
            sql = 'SELECT h.idhorario, h.horario_dia, h.horario_hora, h.horario_aula, s.idSeccion, c.nombre_curso FROM horario_x_curso hxc JOIN horario h ON hxc.idhorario = h.idhorario JOIN secciones s ON hxc.idSeccion = s.idSeccion JOIN cursos c ON s.idCurso = c.idCurso WHERE s.idSeccion = %s'
            data = (data['idSeccion'],)
            cur.execute(sql, data)
            seccion = cur.fetchall()

            if seccion:
                columNames = [column[0] for column in cur.description]
                seccion_dict = [dict(zip(columNames, row)) for row in seccion]
                
                for record in seccion_dict:
                    if isinstance(record.get('horario_hora'), timedelta):
                        # Convertir timedelta a string HH:MM:SS
                        total_seconds = record['horario_hora'].total_seconds()
                        hours = int(total_seconds // 3600)
                        minutes = int((total_seconds % 3600) // 60)
                        seconds = int(total_seconds % 60)
                        record['horario_hora'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                print(seccion_dict)
                return jsonify({'horarioSeccion': seccion_dict}), 200
            else:
                return jsonify({'success': False, 'message': 'horario de seccion no encontrado'}), 404
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'error': 'Error interno al buscar el horario',
            'details': str(e)
        }), 500