from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()


class RolesUsers(db.Model):
  __tablename__ = 'roles_users'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
  role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  email = db.Column(db.String, nullable=False, unique=True)
  password = db.Column(db.String, nullable=False)
  pincode = db.Column(db.Integer)
  service = db.Column(db.String)
  experience = db.Column(db.Integer)
  active = db.Column(db.Boolean())
  fs_uniquifier = db.Column(db.String, unique=True, nullable=False)

  # User roles: Admin, Service Professional, Customer
  roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
  
  # Relationship for service requests
  customer_requests = db.relationship('ServiceReq', foreign_keys='ServiceReq.user_id', backref='customer')
  professional_requests = db.relationship('ServiceReq', foreign_keys='ServiceReq.professional_id', backref='professional')

class Role(db.Model, RoleMixin):
  __tablename__ = "role"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String)

class Services(db.Model):
  __tablename__ = "service"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  description = db.Column(db.String)
  price = db.Column(db.Integer, nullable=False)
  service_requests = db.relationship("ServiceReq", backref="service")
  # prof_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
  

class ServiceReq(db.Model):
  __tablename__ = "servicereq"
  id = db.Column(db.Integer, primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) #nullable until assigned to a professional
  service_status = db.Column(db.String, default='pending', nullable=False)
  user_status = db.Column(db.String, default='requested', nullable=False)
  date_of_request = db.Column(db.String, nullable=False)
  date_of_completion = db.Column(db.String, nullable=False)
  remarks = db.Column(db.String)



# class Section(db.Model):
#   __tablename__ = "section"
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String, nullable=False, unique=True)
#   date = db.Column(db.String, nullable=False)
#   description = db.Column(db.String)