from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

acerca = Blueprint('acerca', __name__, template_folder='templates', static_folder='static')

# ACERCA DE 

@acerca.route('/')
def index():
    return render_template('acercaDe/index.html')