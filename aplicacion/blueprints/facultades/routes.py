from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required

facultades = Blueprint('facultades', __name__, template_folder='templates', static_folder='static')

@facultades.route('/', methods = ['GET', 'POST'])
def index():
    db = current_app.config['db']
    cur = db.cursor()
    if request.method == 'POST':
        nombre_facultad = request.form.get('nombreFacultad')

        try:
            cur.execute('INSERT INTO facultades (`facultad`) VALUES (%s)', (nombre_facultad,))
            db.commit()
            return jsonify({'mensaje': 'facultad creada'}), 200
        except Exception as e:
            db.rollback()
            print(e)
            return jsonify({'error': f'Error al crear facultad: {e}'}), 400
        finally:
            cur.close()
    
    cur.execute('SELECT * FROM facultades')
    registros = cur.fetchall()
    insertRegistros = []
    columNames = [column[0] for column in cur.description]
    for record in registros:
        insertRegistros.append(dict(zip(columNames, record)))
    return render_template('facultades/index.html', facultades = insertRegistros)

@facultades.route('/edit_facultad/<int:idfacultad>', methods = ['PATCH'])
def edit_facultad(idfacultad):
    db = current_app.config['db']
    cur = db.cursor()

    facultad = request.form.get('nombreFacultad')

    try:
        cur.execute('UPDATE facultades SET facultad = %s WHERE idfacultad = %s', (facultad, idfacultad))
        db.commit()
        return jsonify({'mensaje': 'facultad actualizada', 'facultad': f'{idfacultad}'}), 200
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': f'error al actualizar la facultad: {e}'}), 400
    finally:
        cur.close()

@facultades.route('/filtrar_facultad', methods = ['POST'])
def filtrar_facultad():
    db = current_app.config['db']
    cur = db.cursor()
    facultad = request.form['facultad']

    try:
        cur.execute('SELECT * FROM facultades WHERE facultad = %s', (facultad,))
        registros = cur.fetchall()
        insertRegistros = []
        columNames = [column[0] for column in cur.description]
        for record in registros:
            insertRegistros.append(dict(zip(columNames, record)))
        return render_template('facultades/index.html', facultades = insertRegistros)
    except Exception as e:
        print(e)
        return jsonify({'error' f'error buscando facultad: {e}'}), 400
    finally:
        cur.close()
