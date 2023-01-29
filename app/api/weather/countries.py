from flask_restful import Api, Resource, reqparse
from flask import make_response, jsonify
from flask import current_app

from app.weather.models import City, Country

# /api/v1/countries
# GET = all_cities 200
# POST = add country 201
# PUT = update_countries 204
# DELETE = delete_selected_countries 204

class Countries(Resource):
    """API for countries"""
    def __init__(self):
        self.cities = None
        self.countries = None
        self.request = None
        self.api_key = current_app.config['WEATHER_API_KEY']
        self.regparse = reqparse.RequestParser()
        self.regparse.add_argument('name', type=str, required=True, location='json')
        self.regparse.add_argument('code', type=str, required=False, location='json')
        self.regparse.add_argument('id', type=int, required=False, location='json')

    def get(self):
        """HTTP method GET"""
        self.countries = Country.select()
        self.countries = self.prepare_countries_to_json()
        return make_response(jsonify(self.countries), 200)

    def post(self):
        """HTTP method POST"""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.title()
        self.request.code = self.request.code.upper()
        country = Country.select().where(Country.name == self.request.name, Country.code == self.request.code)
        if country:
            response = {'message': f'{self.request.name} is already in database.'}
            return make_response(jsonify(response), 200)
        country = Country(
            code=self.request.code,
            name=self.request.name
        )
        country.save()
        return make_response('', 201)

    def put(self):
        """HTTP method PUT"""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.title()
        self.request.code = self.request.code.upper()
        if not self.request.id:
            response = {'message': 'This field id is necessary.'}
            return make_response(jsonify(response), 200)
        country = Country.select().where(Country.id == self.request.id).first()
        if not country:
            response = {'message': f'Country with id {self.request.id} did not found in database.'}
            return make_response(jsonify(response), 200)
        country.name = self.request.name
        country.code = self.request.code
        country.save()
        return make_response('', 204)

    def delete(self):
        """HTTP method DELETE"""
        self.request = self.regparse.parse_args()
        self.request.name = self.request.name.capitalize()
        self.request.code = self.request.code.upper()
        Country[self.request.id].delete_instance()
        return make_response('', 204)

    def prepare_countries_to_json(self):
        """Prepare cities to json format"""
        countries = []
        for country in self.countries:
            country_temp = {
                'id': country.id,
                'code': country.code,
                'name': country.name
            }
            countries.append(country_temp)

        return countries


def init_app(app):
    with app.app_context():
        api = Api(app, decorators=[current_app.config['CSRF'].exempt])
        api.add_resource(Countries, '/api/v1/countries')
