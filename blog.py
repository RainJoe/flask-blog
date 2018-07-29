import os
from app import create_app, db, user_datastore
from app.models import User, Role
from flask_migrate import Migrate, upgrade
from flask_security.utils import hash_password

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


def create_superuser():
    if Role.query.filter_by(name='admin').first():
        return
    password_raw = os.getenv("FLASK_USER_PASSWORD") or '123456'
    password_hash = hash_password(password_raw)
    try:
        role = user_datastore.create_role(name='admin')
        user = user_datastore.create_user(name=os.getenv("FLASK_USER") or "admin",
                                          email=os.getenv("FLASK_USER_EMAIL") or "email@example.com",
                                          password=password_hash)
        user_datastore.add_role_to_user(user, role)
        db.session.commit()
    except Exception as e:
        print(e)
        pass


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    upgrade()
    db.create_all()
    create_superuser()
