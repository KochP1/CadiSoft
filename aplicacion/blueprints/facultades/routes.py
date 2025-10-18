from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash, g
from flask_login import login_user, logout_user, current_user, login_required

facultades = Blueprint('facultades', __name__, template_folder='templates', static_folder='static')

@facultades.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        nombre_facultad = request.form.get('nombreFacultad')

        try:
            with g.db.cursor() as cur:
                cur.execute('INSERT INTO facultades (`facultad`) VALUES (%s)', (nombre_facultad,))
                g.db.commit()
                return jsonify({'mensaje': 'facultad creada'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'Error al crear facultad: {e}'}), 400
    
    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM facultades')
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))
            return render_template('facultades/index.html', facultades = insertRegistros)
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return render_template('facultades/index.html', facultades=[])

@facultades.route('/edit_facultad/<int:idfacultad>', methods = ['PATCH', 'DELETE'])
@login_required
def edit_facultad(idfacultad):
    if request.method == 'PATCH':
        facultad = request.form.get('nombreFacultad')

        try:
            with g.db.cursor() as cur:
                cur.execute('UPDATE facultades SET facultad = %s WHERE idFacultad = %s', (facultad, idfacultad))
                g.db.commit()
                return jsonify({'mensaje': 'facultad actualizada', 'facultad': f'{idfacultad}'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'error al actualizar la facultad: {e}'}), 400
    
    if request.method == 'DELETE':
        try:
            with g.db.cursor() as cur:
                cur.execute('DELETE FROM facultades WHERE idFacultad = %s', (idfacultad))
                g.db.commit()
                return jsonify({'mensaje': 'facultad eliminada', 'facultad': f'{idfacultad}'})
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': 'error al eliminar la facultad'}), 400

@facultades.route('/filtrar_facultad', methods = ['POST'])
@login_required
def filtrar_facultad():
    facultad = request.form['facultad']

    try:
        with g.db.cursor() as cur:
            cur.execute('SELECT * FROM facultades WHERE facultad = %s', (facultad,))
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [column[0] for column in cur.description]
            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))
            return render_template('facultades/index.html', facultades = insertRegistros)
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'error buscando facultad: {e}'}), 400