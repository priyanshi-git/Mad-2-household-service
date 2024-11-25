from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_security import auth_required, roles_required, current_user
from flask import jsonify
from .models import Services, db

api = Api(prefix='/api')

# Parser for Book Resource
service_parser = reqparse.RequestParser()
service_parser.add_argument('name', type=str, help='name is required and should be a string', required=True)
service_parser.add_argument('description', type=str, help='description is required and should be a string', required=True)

service_parser.add_argument('price', type=str, help='price is required and should be a string', required=True)

# # Parser for Section Resource
# section_parser = reqparse.RequestParser()
# section_parser.add_argument('id', type=int, help='id is required and should be an integer', required=True)
# section_parser.add_argument('name', type=str, help='name is required and should be a string', required=True)
# section_parser.add_argument('date', type=str, help='date is required and should be a string', required=True)
# section_parser.add_argument('description', type=str, help='description is required and should be a string', required=True)

service_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Integer
}

# section_resource_fields = {
#     'id': fields.Integer,
#     'name': fields.String,
#     'date': fields.String,
#     'description': fields.String
# }


class Service_Resource(Resource):
    @marshal_with(service_resource_fields)
    def get(self):
        all_services = Services.query.all()
        return all_services

    @auth_required("token")
    @roles_required("admin")
    def post(self):
        args = service_parser.parse_args()  # Using service_parser here
        service = Services(id=args.get("id"), name=args.get("name"), description=args.get("description"), price=args.get("price"))
        db.session.add(service)
        db.session.commit()
        return {"message": "Service created"}, 201



# class Section_Resource(Resource):
#     @marshal_with(section_resource_fields)
#     def get(self):
#         all_sections = Section.query.all()
#         return all_sections

#     def post(self):
#         args = section_parser.parse_args()  # Using section_parser here
#         section = Section(**args)
#         db.session.add(section)
#         db.session.commit()
#         return {"message": "Section created"}, 201


api.add_resource(Service_Resource, '/services')
# api.add_resource(Section_Resource, '/section_resource')
