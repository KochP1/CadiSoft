from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

alumnos = Blueprint('alumnos', __name__, template_folder='templates', static_folder="static")

@alumnos.route('/', methods = ['GET'])
def index():
    return render_template('alumnos/index.html')