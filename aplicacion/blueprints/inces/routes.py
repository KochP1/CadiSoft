from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash, g
from flask_login import login_user, logout_user, current_user, login_required

inces = Blueprint('inces', __name__, template_folder='templates', static_folder='static')

@inces('/cursos', methods = ['GET'])
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
