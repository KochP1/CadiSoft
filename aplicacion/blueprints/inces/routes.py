from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash, g
from flask_login import login_user, logout_user, current_user, login_required

inces = Blueprint('inces', __name__, template_folder='templates', static_folder='static')

# INSCRIPCIONES INCES

@inces.route('/')
@login_required
def index():
    return render_template('inces/index.html')

@inces.route('/cursos', methods = ['GET'])
@login_required
def cursos():
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM cursos WHERE inces = 1')
            result = cur.fetchall()
            columNames = [column[0] for column in cur.description]
            cursos = []
            for record in result:
                cursos.append(dict(zip(columNames, record)))
            return jsonify({'cursos': cursos}), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener cursos: {e}'}), 500

@inces.route('/empresas')
@login_required
def empresas():
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM empresas')
            result = cur.fetchall()
            columNames = [column[0] for column in cur.description]
            empresas = []
            for record in result:
                empresas.append(dict(zip(columNames, record)))
            return jsonify({'empresas': empresas}), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener empresas: {e}'}), 500
    
@inces.route('/secciones/<int:id>')
@login_required
def secciones(id):
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM secciones s INNER JOIN cursos c ON s.idCurso = c.idCurso WHERE s.idCurso = %s', (id))
            result = cur.fetchall()
            columNames = [column[0] for column in cur.description]
            secciones = []
            for record in result:
                secciones.append(dict(zip(columNames, record)))
            return jsonify({'secciones': secciones}), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener empresas: {e}'}), 500
    
# FINALIZAMOS INSCRIPCIONES INCES

# GESTION DE CURSOS

@inces.route('/gestion_cursos')
@login_required
def gestion_cursos():
    return render_template('inces/cursos.html')

@inces.route('/crear_curso', methods = ['GET', 'POST'])
@login_required
def crear_curso():
    if request.method == 'GET':
        return render_template('inces/crearCurso.html')
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            curso = data['curso']
            facultad = data['facultad']
            duracion = data['duracion']
            imagen = data['imagen']
            materias = data['materias']
            print(data)

            if not data or 'curso' not in data or 'materias' not in data or 'facultad' not in data or 'duracion' not in data:
                return jsonify({'error': 'Datos incompletos'}), 400
            
            if not isinstance(materias, list) or len(materias) == 0:
                return jsonify({'error': 'Formato de materias incorrectos'}), 400
            
            sql = 'INSERT INTO cursos (`idFacultad`, `nombre_curso`, `duracionCurso`, `imagen`, `inces`) VALUES (%s, %s, %s, %s, %s)'
            
            print(F'Curso: {curso}')
            print(f'Materias: {materias}')
            print(f'Facultad: {facultad}')

            with g.db.cursor() as cur:
                cur.execute(sql, (facultad, curso, duracion, imagen, 1))
                g.db.commit()

                cur.execute('SELECT idCurso FROM cursos WHERE nombre_curso = %s', (curso,))
                idCurso = cur.fetchone()

                for record in materias:
                    cur.execute('INSERT INTO materias (`idCurso`, `nombre`) VALUES (%s, %s)', (idCurso[0], record))
                    g.db.commit()
                return jsonify({'message': 'Curso creado'}), 201
        except Exception as e:
            g.db.rollback()
            print(e)
            return jsonify({'error': f'Error: {e}'}), 500

# FINALIZAMOS GESTION DE CURSOS