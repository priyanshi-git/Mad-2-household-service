from flask import Flask
from application.models import db, User, Role
from config import DevelopmentConfig
from application.resources import api
from flask_security import SQLAlchemyUserDatastore, Security
from application.sec import datastore
from application.worker import celery_init_app

def create_app():
  app = Flask(__name__)
  app.config.from_object(DevelopmentConfig)
  db.init_app(app)
  api.init_app(app)
  
  app.security = Security(app, datastore)
  with app.app_context():
    import application.views

  return app

app = create_app()
celery_app = celery_init_app(app)

if __name__ == "__main__":
  app.run(debug=True)