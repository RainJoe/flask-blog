import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SECURITY_PASSWORD_SALT = 'ss'
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads/test')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost:3306/flaskdemo?charset=utf8'


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}