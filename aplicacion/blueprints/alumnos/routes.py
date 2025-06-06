from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

alumnos = Blueprint('alumnos', __name__, template_folder='templates', static_folder="static")

# ALUMNOS 
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



@alumnos.route('/edit_alumno/<int:idusuarios>')
def edit_alumno(idusuarios):
    try:
        db = current_app.config['db']
        cur = db.cursor()
        sql = 'SELECT a.idAlumno, a.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, u.cedula, u.email, u.imagen FROM alumnos a JOIN usuarios u ON a.idusuarios = u.idusuarios WHERE a.idusuarios = %s'
        data = (idusuarios,)
        cur.execute(sql, data)
        registros = cur.fetchall()
        InsertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            InsertRegistros.append(dict(zip(columNames, record)))
        print(InsertRegistros)
        return render_template('alumnos/edit_alumno.html', alumnos = InsertRegistros)
    except Exception as e:
        print(e)
        return url_for('alumnos.index')
    finally:
        cur.close()

# FINALIZAN ENDPOINTS DE ALUMNOS

# REGISTRO FAMILIAR

@alumnos.route('/crear_registro_familiar/<int:idAlumno>', methods = ['POST'])
def crear_registro_familiar(idAlumno):
    db = current_app.config['db']
    db.ping(reconnect=True)

    nombrePapa = request.form.get('nombrePapa')
    apellidoPapa = request.form.get('apellidoPapa')
    nombreMama = request.form.get('nombreMama')
    apellidoMama = request.form.get('apellidoMama')
    contacto = request.form.get('contacto')

    try:
        with db.cursor() as cur:
            sql = 'INSERT INTO registro_familiar (`idAlumno`, `NombrePapa`, `ApellidoPapa`, `NombreMama`, `ApellidoMama`, `Telefono`) VALUES (%s, %s, %s, %s, %s, %s)'
            data = (idAlumno, nombrePapa, apellidoPapa, nombreMama, apellidoMama, contacto)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar creado satisfactoriamente'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al crear registro familiar'}), 400




@alumnos.route('/registro_familiar', methods = ['GET'])
def registro_familiar():
    db = current_app.config['db']
    if request.method == 'GET':
        cur = db.cursor()
        sql = 'SELECT f.idFamilia, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, f.NombrePapa, f.ApellidoPapa, f.NombreMama, f.ApellidoMama, f.Telefono FROM registro_familiar f JOIN alumnos a ON f.idAlumno = a.idAlumno JOIN usuarios u ON a.idusuarios = u.idusuarios'
        cur.execute(sql)
        registros = cur.fetchall()
        insertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            insertRegistros.append(dict(zip(columNames, record)))
        cur.close()
        return render_template('alumnos/registFamiliar.html', familias = insertRegistros)




@alumnos.route('/edit_registro_familiar/<int:idFamilia>')
def edit_registro_familiar(idFamilia):
    db = current_app.config['db']
    try:
        with db.cursor() as cur:
            sql = 'SELECT f.idFamilia, u.idusuarios, u.nombre, u.segundoNombre, u.apellido, u.SegundoApellido, f.NombrePapa, f.ApellidoPapa, f.NombreMama, f.ApellidoMama, f.Telefono FROM registro_familiar f JOIN alumnos a ON f.idAlumno = a.idAlumno JOIN usuarios u ON a.idusuarios = u.idusuarios WHERE f.idFamilia = %s'
            cur.execute(sql, (idFamilia,))
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))
            print(insertRegistros)
            return render_template('alumnos/edit_registro_familiar.html', familia = insertRegistros)
    except Exception as e:
        print(e)




@alumnos.route('/edit_registro_fam_papa/<int:idFamilia>', methods = ['PATCH'])
def edit_registro_fam_papa(idFamilia):
    db = current_app.config['db']
    NombrePapa = request.form.get('NombrePapa')
    ApellidoPapa = request.form.get('ApellidoPapa')

    if not NombrePapa or not ApellidoPapa:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400
    try:
        with db.cursor() as cur:
            sql = 'UPDATE registro_familiar SET NombrePapa = %s, ApellidoPapa = %s WHERE idFamilia = %s'
            data = (NombrePapa, ApellidoPapa, idFamilia)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar actualizado satisfactoriamente'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error al actualizar datos del papa: {e}'}), 500




@alumnos.route('/edit_registro_fam_mama/<int:idFamilia>', methods = ['PATCH'])
def edit_registro_fam_mama(idFamilia):
    db = current_app.config['db']
    NombreMama = request.form.get('NombreMama')
    ApellidoMama = request.form.get('ApellidoMama')
    try:
        with db.cursor() as cur:
            sql = 'UPDATE registro_familiar SET NombreMama = %s, ApellidoMama = %s WHERE idFamilia = %s'
            data = (NombreMama, ApellidoMama, idFamilia)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar actualizado satisfactoriamente'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error al actualizar datos de la mama: {e}'}), 500




@alumnos.route('/edit_registro_fam_contacto/<int:idFamilia>', methods = ['PATCH'])
def edit_registro_fam_contacto(idFamilia):
    db = current_app.config['db']
    contacto = request.form.get('contacto')
    try:
        with db.cursor() as cur:
            sql = 'UPDATE registro_familiar SET Telefono = %s WHERE idFamilia = %s'
            data = (contacto, idFamilia)
            cur.execute(sql, data)
            db.commit()
            return jsonify({'message': 'Registro familiar actualizado satisfactoriamente'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error al actualizar contacto de la familia: {e}'}), 500




@alumnos.route('/eliminar_registro_familiar/<int:idRegistro>', methods = ['DELETE'])
def eliminar_registro_familiar(idRegistro):
    db = current_app.config['db']
    try:
        with db.cursor() as cur:
            sql = 'DELETE FROM registro_familiar WHERE idFamilia = %s'
            cur.execute(sql, (idRegistro,))
            db.commit()
            return jsonify({'message': 'Registro familiar eliminado satisfactoriamente'})
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'Error al eliminar registro familiar: {e}'}), 500




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

# FINALIZA REGISTRO FAMILIAR