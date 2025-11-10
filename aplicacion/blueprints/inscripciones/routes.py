from datetime import timedelta
from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, Response, g
from flask_login import login_required
from flask_bcrypt import Bcrypt

from aplicacion.blueprints.cursos.routes import dateToString
from aplicacion.blueprints.shared.reporte_inscripciones import reporte_inscripciones

inscripciones = Blueprint('inscripciones', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

# PRE INSCRIPCIONES
@inscripciones.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        try:
            with g.db.cursor() as cur:
                cur.execute('SELECT * FROM preinscripcion')
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [columns[0] for columns in cur.description]

                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                return render_template('inscripciones/index.html', preinscripciones = insertRegistros)
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return render_template('inscripciones/index.html', preinscripciones=[])

@inscripciones.route('/procesar_preinscripcion/<int:id>/<curso>', methods = ['GET'])
@login_required
def procesar_preinscripcion(id, curso):
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM usuarios WHERE idusuarios = %s', (id,))
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [columns[0] for columns in cur.description]

            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))
            
            return render_template('inscripciones/preinscripcion.html', preinscripcion = insertRegistros, idusuario = id, curso = curso)
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return redirect(url_for('inscripciones.index'))

@inscripciones.route('/elim_preinscripcion/<int:id>', methods = ['DELETE'])
@login_required
def elim_preinscripcion(id):
    try:
        with g.db.cursor() as cur:
            cur.execute('DELETE FROM preinscripcion WHERE idPreinscipcion = %s', (id,))
            g.db.commit()
            return jsonify({'mensaje': 'preinscripcion eliminada'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al eliminar preinscripcion'}), 500

# INSCRIPCIONES

@inscripciones.route('/reporte_insc', methods = ['GET'])
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

        response = reporte_inscripciones(g.db, 'Privada', p_cedula, p_fecha_inscripcion, p_idSeccion, p_fecha_expiracion, p_es_activa)
        return response
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error: {e}'}), 500
@inscripciones.route('/gestion_insc', methods = ['GET', 'POST'])
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
                cur.callproc('reporte_inscripciones_sp', [p_cedula, p_fecha_inscripcion, p_idSeccion, p_fecha_expiracion, 'Privada', p_es_activa])

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
                
            return render_template('inscripciones/gestionar_inscripciones.html', inscripciones=inscripciones, cedula = p_cedula, fecha_inscripcion = p_fecha_inscripcion, fecha_expiracion = p_fecha_expiracion, idSeccion = p_idSeccion, status = p_es_activa)
        with g.db.cursor() as cur:
            cur.callproc('reporte_inscripciones_sp', [None, None, None, None, 'Privada', None])
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
            
        return render_template('inscripciones/gestionar_inscripciones.html', inscripciones=inscripciones)
    
    except Exception as e:
        print(e)
        return f'{e}'
@inscripciones.route('/alumnos_regulares', methods = ['POST', 'GET'])
@login_required
def alumnos_regulares():

    # POST alumno
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        segundoNombre = request.form.get('segundoNombre')
        apellido = request.form.get('apellido')
        segundoApellido = request.form.get('segundoApellido')
        cedula = request.form.get('cedula')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        rol = 'alumno'
        curso = request.form.get('curso')
        contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

        try:
            imagen = request.files['imagen']
        except KeyError as e:
            imagen = None

        try:
            with g.db.cursor() as cur:
                if imagen == None:
                    sql_usuario = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
                    usuario = (
                        nombre,
                        segundoNombre,
                        apellido,
                        segundoApellido,
                        cedula,
                        email,
                        contraseña_hash,
                        rol
                        )
                    
                    if curso:
                        cur.execute(sql_usuario, usuario)
                        g.db.commit()
                        cur.execute('SELECT idusuarios FROM usuarios WHERE cedula = %s', (cedula,))
                        registro = cur.fetchone()
                        registroStr = ''.join(map(str, registro))
                        idusuario = int(registroStr)

                        cur.execute('DELETE FROM preinscripcion WHERE cedula = %s', (cedula,))
                        g.db.commit()
                        
                        return redirect(url_for('inscripciones.procesar_preinscripcion', id = idusuario, curso=request.form.get('curso')))
                
                else:
                    sql_usuario = 'INSERT INTO usuarios (`nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`, `imagen`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    imagen_blob = imagen.read()
                    usuario = (
                        nombre,
                        segundoNombre,
                        apellido,
                        segundoApellido,
                        cedula,
                        email,
                        contraseña_hash,
                        rol,
                        imagen_blob
                        )
                
                cur.execute(sql_usuario, usuario)
                g.db.commit()
                return jsonify({'mensaje': 'Alumno creado satisfactiramente'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': 'Error al crear el usuario'}), 500
    
    if request.method == 'GET':
        return render_template('inscripciones/alumnosRegulares.html')

@inscripciones.route('/buscar_alumno', methods = ['POST'])
@login_required
def buscar_alumno():
    cedula = request.form.get('cedula')
    rol = 'alumno'

    if not cedula:
        return jsonify({'error': 'La cédula es requerida'}), 400

    try:
        with g.db.cursor() as cur:
            sql = 'SELECT u.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email FROM usuarios u WHERE u.rol = %s AND u.cedula = %s'
            data = (rol, cedula)
            cur.execute(sql, data)
            alumno = cur.fetchone()

            if alumno:
                columNames = [column[0] for column in cur.description]
                alumno_dict = dict(zip(columNames, alumno))
                return jsonify({'alumno': alumno_dict}), 200
            else:
                return jsonify({'success': False, 'message': 'Alumno no encontrado'}), 404
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno al buscar alumno',
            'details': str(e)
        }), 500
    
@inscripciones.route('/buscar_curso', methods = ['POST'])
@login_required
def buscar_curso():

    if not request.json:
        return jsonify({'error': 'La cédula es requerida'}), 400
    
    data = request.get_json()

    required_fields = ['curso']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400

    try:
        with g.db.cursor() as cur:
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
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno al buscar curso',
            'details': str(e)
        }), 500
    
