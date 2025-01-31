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
from models import db, Users, Characters, Planets, FavoritesCharacters, FavoritesPlanets, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        response_body = {}
        results = {}
        users = db.session.execute(db.select(Users)).scalars()
        list_users = []
        for row in users:
            list_users.append(row.serialize())
        results['users'] = list_users
        # Opción 2 - List Comprehesion
        # results['users'] = [row.serialize() for row in users]
        response_body['message'] = 'Listado de Usuarios'
        response_body['results'] = results
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        response_body = {}
        # Escribir la lógica para guardar el registro en la DB
        user = Users(email = data.get('email'),
                     password = data.get('password'),
                     is_active = True)
        db.session.add(user)
        db.session.commit()
        response_body['user'] = user.serialize()
        return response_body, 200
    

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    response_body = {}
    results = {}
    if request.method == 'GET':
        user = db.session.get(Users, user_id)
        if not user:
            response_body['message'] = 'Usuario no existe'
            return response_body, 404
        results['user'] = user.serialize()
        response_body['message'] = 'Usuario encontrado'
        response_body['results'] = results
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if not user:
            response_body['message'] = 'Usuario no existe'
            return response_body, 404
        user.email = data.get('email')
        db.session.commit()
        results['user'] = user.serialize()
        response_body['message'] = 'Usuario actualizado'
        response_body['results'] = results
        return response_body, 200
    if request.method == 'DELETE':
        user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
        if not user:
            response_body['message'] = 'Usuario no existe'
            return response_body, 404
        db.session.delete(user)
        db.session.commit()
        response_body['message'] = 'Usuario eliminado'
        return response_body, 200


@app.route('/people', methods=['GET'])
def handle_characters():
    response_body = {}
    results = {}
    characters = db.session.execute(db.select(Characters)).scalars()
    list_characters = []
    for row in characters:
        list_characters.append(row.serialize())
    results['characters'] = list_characters
    response_body['message'] = 'Listado de Personajes'
    response_body['results'] = results
    return response_body, 200
    

@app.route('/people/<int:characters_id>', methods=['GET'])
def handle_character(characters_id):
    response_body = {}
    results = {}
    character = db.session.get(Characters, characters_id)
    if not character:
        response_body['message'] = 'Personaje no existe'
        return response_body, 404
    results['character'] = character.serialize()
    response_body['message'] = 'Personaje encontrado'
    response_body['results'] = results
    return response_body, 200


@app.route('/planets', methods=['GET'])
def handle_planets():
    response_body = {}
    results = {}
    planets = db.session.execute(db.select(Planets)).scalars()
    list_planets = []
    for row in planets:
        list_planets.append(row.serialize())
    results['planets'] = list_planets
    response_body['message'] = 'Listado de Planetas'
    response_body['results'] = results
    return response_body, 200
    

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_one_planet(planet_id):
    response_body = {}
    results = {}
    planets = db.session.get(Planets, planet_id)
    if not planet:
        response_body['message'] = 'Planeta no existe'
        return response_body, 404
    results['planet'] = planet.serialize()
    response_body['message'] = 'Planeta encontrado'
    response_body['results'] = results
    return response_body, 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_user_favorites(user_id):
    response_body = {}
    results = {}
    favorites = db.session.execute(db.select(Favorites).where(Favorites.id == user_id)).scalar()
    if not user_id:
        response_body['message'] = 'Usuario no existe'
        return response_body, 404
    results['favorites'] = favorites
    response_body['message'] = 'Lista de favoritos'
    response_body['results'] = results
    return response_body, 200


# @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
# def handle_favorites_planets(user_id):
#     data = request.json
#     response_body = {}
#     # Escribir la lógica para guardar el registro en la DB
#     favorite_planet = planet_id.serialize()
#     db.session.add(favorite)
#     db.session.commit()
#     response_body['user'] = user.serialize()
#     return response_body, 200

#     favorites = Favorites.query.filter_by(user_id == id).all()
#     list_favorites = []
#     for row in favorites:
#         list_favorites.append(row.serialize())
#     if not user_id:
#         response_body['message'] = 'Usuario no existe'
#         return response_body, 404
#     results['favorites'] = list_favorites
#     response_body['message'] = 'Lista de favoritos'
#     response_body['results'] = results
#     return response_body, 200
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
