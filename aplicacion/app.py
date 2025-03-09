from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

    login_manager = LoginManager()
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_users():
        return 

    # importar blueprints
    from aplicacion.blueprints.usuarios.routes import usuario
    app.register_blueprint(usuario, url_prefix='/')

    return app