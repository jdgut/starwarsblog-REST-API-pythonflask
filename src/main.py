"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.route('/users')
def handle_users():
    users = list(map(lambda user: user.serialize(), User.query.filter_by(is_active=1).all())) 
    return jsonify(users), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET', 'POST'])
def handle_user_favorites(user_id):
    # get only the ones named "Joe"
    favorites_query = Favorite.query.filter_by(user_id=user_id).all()

    if len(favorites_query) == 0:
        return jsonify({'error' : f'No favorites assigned to user_id {user_id}'}), 404

    # map the results and your list of people  inside of the all_people variable
    favorites = list(map(lambda favorite: favorite.serialize(), favorites_query))

    return jsonify(favorites), 200


@app.route('/people')
def handle_people():
    people = list(map(lambda character: character.serialize(), People.query.all()))
    return jsonify(people), 200

@app.route('/people/<int:people_id>')
def handle_people_details(people_id):
    return 'people details'

@app.route('/planets')
def handle_planets():
    planets = list(map(lambda planet: planet.serialize(), Planet.query.all()))
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>')
def handle_planet_details(planet_id):
    return 'planet_details'

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def handle_delete_favorites(favorite_id):
    return 'delete_favorites'

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
