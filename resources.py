from flask_restful import Resource, Api, fields, reqparse, marshal_with
from flask_security import auth_required
from application.models import Books
from application.database import db

api = Api(prefix='/api')

parser = reqparse.RequestParser()



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

  def post(self):
    args = parser.parse_args()
    book = Books(**args)
    db.session.add(book)
    db.session.commit()
    return {'message' : 'resources created'}, 200

api.add_resource(Books, '/books')