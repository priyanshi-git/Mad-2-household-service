from flask import Flask
from application.models import db, User, Role
from config import DevelopmentConfig
from application.resources import api
from flask_security import SQLAlchemyUserDatastore, Security
from application.sec import datastore
from application.worker import celery_init_app
from celery import Celery
from celery.schedules import crontab
from application.tasks import daily_reminder

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


celery_app.conf.timezone = "Asia/Kolkata"  # Replace with your local timezone
celery_app.conf.enable_utc = False  # Disable UTC if you're using local time


@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1'),
        daily_reminder.s("vishal@iitm.in", 'Happy Monday!'),
    )

if __name__ == "__main__":
  app.run(debug=True)