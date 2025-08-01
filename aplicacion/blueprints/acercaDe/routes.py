from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

acerca = Blueprint('acerca', __name__, template_folder='templates', static_folder='static')

# ACERCA DE 

tables = ['usuarios', 'profesores', 'secciones', 'registro_familiar', 'productos', 'preinscripcion', 'insc_x_seccion', 'inscripcion', 'horario_x_curso', 'horario', 'facultades', 'factura_productos', 'facturas', 'cursos', 'codigos_verificacion', 'calificaciones']
@acerca.route('/')
def index():
    return render_template('acercaDe/index.html')

@acerca.route('/restaurar', methods = ['POST'])
def restaurar():
    db = current_app.config['db']

    with db.cursor() as cur:
        try:
            for record in tables:
                cur.execute(f'Delete FROM {record}')
                db.commit()
                cur.execute(f'ALTER TABLE {record} AUTO_INCREMENT = 1')
                db.commit()
            return jsonify({'mensaje': 'Restauración completada'}), 200
        except Exception as e:
            db.rollback()
            print(e)
            return jsonify({'error': f'Error al restaurar sistema: {e}'}), 500