def time_delta_serializer(time_data):
    # Convertir timedelta a string HH:MM:SS
    total_seconds = time_data.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    time_data = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_data


@inscripciones.route('mostar_horario', methods = ['POST'])
@login_required
def mostrar_horario():
    if not request.json:
        return jsonify({'error': 'La cédula es requerida'}), 400
    
    data = request.get_json()

    required_fields = ['idSeccion']

    if not all(field in data for field in required_fields):
        return jsonify({"error": "faltan campos"}), 400
    
    try:
        with g.db.cursor() as cur:
            sql = 'SELECT h.idhorario, h.horario_dia, h.horario_hora, h.horario_hora_final, h.horario_aula, s.idSeccion, c.nombre_curso FROM horario_x_curso hxc JOIN horario h ON hxc.idhorario = h.idhorario JOIN secciones s ON hxc.idSeccion = s.idSeccion JOIN cursos c ON s.idCurso = c.idCurso WHERE s.idSeccion = %s'
            data = (data['idSeccion'],)
            cur.execute(sql, data)
            seccion = cur.fetchall()

            if seccion:
                columNames = [column[0] for column in cur.description]
                seccion_dict = [dict(zip(columNames, row)) for row in seccion]
                
                for record in seccion_dict:
                    if isinstance(record.get('horario_hora'), timedelta):
                        record['horario_hora'] = time_delta_serializer(record['horario_hora'])

                    if isinstance(record.get('horario_hora_final'), timedelta):
                        record['horario_hora_final'] = time_delta_serializer(record['horario_hora_final'])
                
                return jsonify({'horarioSeccion': seccion_dict}), 200
            else:
                return jsonify({'success': False, 'message': 'horario de seccion no encontrado'}), 404
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno al buscar el horario',
            'details': str(e)
        }), 500

@inscripciones.route('/inscribir_alumno', methods = ['POST'])
@login_required
def inscribir_alumno():
    idAlumno = request.form.get('idAlumno')
    periodoInicio = request.form.get('periodoInicio')
    periodoFinal = request.form.get('periodoFinal')
    tipo = request.form.get('tipo')
    es_activa = 1
    idSeccion = request.form.get('idSeccion')

    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT idInscripcion FROM inscripcion WHERE idusuarios = %s AND fecha_inscripcion = %s AND fecha_expiracion = %s', (idAlumno, periodoInicio, periodoFinal))
            validacion = cur.fetchone()

            if validacion is not None:
                return jsonify({'error': 'Ya existe una inscripcion para este alumno en este periodo'}), 400

            sql = 'INSERT INTO inscripcion (`idusuarios`, `fecha_inscripcion`, `fecha_expiracion`, `tipo`, `es_activa`) VALUES (%s, %s, %s, %s, %s)'
            data = (
                idAlumno,
                periodoInicio,
                periodoFinal,
                tipo,
                es_activa
            )
            cur.execute(sql, data)
            g.db.commit()

            sql_idInscripcion = 'SELECT idInscripcion FROM inscripcion WHERE idusuarios = %s AND fecha_inscripcion = %s AND fecha_expiracion = %s'
            cur.execute(sql_idInscripcion, (idAlumno, periodoInicio, periodoFinal))
            idAlumnoInscripcion = cur.fetchone()

            sql_inscripcionesXcursos = 'INSERT INTO insc_x_seccion (`idInscripcion`, `idSeccion`) VALUES (%s, %s)'
            cur.execute(sql_inscripcionesXcursos, (idAlumnoInscripcion, idSeccion))
            g.db.commit()

            cur.execute('INSERT INTO calificaciones (`idusuarios`, `idSeccion`, `idInscripcion`) VALUES (%s, %s, %s)', (idAlumno, idSeccion, idAlumnoInscripcion))
            g.db.commit()
            
            return jsonify({'mensaje': 'Alumno inscrito satisfactoriamente'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': 'Error al inscribir alumno'}), 400