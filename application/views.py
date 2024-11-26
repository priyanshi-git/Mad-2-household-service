from flask import current_app as app
from flask_security import auth_required, roles_required, roles_accepted
from flask_login import current_user
from flask_restful import fields, marshal
from .models import User, db, Services, Role, ServiceReq
from flask import jsonify, request, render_template
from .sec import datastore
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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

@app.get('/service/<int:service_id>/professionals')
@auth_required("token")
@roles_accepted("user")
def get_service_professionals(service_id):
    try:
        # Ensure the service exists
        service = Services.query.get(service_id)
        if not service:
            return jsonify({'message': 'Service not found'}), 404

        # Find professionals associated with the service
        professionals = User.query.filter(
            User.service == service.name,  # Match service name
            User.active == True  # Only active professionals
        ).all()

        # Serialize the data
        professionals_data = [
            {
                'id': prof.id,
                'name': prof.name,
                'experience': prof.experience,
                'email': prof.email
            }
            for prof in professionals
        ]

        return jsonify(professionals_data), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500




@app.post('/service/<int:service_id>/book')
@auth_required("token")
@roles_accepted("user")
def book_service(service_id):
    try:
        # Validate that the service exists
        service = Services.query.get(service_id)
        if not service:
            return jsonify({'message': 'Service not found'}), 404

        # Get the authenticated user
        user = current_user

        # Parse request data for professional ID
        data = request.json
        professional_id = data.get("professional_id")


        # Check if the user already has a pending request for the service
        existing_request = ServiceReq.query.filter_by(service_id=service_id, user_id=user.id, service_status='pending').first()
        if existing_request:
            return jsonify({'message': 'You already have a pending request for this service.'}), 400

        # Create a new service request
        new_request = ServiceReq(
            service_id=service_id,
            professional_id=professional_id,
            service_status="Pending",
            user_status="Requested",
            user_id=user.id,
            date_of_request=datetime.now().strftime('%Y-%m-%d'),
            date_of_completion="",
            remarks="",
        )
        db.session.add(new_request)
        db.session.commit()

        return jsonify({'message': 'Service booked successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.get('/user/service-requests')
@auth_required("token")
@roles_accepted("user")
def get_user_service_requests():
    try:
        # Get the authenticated user
        user = current_user

        # Query the ServiceReq table for the logged-in user's service requests
        service_requests = (
            db.session.query(ServiceReq, Services, User)
            .join(Services, ServiceReq.service_id == Services.id)
            .join(User, ServiceReq.professional_id == User.id)
            .filter(ServiceReq.user_id == user.id)
            .all()
        )

        # Format the results
        result = [
            {
                "service_name": request.Services.name,
                "professional_name": request.User.name,
                "date_requested": request.ServiceReq.date_of_request,
                "user_status": request.ServiceReq.user_status,
            }
            for request in service_requests
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



