from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from config import config

db = SQLAlchemy()
security = Security()

from .models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    security.init_app(app, user_datastore)

    return app