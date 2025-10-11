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
from werkzeug.middleware.proxy_fix import ProxyFix
import redis

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

    # --- CONFIGURACIONES CLAVE PARA SESIONES MÚLTIPLES EN PRODUCCIÓN (Railway/HTTPS) ---
    # 1. Fuerza que la cookie solo se envíe sobre HTTPS (ESENCIAL en Railway)
    app.config['SESSION_COOKIE_SECURE'] = True
    # 2. Controla cuándo la cookie es enviada por el navegador (buena práctica de seguridad)
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    # 3. La sesión no es permanente por defecto (depende de login_user(remember=True))
    app.config['SESSION_PERMANENT'] = False
    # 4. Establece la duración de la cookie si se usa remember=True
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    # 5. AÑADIDO: Define un nombre de cookie ÚNICO para evitar colisiones con cookies viejas
    app.config['SESSION_COOKIE_NAME'] = 'fs_multi_session'
    # 6. AÑADIDO: Firma la cookie de sesión para mayor seguridad
    app.config['SESSION_USE_SIGNER'] = True

    # AÑADIDO: Asegurar que la cookie se aplica al dominio actual (necesario en proxies)
    # None permite al navegador usar el dominio del host actual.
    app.config['SESSION_COOKIE_DOMAIN'] = None
    # AÑADIDO: Asegurar que la cookie se aplica a todas las rutas.
    app.config['SESSION_COOKIE_PATH'] = '/'

    #app.secret_key = app.config['SECRET_KEY']

    db = pymysql.connect(
    host=app.config['DB_HOST'],
    port=int(app.config['DB_PORT']),
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    database=app.config['DB_NAME']
)

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

    app.config['SESSION_TYPE'] = 'redis'
    redis_url = getenv('REDIS_URL')
    if redis_url:
        # Intenta conectar usando la URL (p. ej., de Railway)
        try:
            # Esta llamada fallará si el hostname 'redis.railway.internal' no es resoluble localmente
            app.config['SESSION_REDIS'] = redis.from_url(redis_url)
            app.config['SESSION_REDIS'].ping() # Prueba la conexión
            print("Configurando sesiones con Redis usando URL (REDIS_URL).")
        except Exception as e:
            # Error de conexión (probablemente el error 11001 "getaddrinfo failed")
            print(f"ATENCION: FALLO la conexión a Redis usando REDIS_URL. Error: {e}")
            print("Volviendo a la sesión basada en cookies (SESSION_TYPE='null') para iniciar la aplicación.")
            app.config['SESSION_TYPE'] = 'null' # Fallback para que la app no se bloquee localmente
    Session(app)
    print(f"Sesión configurada con tipo: {app.config.get('SESSION_TYPE', 'cookie por defecto')}")

    app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = getenv('MAIL_DEFAULT_SENDER')
    mail = Mail(app)

    login_manager = LoginManager(app)
    login_manager.session_protection = None 
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