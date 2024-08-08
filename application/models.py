from .database import db, security
from flask_security import UserMixin, RoleMixin
from flask_security.models import fsqla_v3 as fsq

fsq.FsModels().set_db_info(db)

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('user', lazy='dynamic'))

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))

class Section(db.Model):
    __tablename__ = "section"
    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String, nullable=False, unique=True)
    s_date = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class Books(db.Model):
    __tablename__ = "books"
    b_id = db.Column(db.Integer, primary_key=True)
    b_title = db.Column(db.String, nullable=False, unique=True)
    b_author = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    link = db.Column(db.String, nullable=False)
    b_section = db.Column(db.String, nullable=False)

class Issues(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.b_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lib_status = db.Column(db.String, default='pending', nullable=False)
    user_status = db.Column(db.String, default='requested', nullable=False)
    book = db.relationship("Books", backref="issue")
    user = db.relationship("User", backref="issues")
    issued_on = db.Column(db.String, nullable=False)