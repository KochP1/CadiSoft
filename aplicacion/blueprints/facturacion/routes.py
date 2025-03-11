from flask import request, render_template, redirect, url_for, Blueprint, current_app
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, generate_password_hash

facturacion = Blueprint('facturacion', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()