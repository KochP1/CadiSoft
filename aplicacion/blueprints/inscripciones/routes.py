from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, Response
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

inscripciones = Blueprint('inscripciones', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@inscripciones.route('/')
def index():
    return render_template('inscripciones/index.html')

@inscripciones.route('/alumnos_regulares')
def alumnos_regulares():
    return render_template('inscripciones/alumnosRegulares.html')
