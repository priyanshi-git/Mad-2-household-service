from flask_restful import Resource, Api, fields, reqparse, marshal_with
from flask_security import auth_required
from application.models import Books
from application.database import db

# Initialize the API with a prefix
api = Api(prefix='/api')

# Set up the parser for handling request data
parser = reqparse.RequestParser()
parser.add_argument('b_id', type=int, required=True, help="ID cannot be blank!")
parser.add_argument('b_title', type=str, required=True, help="Title cannot be blank!")
parser.add_argument('b_author', type=str, required=True, help="Author cannot be blank!")
parser.add_argument('description', type=str)
parser.add_argument('link', type=str)
parser.add_argument('b_section', type=str)

# Define the fields for marshalling the Book data
book_materials_fields = {
    'b_id': fields.Integer,
    'b_title': fields.String,
    'b_author': fields.String,
    'description': fields.String,
    'link': fields.String,
    'b_section': fields.String,
}

# Define the BookMaterials resource
class BookMaterials(Resource):
    @auth_required('token')
    @marshal_with(book_materials_fields)
    def get(self):
        all_resources = Books.query.all()
        return all_resources

    @auth_required('token')
    @marshal_with(book_materials_fields)
    def post(self):
        args = parser.parse_args()
        book = Books(
            b_id=args.b_id, 
            b_title=args.b_title, 
            b_author=args.b_author, 
            description=args.description, 
            link=args.link, 
            b_section=args.b_section
        )
        db.session.add(book)
        db.session.commit()
        return book, 201  # Return the created book object and HTTP 201 status code

# Add the BookMaterials resource to the API
api.add_resource(BookMaterials, '/books')
