
import os

__author__ = 'Manuel Escriche'

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SERVER_NAME='backlog.fiware.org'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(24)
    DATABASE_URI = ''
    HOME = basedir

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False
    HTMLDOCS = os.path.join(Config.HOME, 'docs')
    STORE = os.path.join(Config.HOME, 'store')
    LOGS = os.path.join(Config.HOME, 'logs')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    STORE = os.path.join(Config.HOME, 'store')
    LOGS = os.path.join(Config.HOME, 'logs')

    HTMLDOCS = '/Users/MANEV/FIWARE/FW-BacklogHelp/build/html'
    DOCS = '/Users/MANEV/FIWARE/FW-BacklogHelp/build/web/data'
    # LOGS = '/Users/fiware/Development/management-backlogwebsite'


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    STORE = os.path.join(Config.HOME, 'store')
    LOGS = os.path.join(Config.HOME, 'logs')
    DOCS = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
