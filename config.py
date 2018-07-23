import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or '0a4d55a8d778e5022fab701977c5d840bbc486d0'
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost:3306/flaskblog?charset=utf8'
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads/test')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost:3306/flaskblog?charset=utf8'


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}