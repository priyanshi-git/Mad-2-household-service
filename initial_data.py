from main import app
from application.sec import datastore
from application.models import db, Role
from werkzeug.security import generate_password_hash

with app.app_context():
  db.create_all()
  datastore.find_or_create_role(name="admin", description="user is a admin")
  datastore.find_or_create_role(name="user", description="user is a general user")
  datastore.find_or_create_role(name="professional", description="user is a service professional")
  db.session.commit()


  if not datastore.find_user(email="admin@iitm.ac.in"):
    datastore.create_user(email="admin@iitm.ac.in", password=generate_password_hash('adminpass'), roles=['admin'])
  if not datastore.find_user(email="user1@iitm.ac.in"):
    datastore.create_user(email="user1@iitm.ac.in", password=generate_password_hash('user1pass'), pincode="110033", name="user1", roles=['user'], active=False)
  if not datastore.find_user(email="professional@iitm.ac.in"):
    datastore.create_user(email="professional@iitm.ac.in", password=generate_password_hash('professionalpass'), pincode="110033", service="Plumbing", experience="1", name="professional 1", roles=['professional'], active=False)
  
  db.session.commit()







  # libr = Role(id='librarian', name='Librarian', description='the maintainer of sections and e-books in the library')
  # db.session.add(libr)
  # genuser = Role(id='genuser', name='General User', description='an individual who wants to access an e-book from the library')
  # db.session.add(genuser)
  # db.session.commit()