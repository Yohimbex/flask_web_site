from flask_restful import Api, Resource, reqparse
from flask import make_response, jsonify
from flask import current_app

from app.main.models import User

# /api/v1/users
# GET = all_users 200
# POST = add user 201
# PUT = update_users 204
# DELETE = delete_all_users 204

class Users(Resource):
    """API for users"""
    def __init__(self):
        self.users = None
        self.request = None
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('email', type=str, required=True, location='json')
        self.regparse.add_argument('name', type=str, required=False, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self):
        """HTTP method GET"""
        self.users = User.select()
        self.users = self.prepare_users_to_json()
        return make_response(jsonify(self.users), 200)

    def post(self):
        """HTTP method POST"""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.title()
        user = User.select().where(User.email == self.request.email)
        if user:
            response = {'message': f'{self.request.email} is already in database.'}
            return make_response(jsonify(response), 200)
        user = User(
            name=self.request.name,
            email=self.request.email
        )
        user.save()
        return make_response('', 201)

    def put(self):
        """HTTP method PUT"""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.title()
        if not self.request.id:
            response = {'message': 'The id field is necessary.'}
            return make_response(jsonify(response), 200)
        user = User.select().where(User.id == self.request.id).first()
        if not user:
            response = {'message': f'User with id {self.request.id} did not found in database.'}
            return make_response(jsonify(response), 200)
        user.name = self.request.name
        user.email = self.request.email
        user.save()
        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE"""
        User.delete().execute()
        return make_response('', 204)

    def prepare_users_to_json(self):
        """Prepare cities to json format"""
        users = []
        for user in self.users:
            user_temp = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
            users.append(user_temp)

        return users


def init_app(app):
    with app.app_context():
        api = Api(app, decorators=[current_app.config['CSRF'].exempt])
        api.add_resource(Users, '/api/v1/users')
