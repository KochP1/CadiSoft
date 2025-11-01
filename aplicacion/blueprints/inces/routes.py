from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, flash, g
from flask_login import login_user, logout_user, current_user, login_required

inces = Blueprint('inces', __name__, template_folder='templates', static_folder='static')