from flask import request, render_template, redirect, url_for, Blueprint, current_app
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, generate_password_hash

usuario = Blueprint('usuario', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@usuario.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('usuarios/index.html')

@usuario.route('/regist_user', methods = ['GET', 'POST'])
def regist_user():
    return render_template('usuarios/regist.html')

@usuario.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
    return render_template('usuarios/forgot.html')