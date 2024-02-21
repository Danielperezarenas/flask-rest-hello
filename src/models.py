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


class FavoritesCharacters(db.Model):
    __tablename__ = 'favorites_characters'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    users = db.relationship(Users)
    characters = db.relationship(Characters)


class FavoritesPlanets(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    users = db.relationship(Users)
    planets = db.relationship(Planets)
