from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

alumnos = Blueprint('alumnos', __name__, template_folder='templates', static_folder="static")

@alumnos.route('/', methods = ['GET'])
def index():
    try:
        db = current_app.config['db']
        cur = db.cursor()
        sql = 'SELECT a.idAlumno, a.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email FROM alumnos a JOIN usuarios u ON a.idusuarios = u.idusuarios'
        cur.execute(sql)
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        return render_template('alumnos/index.html', alumnos = InsertRegistros)
    except Exception as e:
        print(e)
        return render_template('alumnos/index.html')
    finally:
        cur.close()

@alumnos.route('/buscar_alumno', methods = ['POST'])
def buscar_alumno():
    db = current_app.config['db']
    cedula = request.form['cedula']
    cur = db.cursor()
    sql = 'SELECT a.idAlumno, a.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email FROM alumnos a JOIN usuarios u ON a.idusuarios = u.idusuarios WHERE u.cedula = %s'
    data = (cedula,)
    cur.execute(sql, data)
    registros = cur.fetchall()
    if len(registros) == 0:
        flash('Cédula incorrecta', 'error')
        return redirect(url_for('alumnos.index'))
    insertRegistros = []
    columNames = [column[0] for column in cur.description]
    for record in registros:
        insertRegistros.append(dict(zip(columNames, record)))
    return render_template('alumnos/index.html', alumnos = insertRegistros)

@alumnos.route('/registro_familiar', methods = ['GET'])
def registro_familiar():
    db = current_app.config['db']
    cur = db.cursor()
    sql = 'SELECT f.idFamilia, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, f.NombrePapa, f.ApellidoPapa, f.NombreMama, f.ApellidoMama, f.Telefono FROM registro_familiar f JOIN alumnos a ON f.idAlumno = a.idAlumno JOIN usuarios u ON a.idusuarios = u.idusuarios'
    cur.execute(sql)
    registros = cur.fetchall()
    insertRegistros = []
    columNames = [column[0] for column in cur.description]
    for record in registros:
        insertRegistros.append(dict(zip(columNames, record)))
    return render_template('alumnos/registFamiliar.html', familias = insertRegistros)

@alumnos.route('/buscar_registro_familiar', methods = ['POST'])
def buscar_registro_familiar():
    try:
        db = current_app.config['db']
        cedula = request.form['cedula']
        cur = db.cursor()
        sql = 'SELECT f.idFamilia, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, f.NombrePapa, f.ApellidoPapa, f.NombreMama, f.ApellidoMama, f.Telefono FROM registro_familiar f JOIN alumnos a ON f.idAlumno = a.idAlumno JOIN usuarios u ON a.idusuarios = u.idusuarios WHERE u.cedula = %s'
        data = (cedula,)
        cur.execute(sql, data)
        registros = cur.fetchall()

        if len(registros) == 0:
            flash('Cédula incorrecta', 'error')
            return redirect(url_for('alumnos.registro_familiar'))
        insertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            insertRegistros.append(dict(zip(columNames, record)))
        return render_template('alumnos/registFamiliar.html', familias = insertRegistros)
    except Exception as e:
        print(e)
        return redirect(url_for('alumnos.registro_familiar'))
    
@alumnos.route('/eliminar_alumno/<int:idusuarios>', methods = ['DELETE'])
def eliminar_alumno(idusuarios):
    db = current_app.config['db']
    cur = db.cursor()

    try:
        cur.execute('DELETE FROM usuarios WHERE idusuarios = %s', (idusuarios))
        db.commit()
        return jsonify({'mensaje': 'alumno eliminado'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'{e}'}), 400
    finally:
        cur.close()