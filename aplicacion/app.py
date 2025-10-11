from datetime import timedelta
from flask import Flask, current_app, request, session
from flask_login import LoginManager, current_user, login_user
from flask_mail import Mail
import pymysql
from os import getenv
from dotenv import load_dotenv
from .config import Config
from flask_apscheduler import APScheduler
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
import redis
import uuid

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['DB_HOST'] = getenv('DB_HOST')
    app.config['DB_USER'] = getenv('DB_USER')
    app.config['DB_PASSWORD'] = getenv('DB_PASSWORD')
    app.config['DB_NAME'] = getenv('DB_NAME')
    app.config['DB_PORT'] = getenv('DB_PORT')

    # Configuración de Redis para sesiones
    redis_url = getenv('REDIS_URL')
    if redis_url:
        try:
            redis_client = redis.from_url(redis_url)
            redis_client.ping()
            app.config['SESSION_TYPE'] = 'redis'
            app.config['SESSION_REDIS'] = redis_client
            app.config['SESSION_USE_SIGNER'] = True
            app.config['SESSION_PERMANENT'] = True
            app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
            app.config['SESSION_KEY_PREFIX'] = 'flask_session:'
            print("Redis configurado correctamente para sesiones")
        except Exception as e:
            print(f"Error conectando a Redis: {e}")
            app.config['SESSION_TYPE'] = 'filesystem'
    else:
        app.config['SESSION_TYPE'] = 'filesystem'

    # Configuración de cookies para sesiones múltiples
    app.config['SESSION_COOKIE_NAME'] = 'app_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True  # True para HTTPS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Cambia a 'Lax' o 'None'
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True

    # Inicializar Flask-Session ANTES de Flask-Login
    Session(app)

    # Configuración de la base de datos
    db = pymysql.connect(
        host=app.config['DB_HOST'],
        port=int(app.config['DB_PORT']),
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME']
    )

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("Conexión a BD establecida")
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")

    app.app_context().push()

    # Configuración de email
    app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')
    mail = Mail(app)

    # Configuración de Flask-Login
    login_manager = LoginManager(app)
    login_manager.session_protection = "strong"  # Importante para seguridad
    
    from aplicacion.blueprints.usuarios.model import User
    
    @login_manager.user_loader
    def load_user(user_id):
        db = current_app.config['db']
        return User.get_by_id(db, int(user_id))

    # Registrar blueprints
    from aplicacion.blueprints.usuarios.routes import usuario
    from aplicacion.blueprints.cursos.routes import cursos
    from aplicacion.blueprints.facturacion.routes import facturacion
    from aplicacion.blueprints.profesores.routes import profesores
    from aplicacion.blueprints.alumnos.routes import alumnos
    from aplicacion.blueprints.facultades.routes import facultades
    from aplicacion.blueprints.inscripciones.routes import inscripciones
    from aplicacion.blueprints.acercaDe.routes import acerca

    app.register_blueprint(usuario, url_prefix='/')
    app.register_blueprint(cursos, url_prefix='/cursos')
    app.register_blueprint(facturacion, url_prefix='/facturacion')
    app.register_blueprint(profesores, url_prefix='/profesores')
    app.register_blueprint(alumnos, url_prefix='/alumnos')
    app.register_blueprint(facultades, url_prefix='/facultades')
    app.register_blueprint(inscripciones, url_prefix='/inscripciones')
    app.register_blueprint(acerca, url_prefix='/acerca')

    app.config['db'] = db
    app.config['mail'] = mail

    Config.set_db(db)
    app.config.from_object(Config)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    return app