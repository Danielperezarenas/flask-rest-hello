from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    subscription_date = db.Column(db.Date)

    def __repr__(self):
        return '<User: %r>' % self.email

    def serialize(self):
        return {"id": self.id,
                "email": self.email,
                "suscription_date": self.subscription_date,
                "is_active": self.is_active}


class Profiles(db.Model):
    __tablename__ = 'profiles'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    nickname =  db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    users = db.relationship(Users)
    
    def __repr__(self):
        return '<Profile: %r>' % self.firstname

    def serialize(self):
        return {"id": self.id, 
                "firstname": self.firstname,
                "lastname": self.lastname,
                "nickname": self.nickname,
                "image_url": self.img_url,
                "users_id": self.users_id}


class Address(db.Model):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each db.Column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(250))
    street_number = db.Column(db.String(250))
    post_code = db.Column(db.String(250), nullable=False)
    # 3.3 One to Many
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship(Users)

    def __repr__(self):
        return '<Address: %r>' % self.street_name % self.street_number

    def serialize(self):
        return {"id": self.id, 
                "street_name": self.street_name,
                "street_number": self.street_number,
                "post_code": self.post_code,
                "users_id": self.users_id}


class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    height = db.Column(db.String)
    mass = db.Column(db.String)
    hair_color = db.Column(db.String)
    skin_color = db.Column(db.String)
    eye_color = db.Column(db.String)
    birth_year = db.Column(db.String)
    gender = db.Column(db.String)
    homeworld = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return '<Character: %r>' % self.name

    def serialize(self):
        return {"id": self.id, 
                "name": self.name,
                "description": self.description,
                "height": self.height,
                "mass": self.mass,
                "hair_color": self.hair_color,
                "skin_color": self.skin_color,
                "eye_color": self.eye_color,
                "birth_year": self.birth_year,
                "gender": self.gender,
                "homeworld": self.homeworld,
                "url": self.url}


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    population = db.Column(db.Integer)
    climate = db.Column(db.String)
    terrain = db.Column(db.String)
    surface_water = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return '<Planet: %r>' % self.name

    def serialize(self):
        return {"id": self.id, 
                "name": self.name,
                "description": self.description,
                "diameter": self.diameter,
                "rotation_period": self.rotation_period,
                "orbital_period": self.orbital_period,
                "gravity": self.gravity,
                "population": self.population,
                "climate": self.climate,
                "terrain": self.terrain,
                "surface_water": self.surface_water,
                "url": self.url}


class FavoritesCharacters(db.Model):
    __tablename__ = 'favorites_characters'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    users = db.relationship(Users)
    characters = db.relationship(Characters)

    def __repr__(self):
        return '<Favorites Characters: %r>' % self.users_id % self.characters_id

    def serialize(self):
        return {"id": self.id, 
                "users_id": self.users_id,
                "characters_id": self.characters_id}


class FavoritesPlanets(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    users = db.relationship(Users)
    planets = db.relationship(Planets)

    def __repr__(self):
        return '<Favorites Planets: %r>' % self.users_id % self.planets_id

    def serialize(self):
        return {"id": self.id, 
                "users_id": self.users_id,
                "planets_id": self.planets_id}

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship(Users)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship(Planets)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    characters = db.relationship(Characters)

    def __repr__(self):
        return '<Favorites %r>' % self.id % self.user_id

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "planet_id": self.planet_id,
                "people_id": self.people_id}