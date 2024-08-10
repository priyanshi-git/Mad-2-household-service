from flask import render_template_string, render_template, Flask, request, jsonify
from flask_security import auth_required, current_user, roles_required, verify_password
from flask_security import SQLAlchemySessionUserDatastore
from flask_security.utils import hash_password
from application.database import db

def create_view(app : Flask, user_datastore : SQLAlchemySessionUserDatastore, db ):

    # homepage
    @app.route('/')
    def home():
        return render_template('index.html') # entry point to vue frontend

    @app.route('/user-login', methods=['POST'])
    def user_login():

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')


        if not email or not password:
            return jsonify({'message' : 'not valid email or password'}), 404

        user = user_datastore.find_user(email = email)

        if not user:
            return jsonify({'message' : 'invalid user'}), 404

        if verify_password(password, user.password):
            return jsonify({
                'token' : user.get_auth_token(),
                'role' : user.roles[0].name,
                'id' : user.id,
                'email' : user.email
            }), 200


    # profile
    @app.route('/profile')
    @auth_required('token')
    def profile():
        return render_template_string(
            """
                <h1> this is profile page </h1>
                <p> Welcome, {{current_user.email}}</p>
                <p> Role :  {{current_user.roles[0].description}}</p>
                <p><a href="/logout">Logout</a></p>
            """
        )

    @app.route('/register', methods=['POST'])
    def register():

        data = request.get_json()
        

        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
 

        if not email or not password or not role:
            return jsonify({'message' : 'invalid input'}), 403

        if user_datastore.find_user(email = email ):
            return jsonify({'message' : 'user already exists'}), 400
        
        if role == 'genuser':
            user_datastore.create_user(name = name, email = email, password = hash_password(password), active = 0, roles=[role]), 201
            db.session.commit()
            return jsonify({'message' : 'User successfully created'})
        
        return jsonify({'message' : 'invalid role'}), 400


    @app.route('/inst-dashboard')
    @roles_required('inst')
    def inst_dashboard():
        return render_template_string(
            """
                <h1>this is instructor dashboard</h1>
                <p>This should only be accessible to inst</p>
            """
        )
    
    @app.route('/stud-dashboard')
    @roles_required('stud')
    def stud_dashboard():
        return render_template_string(
            """
                <h1>this is student dashboard</h1>
                <p>This should only be accessible to student</p>
            """
        )