from flask import Flask
import views
from application.database import db, security
from application.create_initial_data import create_data
import resources
import os

app = None
rootDir = os.path.abspath(os.path.dirname('file'))

database_uri = f"sqlite:///{os.path.join(rootDir, 'instance', 'mad2_project.db')}"
print(database_uri)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'should-not-be-exposed'
    app.config["SECURITY_PASSWORD_SALT"] = "salty-password"
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    db.init_app(app)

    with app.app_context():
        from application.models import User, Role
        from flask_security import SQLAlchemyUserDatastore

        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security.init_app(app, user_datastore)
        db.create_all()
        
        # Call create_data here, passing app and user_datastore
        create_data(app, user_datastore)
    
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['SECURITY_CSRF_PROTECT_MECHANISHMS'] = True
    app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True

    views.create_view(app, user_datastore, db)

    #connect flask to flask_restful
    resources.api.init_app(app)
    app.app_context().push()
    app.debug = True
    
    return app

app = create_app()

# from application.controllers import *

if __name__ == '__main__':
    app.run()