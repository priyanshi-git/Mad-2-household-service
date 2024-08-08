from flask_security.utils import hash_password

def create_data(app, user_datastore):
    with app.app_context():
        print('### creating Data #####')

        #creating roles
        user_datastore.find_or_create_role(name='librarian', description="Librarian")
        user_datastore.find_or_create_role(name='genuser', description="General User")

        #creating user data
        if not user_datastore.find_user(email="librarian@iitm.ac.in"):
            user_datastore.create_user(name= "initial_name", email="librarian@iitm.ac.in", password=hash_password('pass'), active=True, roles=['librarian'])

        user_datastore.commit()