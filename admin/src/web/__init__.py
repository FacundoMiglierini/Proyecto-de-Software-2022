from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import session
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from src.web.config import config
from src.web.helpers import handlers
from src.core import seeds, database
from src.web.controllers.admin import admin_blueprint
from src.web.controllers.user import user_blueprint
from src.web.controllers.socios import socio_blueprint
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.disciplinas import disciplina_blueprint
from src.web.controllers.cuotas import cuotas_blueprint
from src.web.controllers.api.club import api_club_blueprint
from src.web.controllers.api.socios import api_socio_blueprint
from src.web.controllers.api.auth import api_auth_blueprint
from src.web.helpers.auth import is_authenticated 
from src.web.helpers.roles import user_has_permission
from src.web.controllers.api.auth import login_jwt
from src.web.controllers.api.socios import pagar

def create_app(env="development", static_folder="static"):
    """Método de inicialización de la aplicación"""

    #Environment settings 
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    with app.app_context():
        database.init_app(app)
        database.reset_db()
        seeds.run()

    #CSRF Protection
    def set_csrf():
        csrf = CSRFProtect()
        csrf.init_app(app)
        csrf.exempt(login_jwt)
        csrf.exempt(pagar)

    #Blueprints
    def load_blueprints():
        '''Registro de blueprints'''

        # Controllers
        app.register_blueprint(admin_blueprint)
        app.register_blueprint(user_blueprint)
        app.register_blueprint(auth_blueprint)
        app.register_blueprint(socio_blueprint)
        app.register_blueprint(disciplina_blueprint)
        app.register_blueprint(cuotas_blueprint)
        # API
        app.register_blueprint(api_auth_blueprint)
        app.register_blueprint(api_club_blueprint)
        app.register_blueprint(api_socio_blueprint)

    #Handlers
    def load_handlers():
        '''Registro de handlers'''

        app.register_error_handler(401, handlers.unauthorized)
        app.register_error_handler(403, handlers.forbidden)
        app.register_error_handler(404, handlers.not_found_error)
        app.register_error_handler(500, handlers.internal_server_error)
        
    #Jinja
    def set_commands_jinja():
        '''Carga de comandos de jinja'''
        
        app.jinja_env.globals.update(is_authenticated=is_authenticated)
        app.jinja_env.globals.update(has_permission=user_has_permission)
        
        @app.template_filter('datetime_format')
        def datetime_format(value, format="%H:%M %d-%m-%Y"):
            return value.strftime(format)
            
        app.jinja_env.filters["datetime_format"] = datetime_format

    #Commands
    def set_commands():
        '''Carga de comandos de Flask'''
        
        @app.cli.command(name="resetdb")
        def resetdb():
            database.reset_db()

        @app.cli.command(name="seeds")
        def seedsdb():
            seeds.run()

    #Launcher
    set_csrf()
    load_blueprints()
    load_handlers()
    set_commands_jinja()
    set_commands()
    Session(app) 
    JWTManager(app)
    if env == 'development':
        CORS(app, supports_credentials=True)
     
    #Root page
    @app.route("/")
    def landing():
        '''Landing page de la aplicación'''
        
        if(session.get("username") != None):
            return redirect(url_for("user.index_users"))
        
        return render_template("land_page.html")

    return app
