from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash, g
from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd
import io

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
            return render_template('inces/empresas.html', empresas = empresas)
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
    try:
        with g.db.cursor() as cur:
            cur.execute('''
                SELECT c.idCurso, f.idFacultad, f.facultad, c.nombre_curso, c.duracionCurso, m.nombre as materia_nombre 
                FROM cursos c 
                INNER JOIN materias m ON c.idCurso = m.idCurso 
                INNER JOIN facultades f ON c.idFacultad = f.idFacultad
                ORDER BY c.nombre_curso, m.nombre
            ''')
            resultados = cur.fetchall()
            
            cursos_dict = {}
            for row in resultados:
                # Acceder por índice
                id_curso = row[0]
                idFacultad = row[1] 
                facultad = row[2] 
                nombre_curso = row[3]
                duracionCurso = row[4] 
                
                # Si es la primera vez que encontramos este curso, inicializarlo
                if id_curso not in cursos_dict:
                    cursos_dict[id_curso] = {
                        'idCurso': id_curso,
                        'idFacultad': idFacultad,
                        'facultad': facultad,
                        'nombre_curso': nombre_curso,
                        'duracionCurso': duracionCurso,
                        'materias': []
                    }
                
                materia_nombre = row[-1]  # Última columna del SELECT
                if materia_nombre:
                    cursos_dict[id_curso]['materias'].append(materia_nombre)
            
            # Convertir el diccionario a lista
            cursos_array = list(cursos_dict.values())
            
            return render_template('inces/cursos.html', cursos = cursos_array)
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error: {e}'}), 500
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

                cur.execute('SELECT idCurso FROM cursos WHERE nombre_curso = %s AND inces = 1', (curso,))
                idCurso = cur.fetchone()

                for record in materias:
                    cur.execute('INSERT INTO materias (`idCurso`, `nombre`) VALUES (%s, %s)', (idCurso[0], record))
                    g.db.commit()
                return jsonify({'message': 'Curso creado'}), 201
        except Exception as e:
            g.db.rollback()
            print(e)
            return jsonify({'error': f'Error: {e}'}), 500
        

@inces.route('/carga_masiva', methods = ['POST'])
def carga_masiva():
    try:
        if 'excel' not in request.files:
            return jsonify({'error': 'No se encontró el archivo'}), 400
        
        archivo = request.files['excel']
        
        if archivo.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        # Leer el archivo SIN header para evitar que la primera fila sea considerada como nombres de columnas
        if archivo.filename.lower().endswith('.csv'):
            df = pd.read_csv(archivo, header=None)
        else:
            df = pd.read_excel(archivo, header=None)
        
        # Obtener TODOS los valores de la columna A (primera columna)
        columna_a = []
        if not df.empty:
            # Seleccionar la primera columna sin eliminar NaN
            columna_a = df.iloc[:, 0].fillna('').astype(str).tolist()
        
        print("Valores de la columna A:", columna_a)
        print("Número de elementos:", len(columna_a))
        
        return jsonify({
            'message': 'Archivo procesado correctamente', 
            'columna_a': columna_a
        }), 200
        
    except Exception as e:
        print(f"Error procesando el archivo: {str(e)}")
        return jsonify({'error': f'Error procesando el archivo: {str(e)}'}), 500

# FINALIZAMOS GESTION DE CURSOS