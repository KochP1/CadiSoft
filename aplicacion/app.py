from datetime import timedelta
from flask import Flask, current_app
from flask_login import LoginManager
from flask_mail import Mail
import pymysql
from os import getenv
from dotenv import load_dotenv
from .config import Config
from flask_apscheduler import APScheduler
from flask_session import Session

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_COOKIE_NAME'] = 'mi_app_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # True si usas HTTPS en producción
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Asegúrate de que cada dispositivo tenga su propia sesión
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True

    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['DB_HOST'] = getenv('DB_HOST')
    app.config['DB_USER'] = getenv('DB_USER')
    app.config['DB_PASSWORD'] = getenv('DB_PASSWORD')
    app.config['DB_NAME'] = getenv('DB_NAME')
    app.config['DB_PORT'] = getenv('DB_PORT')

    app.secret_key = app.config['SECRET_KEY']

    db = pymysql.connect(
    host=app.config['DB_HOST'],
    port=int(app.config['DB_PORT']),
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    database=app.config['DB_NAME']
)
    
    app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')

    mail = Mail(app)
    session = Session(app)

    try:
        with db.cursor() as cursor:
            # Ejecutar una consulta sencilla para comprobar la conexión
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("Conexion")
            else:
                print("error")
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    
    app.app_context().push()


    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.session_protection = "basic"  # o "strong"
    login_manager.refresh_view = "usuario.index"

    from aplicacion.blueprints.usuarios.model import User
    @login_manager.user_loader
    def load_users(user_id):
        db = current_app.config['db']
        return User.get_by_id(db, int(user_id))

    # importar blueprints
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
    app.register_blueprint(alumnos, url_prefix = '/alumnos')
    app.register_blueprint(facultades, url_prefix = '/facultades')
    app.register_blueprint(inscripciones, url_prefix = '/inscripciones')
    app.register_blueprint(acerca, url_prefix = '/acerca')

    app.config['db'] = db
    app.config['mail'] = mail

    Config.set_db(db)
    app.config.from_object(Config)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    return app