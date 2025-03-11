from flask import Flask
from flask_login import LoginManager
import pymysql
from os import getenv
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt, generate_password_hash

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['DB_HOST'] = getenv('DB_HOST')
    app.config['DB_USER'] = getenv('DB_USER')
    app.config['DB_PASSWORD'] = getenv('DB_PASSWORD')
    app.config['DB_NAME'] = getenv('DB_NAME')

    app.secret_key = app.config['SECRET_KEY']

    db = pymysql.connect(
    host=app.config['DB_HOST'],
    port=3306,
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


    login_manager = LoginManager()
    login_manager.init_app(app)
    bcrypt = Bcrypt(app)


    @login_manager.user_loader
    def load_users():
        return 

    # importar blueprints
    from aplicacion.blueprints.usuarios.routes import usuario
    app.register_blueprint(usuario, url_prefix='/')

    # Pasar la conexión a la base de datos al Blueprint
    app.config['db'] = db


    return app