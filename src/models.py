from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250), nullable=False)
    location= db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    mass = db.Column(db.Integer(), nullable=False)
    hair_color = db.Column(db.String(120), nullable=False)
    skin_color = db.Column(db.String(120), nullable=False)
    eye_color  = db.Column(db.String(120), nullable=False)
    gender  = db.Column(db.String(120), nullable=False)
    birth_year  = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "height" : self.height,
            "mass" : self.mass,
            "hair_color" : self.hair_color,
            "skin_color" : self.skin_color, 
            "eye_color"  : self.eye_color,
            "gender" : self.gender,
            "birth_year"  : self.birth_year
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    rotation_period = db.Column(db.Integer(), nullable=False)
    orbital_period = db.Column(db.Integer(), nullable=False)
    diameter = db.Column(db.Integer(), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain  = db.Column(db.String(120), nullable=False)
    population  = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "rotation_period" : self.rotation_period,
            "orbital_period" : self.orbital_period,
            "diameter" : self.diameter,
            "climate" : self.climate, 
            "terrain"  : self.terrain,
            "population" : self.population
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=0)
    planet_id = db.Column(db.Integer, default=0)
    people_id = db.Column(db.Integer, default=0)



    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "planet_id" : self.planet_id,
            "people_id" : self.people_id
        }