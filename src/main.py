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

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/create-token", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email=email, password=password).first()

    newVariable = "this is a string"

    if user is None:
        raise APIException('Invalid Email/Password', status_code=401)

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    return jsonify(user_id=current_user_id), 200

@app.route("/user", methods=['POST'])
def create_user():
    user_id = 100
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 200


@app.route('/users')
def handle_users():
    users = list(map(lambda user: user.serialize(), User.query.filter_by(is_active=1).all())) 
    return jsonify(users), 200

@app.route('/users/favorites', methods=['GET', 'POST'])
def handle_user_favorites(user_id):

    if request.post:
        posted_data = request.get_json()

        if planet_id in posted_data:
            planet_id = posted_data['planet_id']

        if people_id in posted_data:
            people_id = posted_data['people_id']

    favorites = list(map(lambda favorite: favorite.serialize(), Favorite.query.filter_by(user_id=user_id).all()))
    if not favorites:
       raise APIException('No favorites assigned', status_code=404)

    # map the results and your list of people  inside of the all_people variable
    favorites = list(map(lambda favorite: favorite.serialize(), favorites_query))

    return jsonify(favorites), 200

@app.route('/people')
def handle_people():
    people = list(map(lambda character: character.serialize(), People.query.all()))
    return jsonify(results=people), 200

@app.route('/people/<int:people_id>')
def handle_people_details(people_id):
    #character = People.query.filter_by(id=people_id).first_or_404()
    character = People.query.filter_by(id=people_id).first()
    if not character:
         raise APIException('Character not found', status_code=404)

    return jsonify(character.serialize()), 200

@app.route('/planets')
def handle_planets():
    planets = list(map(lambda planet: planet.serialize(), Planet.query.all()))
    return jsonify(results=planets), 200

@app.route('/planets/<int:planet_id>')
def handle_planet_details(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    if not planet:
        raise APIException('Planet not found', status_code=404)

    return jsonify(planet.serialize()), 200

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def handle_delete_favorites(favorite_id):
    favorite = Favorite.query.filter_by(id=favorite_id).first()

    if not favorite:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()

    return jsonify(''), 204
    
   

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
