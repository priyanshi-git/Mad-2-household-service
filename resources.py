from flask_restful import Resource, Api, fields, reqparse, marshal_with
from flask_security import auth_required
from application.models import Books
from application.database import db

api = Api(prefix='/api')

parser = reqparse.RequestParser()

parser.add_argument('id', type=int)
parser.add_argument('b_title', type=str)
parser.add_argument('b_author', type=str)
parser.add_argument('description', type=str)
parser.add_argument('link', type=str)
parser.add_argument('b_section', type=str)

book_materials_fields = {
  'id' : fields.Integer,
  'b_title' : fields.String,
  'b_author' : fields.String,
  'description' : fields.String,
  'link' : fields.String,
  'b_section' : fields.String,
}

class BookMaterials(Resource):
  @auth_required()
  @marshal_with(book_materials_fields)

  def get(self):
    all_resources = Books.query.all()
    return all_resources

  @auth_required
  def post(self):
    args = parser.parse_args()
    book = Books(id = args.id, b_title = args.b_title, b_author = args.b_author, description = args.description, link = args.link, b_section = args.b_section)
    db.session.add(book)
    db.session.commit()
    return {'message' : 'resources created'}, 200

api.add_resource(Books, '/books')