from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, generate_password_hash

usuario = Blueprint('usuario', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@usuario.route('/')
def index():
    return render_template('usuarios/index.html')