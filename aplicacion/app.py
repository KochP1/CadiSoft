from datetime import time, timedelta
from flask import Flask, request, g
from flask_login import LoginManager
import pymysql
from os import getenv
from dotenv import load_dotenv
from .config import Config
from flask_apscheduler import APScheduler
from werkzeug.middleware.proxy_fix import ProxyFix
from dbutils.pooled_db import PooledDB

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

    if getenv('ENVIRONMENT') == 'production':
        from aplicacion.keep_alive import keep_alive
        keep_alive()
    
    # ProxyFix para Railway
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    app.config.update(
        SECRET_KEY=getenv('SECRET_KEY'),
        
        # Configuración de cookies
        SESSION_COOKIE_NAME='app_main_session',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_DOMAIN=None,
        SESSION_COOKIE_PATH='/',
        
        # Flask-Login configuration
        REMEMBER_COOKIE_NAME='app_remember_token',
        REMEMBER_COOKIE_DURATION=timedelta(days=7),
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SAMESITE='Lax',
        REMEMBER_COOKIE_DOMAIN=None,
        REMEMBER_COOKIE_PATH='/',
    )

    db = pymysql.connect(
        host=getenv('DB_HOST'),
        port=int(getenv('DB_PORT')),
        user=getenv('DB_USER'),
        password=getenv('DB_PASSWORD'),
        database=getenv('DB_NAME')
    )
    
    # CONFIGURACIÓN DEL POOL DE CONEXIONES
    DB_CONFIG = {
        'host': getenv('DB_HOST'),
        'port': int(getenv('DB_PORT')),
        'user': getenv('DB_USER'),
        'password': getenv('DB_PASSWORD'),
        'database': getenv('DB_NAME'),
        'charset': 'utf8mb4',
        'autocommit': True
    }
    
    # Crear pool de conexiones
    app.config['DB_POOL'] = PooledDB(
        creator=pymysql,
        mincached=2,           # Conexiones mínimas en el pool
        maxcached=5,           # Conexiones máximas en cache
        maxconnections=20,     # Conexiones máximas totales
        blocking=True,         # Bloquear cuando se alcance el máximo
        maxusage=100,          # Máximo uso por conexión antes de reciclar
        setsession=[],         # Comandos SQL a ejecutar al crear conexión
        ping=1,                # Ping automático (0=no, 1=si, 2=ping robusto)
        **DB_CONFIG
    )
    
    # Inicializar Flask-Login
    login_manager = LoginManager(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = "usuario.index"
    login_manager.login_message = "Tu sesión ha expirado, vuelve a iniciar sesión"
    login_manager.login_message_category = "alert"
    
    # FUNCIÓN PARA OBTENER CONEXIÓN DEL POOL
    def get_db_connection():
        """Obtener conexión del pool"""
        return app.config['DB_POOL'].connection()
    
    # User loader ACTUALIZADO
    from aplicacion.blueprints.usuarios.model import User
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            # Obtener conexión temporal del pool
            db_conn = get_db_connection()
            user = User.get_by_id(db_conn, int(user_id))
            db_conn.close()  # IMPORTANTE: cerrar conexión del user_loader
            return user
        except Exception as e:
            print(f"Error en user_loader: {e}")
            return None
    
    # MIDDLEWARE PARA GESTIÓN AUTOMÁTICA DE CONEXIONES
    @app.before_request
    def before_request():
        """Asignar conexión de BD a g.db para cada request"""
        g.db = get_db_connection()
    
    @app.teardown_appcontext
    def close_db(error):
        """Cerrar conexión al final del request"""
        db = getattr(g, 'db', None)
        if db is not None:
            try:
                db.close()
            except Exception as e:
                print(f"Error cerrando conexión BD: {e}")
    
    # Registrar blueprints
    from aplicacion.blueprints.usuarios.routes import usuario
    from aplicacion.blueprints.diagnostico.routes import diagnostico
    from aplicacion.blueprints.cursos.routes import cursos
    from aplicacion.blueprints.facturacion.routes import facturacion
    from aplicacion.blueprints.profesores.routes import profesores
    from aplicacion.blueprints.alumnos.routes import alumnos
    from aplicacion.blueprints.facultades.routes import facultades
    from aplicacion.blueprints.inscripciones.routes import inscripciones
    from aplicacion.blueprints.acercaDe.routes import acerca
    
    app.register_blueprint(usuario, url_prefix='/')
    app.register_blueprint(diagnostico, url_prefix='/debug')
    app.register_blueprint(cursos, url_prefix='/cursos')
    app.register_blueprint(facturacion, url_prefix='/facturacion')
    app.register_blueprint(profesores, url_prefix='/profesores')
    app.register_blueprint(alumnos, url_prefix='/alumnos')
    app.register_blueprint(facultades, url_prefix='/facultades')
    app.register_blueprint(inscripciones, url_prefix='/inscripciones')
    app.register_blueprint(acerca, url_prefix='/acerca')

    
    # Actualizar Config para usar el pool
    Config.set_db_pool(get_db_connection)
    app.config.from_object(Config)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    return app

    # Middleware para debug
    # @app.before_request
    # def log_session_info():
    #     if request.endpoint and 'debug' not in request.endpoint:
    #         print(f"=== BEFORE REQUEST ===")
    #         print(f"Endpoint: {request.endpoint}")
    #         print(f"User authenticated: {current_user.is_authenticated}")
    #         print(f"Session keys: {list(session.keys())}")
    #         print(f"User ID in session: {session.get('_user_id')}")