class Config(object):
  DEBUG = False
  TESTING = False

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
  SECRET_KEY = "thisissecret"
  SECURITY_PASSWORD_SALT = "thisissalt"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECURITY_CSRF_PROTECT_MECHANISMS=None
  SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS=True
  WTF_CSRF_ENABLED=False
  SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'