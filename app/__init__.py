import logging
import os
from flask import Flask
from flask_login import LoginManager
from config import config
from kconfig import settings

__author__ = 'Manuel Escriche'

login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = "Welcome to FIWARE Backlog Management Website!!!"


def create_app(config_name):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    settings.storeHome = app.config['STORE']

    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .urgent import urgent as urgent_blueprint
    app.register_blueprint(urgent_blueprint, url_prefix='/urgent')

    from .accountsdesk import accountsdesk as accountsdesk_blueprint
    app.register_blueprint(accountsdesk_blueprint, url_prefix='/accountsdesk')

    from .helpdesk import helpdesk as helpdesk_blueprint
    app.register_blueprint(helpdesk_blueprint, url_prefix='/helpdesk')

    from .lab import lab as lab_blueprint
    app.register_blueprint(lab_blueprint, url_prefix='/lab')

    from .chapters import chapters as chapters_blueprint
    app.register_blueprint(chapters_blueprint, url_prefix='/chapters')

    from .enablers import enablers as enablers_blueprint
    app.register_blueprint(enablers_blueprint, url_prefix='/enablers')

    from .tools import tools as tools_blueprint
    app.register_blueprint(tools_blueprint, url_prefix='/tools')

    from .delivery import delivery as delivery_blueprint
    app.register_blueprint(delivery_blueprint, url_prefix='/delivery')

    from .guide import guide as guide_blueprint
    app.register_blueprint(guide_blueprint, url_prefix='/guide')

    from .coordination import coordination as coordination_blueprint
    app.register_blueprint(coordination_blueprint, url_prefix='/coordination')

    from .workgroups import workgroups as workgroups_blueprint
    app.register_blueprint(workgroups_blueprint, url_prefix='/workgroups')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
