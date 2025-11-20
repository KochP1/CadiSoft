from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, g
from flask_login import current_user, login_required
import pandas as pd
import io

from aplicacion.blueprints.cursos.routes import dateToString
from aplicacion.blueprints.shared.reporte_inscripciones import reporte_inscripciones

inces = Blueprint('inces', __name__, template_folder='templates', static_folder='static')

# INSCRIPCIONES INCES

@inces.route('/secciones_filtrado')
def secciones_filtrado():
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT s.idSeccion, s.seccion, c.nombre_curso AS curso FROM secciones s JOIN cursos c ON s.idCurso = c.idCurso')
            result = cur.fetchall()
            columNames = [column[0] for column in cur.description]
            secciones = []

            for record in result:
                secciones.append(dict(zip(columNames, record)))
            
            return jsonify({'secciones': secciones}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error: {e}'}), 500

@inces.route('/gestion_insc', methods = ['GET', 'POST'])
def gestion_insc():
    try:
        if request.method == 'POST':
            p_cedula = request.form.get('cedula')
            p_fecha_inscripcion = request.form.get('inicio')
            p_idSeccion = request.form.get('seccion')
            p_fecha_expiracion = request.form.get('fin')
            p_es_activa = request.form.get('status')  # Puede ser '1', '0' o None

            # Limpiar valores vacíos
            p_cedula = p_cedula if p_cedula else None
            p_fecha_inscripcion = p_fecha_inscripcion if p_fecha_inscripcion else None
            p_fecha_expiracion = p_fecha_expiracion if p_fecha_expiracion else None
            p_idSeccion = int(p_idSeccion) if p_idSeccion else None
            p_es_activa = int(p_es_activa) if p_es_activa else None
            
            with g.db.cursor() as cur:
                cur.callproc('reporte_inscripciones_sp', [p_cedula, p_fecha_inscripcion, p_idSeccion, p_fecha_expiracion, 'Inces', p_es_activa])

                result = cur.fetchall()
                columNames = [column[0] for column in cur.description]
                
                # Agrupar inscripciones
                inscripciones_dict = {}
                
                for record in result:
                    record_dict = dict(zip(columNames, record))
                    
                    key = f"{record_dict['idusuarios']}_{record_dict['fecha_inscripcion']}_{record_dict['fecha_expiracion']}"
                    
                    if key not in inscripciones_dict:
                        inscripciones_dict[key] = {
                            'idInscripcion': record_dict['idInscripcion'],
                            'idusuarios': record_dict['idusuarios'],
                            'nombre': record_dict['nombre'],
                            'apellido': record_dict['apellido'],
                            'cedula': record_dict['cedula'],
                            'fecha_inscripcion': record_dict['fecha_inscripcion'],
                            'fecha_expiracion': record_dict['fecha_expiracion'],
                            'tipo': record_dict['tipo'],
                            'status': record_dict['status'],
                            'imagen': record_dict['imagen'],
                            'secciones': []  # Array para múltiples secciones
                        }
                
                    # Agregar la sección actual al array
                    inscripciones_dict[key]['secciones'].append({
                        'curso': record_dict['curso'],
                        'seccion': record_dict['seccion']
                    })
            
                # Convertir a lista para el template
                inscripciones = list(inscripciones_dict.values())

                for record in inscripciones:
                    record['fecha_inscripcion'] = dateToString(record['fecha_inscripcion'])
                    record['fecha_expiracion'] = dateToString(record['fecha_expiracion'])
                
            return render_template('inces/inscripciones.html', inscripciones=inscripciones, cedula = p_cedula, fecha_inscripcion = p_fecha_inscripcion, fecha_expiracion = p_fecha_expiracion, idSeccion = p_idSeccion, status = p_es_activa)

        with g.db.cursor() as cur:
            cur.callproc('reporte_inscripciones_sp', [None, None, None, None, 'Inces', None])
            result = cur.fetchall()
            columNames = [column[0] for column in cur.description]
            
            # Agrupar inscripciones
            inscripciones_dict = {}
            
            for record in result:
                record_dict = dict(zip(columNames, record))
                
                key = f"{record_dict['idusuarios']}_{record_dict['fecha_inscripcion']}_{record_dict['fecha_expiracion']}"
                
                if key not in inscripciones_dict:
                    inscripciones_dict[key] = {
                        'idInscripcion': record_dict['idInscripcion'],
                        'idusuarios': record_dict['idusuarios'],
                        'nombre': record_dict['nombre'],
                        'apellido': record_dict['apellido'],
                        'cedula': record_dict['cedula'],
                        'fecha_inscripcion': record_dict['fecha_inscripcion'],
                        'fecha_expiracion': record_dict['fecha_expiracion'],
                        'tipo': record_dict['tipo'],
                        'status': record_dict['status'],
                        'imagen': record_dict['imagen'],
                        'secciones': []  # Array para múltiples secciones
                    }
                
                # Agregar la sección actual al array
                inscripciones_dict[key]['secciones'].append({
                    'curso': record_dict['curso'],
                    'seccion': record_dict['seccion']
                })
            
            # Convertir a lista para el template
            inscripciones = list(inscripciones_dict.values())

            for record in inscripciones:
                record['fecha_inscripcion'] = dateToString(record['fecha_inscripcion'])
                record['fecha_expiracion'] = dateToString(record['fecha_expiracion'])
            
        return render_template('inces/inscripciones.html', inscripciones=inscripciones)
    
    except Exception as e:
        print(e)
        return f'{e}'

@inces.route('/reporte_insc', methods = ['GET'])
def reporte_insc():
    try:
        p_cedula = request.args.get('cedula', type=str)
        p_fecha_inscripcion = request.args.get('fecha_inscripcion', type=str)
        p_idSeccion = request.args.get('idSeccion', type=int)
        p_fecha_expiracion = request.args.get('fecha_expiracion', type=str)
        p_es_activa = request.args.get('status', type=int)

        # Convertir a None si están vacíos o son 'None'
        p_cedula = None if p_cedula in [None, 'None', ''] else p_cedula
        p_fecha_inscripcion = None if p_fecha_inscripcion in [None, 'None', ''] else p_fecha_inscripcion
        p_idSeccion = None if p_idSeccion in [None, 0] else p_idSeccion
        p_fecha_expiracion = None if p_fecha_expiracion in [None, 'None', ''] else p_fecha_expiracion
        p_es_activa = None if p_es_activa in [None] else p_es_activa

        response = reporte_inscripciones(g.db, 'Inces', p_cedula, p_fecha_inscripcion, p_idSeccion, p_fecha_expiracion, p_es_activa)
        return response
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error: {e}'}), 500

@inces.route('/mod_status/<int:id>', methods = ['PATCH'])
def mod_status(id):
    try:
        data = request.get_json()
        status = data['status']

        if not data or 'status' not in data or not id:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        with g.db.cursor() as cur:
            cur.execute('UPDATE inscripcion SET es_activa = %s WHERE idInscripcion = %s', (status, id))
            g.db.commit()
            return jsonify({'message': 'Status de inscripcion actualizado'}), 200
    except Exception as e:
        return jsonify({'error': f'{e}'}), 500

@inces.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        try:
            data = request.get_json()
            idAlumno = data['alumno']
            idEmpresa = data['empresa']
            inicio = data['inicio']
            final = data['final']
            idSeccion = data['seccion']
            tipo = 'Inces'

            if not data or 'alumno' not in data or 'empresa' not in data or 'inicio' not in data or 'final' not in data or 'seccion' not in data:
                return jsonify({'error': 'Faltan campos'}), 400
            
            with g.db.cursor() as cur:
                cur.callproc('inscripcion_inces_sp', [idAlumno, inicio, idSeccion, final, tipo, idEmpresa])
                g.db.commit()
                return jsonify({'message': 'Alumno inscrito'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': f'Error al crear empresas: {e}'})
    return render_template('inces/index.html')
    
# FINALIZAMOS INSCRIPCIONES INCES

# GESTION DE CURSOS

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
                WHERE c.inces = 1
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

            if not data or 'curso' not in data or 'materias' not in data or 'facultad' not in data or 'duracion' not in data:
                return jsonify({'error': 'Datos incompletos'}), 400
            
            if not isinstance(materias, list) or len(materias) == 0:
                return jsonify({'error': 'Formato de materias incorrectos'}), 400
            
            sql = 'INSERT INTO cursos (`idFacultad`, `nombre_curso`, `duracionCurso`, `imagen`, `inces`) VALUES (%s, %s, %s, %s, %s)'

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
        
@inces.route('/materias/<int:id>')
def materias(id):
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM materias WHERE idCurso = %s', (id,))
            result = cur.fetchall()
            materias = []

            for record in result:
                materias.append(record[2])
            print(materias)

            return jsonify({'materias': materias}), 200
    except Exception as e:
        return jsonify({'error': f'Error: {e}'}), 500
        

@inces.route('/carga_masiva', methods = ['POST'])
@login_required
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
        return jsonify({'error': f'Error procesando el archivo: {str(e)}'}), 500

    
@inces.route('/carga_masiva_materias', methods=['POST'])
@login_required
def carga_masiva_materias():
    try:
        if 'excel' not in request.files:
            return jsonify({'error': 'No se encontró el archivo'}), 400
        
        archivo = request.files['excel']
        
        if archivo.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        if not archivo.filename.lower().endswith(('.xlsx', '.xls', '.csv')):
            return jsonify({'error': 'El archivo debe ser Excel (.xlsx, .xls) o CSV'}), 400
        
        # Leer el archivo
        if archivo.filename.lower().endswith('.csv'):
            df = pd.read_csv(archivo, header=None)
        else:
            df = pd.read_excel(archivo, header=None)
        
        materias_array = []
        errores = []
        
        for index, row in df.iterrows():
            # Saltar filas completamente vacías
            if row.isna().all():
                continue
                
            if len(row) >= 3:
                materia = str(row[0]).strip() if pd.notna(row[0]) else ""
                fecha_inicio = str(row[1]).strip() if pd.notna(row[1]) else ""
                fecha_final = str(row[2]).strip() if pd.notna(row[2]) else ""
                
                # Validaciones
                if not materia:
                    errores.append(f"Fila {index + 1}: Materia vacía")
                    continue
                
                # Validar formato de fechas (opcional)
                if fecha_inicio and not es_fecha_valida(fecha_inicio):
                    errores.append(f"Fila {index + 1}: Formato de fecha inicio inválido: {fecha_inicio}")
                
                if fecha_final and not es_fecha_valida(fecha_final):
                    errores.append(f"Fila {index + 1}: Formato de fecha final inválido: {fecha_final}")
                
                materia_obj = {
                    'materia': materia,
                    'inicio': fecha_inicio,
                    'final': fecha_final,
                    'fila': index + 1
                }
                materias_array.append(materia_obj)
            else:
                errores.append(f"Fila {index + 1}: No tiene suficientes columnas (se esperaban 3)")
        
        print(f"Procesadas {len(materias_array)} materias correctamente")
        if errores:
            print(f"Errores encontrados: {len(errores)}")
            for error in errores:
                print(f"  - {error}")
        
        return jsonify({
            'message': 'Archivo procesado correctamente', 
            'materias': materias_array,
            'total_materias': len(materias_array),
            'errores': errores,
            'total_errores': len(errores)
        }), 200
        
    except Exception as e:
        print(f"Error procesando el archivo: {str(e)}")
        return jsonify({'error': f'Error procesando el archivo: {str(e)}'}), 500

# Función auxiliar para validar fechas (opcional)
def es_fecha_valida(fecha_str):
    """Valida si un string tiene formato de fecha básico"""
    try:
        # Intentar parsear como fecha
        from datetime import datetime
        # Intentar varios formatos comunes
        formatos = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d']
        for formato in formatos:
            try:
                datetime.strptime(fecha_str, formato)
                return True
            except ValueError:
                continue
        return False
    except:
        return False
    
@inces.route('/crear_seccion/<int:id>', methods = ['POST'])
def crear_seccion(id):
    try:
        data = request.get_json()
        seccion = data['seccion']
        profesor = data['profesor']
        aula = data['aula']
        materias = data['materias']

        if not data or 'seccion' not in data or 'profesor' not in data or 'aula' not in data or 'materias' not in data or len(materias) <= 0:
            return jsonify({'error': 'Faltan campos'}), 400

        with g.db.cursor() as cur:
            cur.execute('INSERT INTO secciones (`idCurso`, `idProfesor`, `seccion`, `aula`) VALUES (%s, %s, %s, %s)', (id, profesor, seccion, aula))
            g.db.commit()

            cur.execute('SELECT idSeccion FROM secciones WHERE seccion = %s', (seccion,))
            res = cur.fetchone()
            idSeccion = res[0]

            for record in materias:
                inicio_mysql = convertir_fecha_mysql(record['inicio'])
                final_mysql = convertir_fecha_mysql(record['final'])
                
                if inicio_mysql and final_mysql:
                    cur.execute('INSERT INTO periodo_materias (`idSeccion`, `materia`, `inicio`, `fin`) VALUES (%s, %s, %s, %s)', 
                            (idSeccion, record['materia'], inicio_mysql, final_mysql))
                    g.db.commit()

            return jsonify({'message': 'Sección creada satisfactoriamente'}), 200

    except Exception as e:
        g.db.rollback()
        return jsonify({'error': f'Error: {e}'}), 500
    
from datetime import datetime

def convertir_fecha_mysql(fecha_str):
    """Convierte formato YYYY/DD/MM a YYYY-MM-DD para MySQL"""
    if not fecha_str:
        return None
    
    try:
        # Para formato: 2025/31/10 → 2025-10-31
        fecha_dt = datetime.strptime(fecha_str, '%Y/%d/%m')
        return fecha_dt.strftime('%Y-%m-%d')
    except ValueError:
        # Si falla, intentar otros formatos
        try:
            fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha_str
        except ValueError:
            try:
                fecha_dt = datetime.strptime(fecha_str, '%d/%m/%Y')
                return fecha_dt.strftime('%Y-%m-%d')
            except ValueError:
                print(f"Formato de fecha no reconocido: {fecha_str}")
                return None
            
@inces.route('/materias_by_id/<int:id>')
def materias_by_id(id):
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT idSeccion, materia, inicio, fin AS final FROM periodo_materias WHERE idSeccion = %s', (id))
            res = cur.fetchall()
            materias = []
            columNamesMaterias = [column[0] for column in cur.description]
            for record in res:
                materias.append(dict(zip(columNamesMaterias, record)))
            print(materias)
            return jsonify({'materias': materias}), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener materias: {e}'}), 500

@inces.route('/edit_seccion_inces/<int:id>', methods = ['PUT'])
def edit_seccion_inces(id):
    try:
        data = request.get_json()
        materias = data['materias']

        if not data or 'materias' not in data or len(materias) <= 0:
            return jsonify({'error': 'Faltan campos'}), 400

        with g.db.cursor() as cur:

            cur.execute('DELETE FROM periodo_materias WHERE idSeccion = %s', (id,))

            for record in materias:
                inicio_mysql = convertir_fecha_mysql(record['inicio'])
                final_mysql = convertir_fecha_mysql(record['final'])
                
                if inicio_mysql and final_mysql:
                    cur.execute('INSERT INTO periodo_materias (`idSeccion`, `materia`, `inicio`, `fin`) VALUES (%s, %s, %s, %s)', 
                            (id, record['materia'], inicio_mysql, final_mysql))
            g.db.commit()

            return jsonify({'message': 'Sección creada satisfactoriamente'}), 200

    except Exception as e:
        print(e)
        g.db.rollback()
        return jsonify({'error': f'Error: {e}'}), 500
    
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

# FINALIZAMOS GESTION DE CURSOS

# GESTIÓN DE EMPRESAS

@inces.route('/json_empresas')
@login_required
def json_empresas():
    with g.db.cursor() as cur:
        if request.method == 'GET':
            try:
                    cur.execute('SELECT * FROM empresas')
                    result = cur.fetchall()
                    columNames = [column[0] for column in cur.description]
                    empresas = []
                    for record in result:
                        empresas.append(dict(zip(columNames, record)))
                    return jsonify({'empresas': empresas}), 200
            except Exception as e:
                return jsonify({'error': f'Error al obtener empresas: {e}'}), 500

@inces.route('/empresas', methods = ['GET', 'POST'])
@login_required
def empresas():
    with g.db.cursor() as cur:
        if request.method == 'GET':
            try:
                    cur.execute('SELECT * FROM empresas')
                    result = cur.fetchall()
                    columNames = [column[0] for column in cur.description]
                    empresas = []
                    for record in result:
                        empresas.append(dict(zip(columNames, record)))
                    return render_template('inces/empresas.html', empresas = empresas)
            except Exception as e:
                return jsonify({'error': f'Error al obtener empresas: {e}'}), 500
        elif request.method == 'POST':
            try:
                data = request.get_json()
                nombre = data['nombre']
                if not data or 'nombre' not in data:
                    return  jsonify({'error': 'No hay campos para actualizar'}), 400
                sql = 'INSERT INTO empresas (`nombre`) VALUES (%s)'
                cur.execute(sql, (nombre,))
                g.db.commit()
                return jsonify({'message': 'Empresa creada'}), 200
            except Exception as e:
                return jsonify({'error': f'Error al crear empresa: {e}'}), 500

@inces.route('/mod_empresa/<int:id>', methods = ['DELETE', 'PUT'])
@login_required
def mod_empresa(id):
    try:
        with g.db.cursor() as cur:
            if request.method == 'DELETE':
                sql = 'DELETE FROM empresas WHERE id = %s'
                cur.execute(sql, (id,))
                g.db.commit()
                return jsonify({'message': 'Empresa eliminada'}), 200
            else:
                data = request.get_json()
                nombre = data['nombre']
                if not data or 'nombre' not in data:
                    return  jsonify({'error': 'No hay campos para actualizar'}), 400
                
                sql = 'UPDATE empresas SET nombre = %s WHERE id = %s'
                cur.execute(sql, (nombre, id))
                g.db.commit()
                return jsonify({'message': 'Empresa actualizada'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error: {e}'}), 500
    

@inces.route('/buscar_empresa', methods = ['POST'])
def buscar_empresa():
    try:
        nombre = request.form.get('empresa')
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM empresas WHERE nombre = %s', (nombre,))
            result = cur.fetchall()
            columNames = [column[0] for column in cur.description]
            empresas = []
            for record in result:
                empresas.append(dict(zip(columNames, record)))
            return render_template('inces/empresas.html', empresas = empresas)
    except Exception as e:
        print(e)
        return redirect(url_for('inces.empresas'))

# FINALIZAMOS GESTIÓN DE EMPRESAS

