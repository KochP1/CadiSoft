from flask import request, render_template, redirect, url_for, Blueprint, current_app
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, generate_password_hash

facturacion = Blueprint('facturacion', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@facturacion.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('facturacion/index.html')

@facturacion.route('/inventario',methods = ['GET', 'POST'])
def inventario():
    if request.method == 'GET':
        return render_template('facturacion/inventario.html')