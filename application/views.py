from flask import current_app as app
from flask_security import auth_required, roles_required, roles_accepted
from flask_restful import fields, marshal
from .models import User, db, Services, Role
from flask import jsonify, request, render_template
from .sec import datastore
from werkzeug.security import check_password_hash, generate_password_hash

@app.get('/')
def home():
  return render_template('index.html')

@app.get('/professional')
@auth_required("token")
@roles_required("professional")
def activate_professional():
  return "Welcome professional"


@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def activate_admin():
  return "Welcome admin"


@app.get('/activate/user/<int:user_id>')
@auth_required("token")
@roles_required("admin")
def activate_genuser(user_id):
  user = User.query.get(user_id)
  if not user:
    return jsonify({"message":"User not found"}), 404

  user.active=True
  db.session.commit()
  return jsonify({"message":"User Activated"}), 200


@app.post('/user-login')
def user_login():
  data = request.get_json()
  email = data.get('email')
  if not email:
    return jsonify({"message" : "email not provided"}), 404

  user = datastore.find_user(email=email)

  if not user:
    return jsonify({"message" : "user not found"}), 404

  if check_password_hash(user.password, data.get("password")):
    return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})

  else:
    return jsonify({"message": "wrong password"}), 400


@app.post('/registeruser')
def register():
  data = request.get_json()
  email = data.get('email')
  name = data.get('name')
  password = data.get('password')
  pincode = data.get('pincode')
  role = "user"

  if not email or not name or not password or role not in ['user']:
    return jsonify({"message" : "Invalid Input"}), 400
  
  if datastore.find_user(email=email):
    return jsonify({"message" : "User already exists"}), 400
  
  if role == "user":
    active = True
  try:
    datastore.create_user(email = email, name = name, password = generate_password_hash(password), pincode = pincode, roles=[role], active=active)
    db.session.commit()
  except:
    print('Error while creating')
    db.session.rollback()
    return jsonify({'message' : 'Error while creating user'}), 408
  
  return jsonify({"message" : "User created successfully"}), 200


@app.post('/registerprofessional')
def registerp():
  data = request.get_json()
  email = data.get('email')
  name = data.get('name')
  password = data.get('password')
  pincode = data.get('pincode')
  service = data.get('service')
  experience = data.get('experience')
  role = "professional"

  if not email or not name or not password or role not in ['professional']:
    return jsonify({"message" : "Invalid Input"}), 400
  
  if datastore.find_user(email=email):
    return jsonify({"message" : "User already exists"}), 400
  
  if role == "professional":
    active = False
  try:
    datastore.create_user(email = email, name = name, password = generate_password_hash(password), pincode = pincode, roles=[role], service=service, experience=experience, active=active)
    db.session.commit()
  except:
    print('Error while creating')
    db.session.rollback()
    return jsonify({'message' : 'Error while creating user'}), 408
  
  return jsonify({"message" : "User created successfully"}), 200

user_fields = {
  "id": fields.Integer,
  "name": fields.String,
  "email": fields.String,
  "active": fields.Boolean,
  "service": fields.String,
  "experience": fields.Integer
}

@app.get('/get_users')
@auth_required("token")
@roles_required("admin")
def all_users():
  users = User.query.filter(User.roles.any(Role.name == "user")).all()
  if len(users) == 0:
    return jsonify({"message": "No User Found"}), 404
  return marshal(users, user_fields)


@app.get('/get_professionals')
@auth_required("token")
@roles_required("admin")
def all_professionals():
  try: 
    users = User.query.filter(User.roles.any(Role.name == "professional")).all()
    user_data = [{'id': user.id, 'name': user.name, 'active': user.active, 'experience': user.experience, 'service': user.service} for user in users]
    return user_data, 200
  except Exception as e:
      return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.get('/services')
@auth_required("token")
@roles_accepted("admin", "user")
def service_list():
    try:
        services = Services.query.all()
        services_data = [{'id': service.id, 'name': service.name, 'description': service.description, 'price': service.price}for service in services]
        return services_data, 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.get('/services/<int:service_id>')
@auth_required("token")
@roles_required("admin")
def service_get(service_id):
  try:
    service = Services.query.get(service_id)
    if not service:
      return jsonify({'message': 'Service not found'}), 404
    else:
      # Convert the service object to a dictionary
      service_data = {
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': service.price,
      }
      return jsonify(service_data), 200
  except Exception as e:
    return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.delete('/delete/services/<int:service_id>')
@auth_required("token")
@roles_required("admin")
def delete_service(service_id):
    try:
        service = Services.query.get(service_id)
        if not service:
          return jsonify({'message':'Service not found'}),404
        else:
            db.session.delete(service)
            db.session.commit()
            return jsonify({'message': 'Section deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.delete('/delete/professional/<int:user_id>')
@auth_required("token")
@roles_required("admin")
def delete_prof(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
          return jsonify({'message':'User not found'}),404
        else:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.put('/update_service/<int:service_id>')
@auth_required('token')
@roles_required('admin')
def edit_service(service_id):
  # Fetch the service from the database
  service = Services.query.get(service_id)
  if not service:
    return jsonify({'message': 'Service not found'}), 404

  # Parse request data
  data = request.get_json()
  if not data:
    return jsonify({'message': 'No data provided'}), 400

  # Update fields if provided
  new_name = data.get('name')
  new_description = data.get('description')
  new_price = data.get('price')

  if new_name:
    service.name = new_name
  if new_description:
    service.description = new_description
  if new_price:
    try:
      service.price = float(new_price)  # Ensure price is a valid number
    except ValueError:
      return jsonify({'message': 'Price must be a number'}), 400

  # Commit changes
  try:
    db.session.commit()
    return jsonify({"message": "Service updated successfully"}), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
