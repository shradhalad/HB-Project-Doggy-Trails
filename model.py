from flask_sqlalchemy import SQLAlchemy
from app_settings import get_app

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import googlemaps


DB_URI = "postgresql:///project"
db = SQLAlchemy(get_app())
""" Model Definitions """

class User(db.Model):
    """User"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, unique=True, primary_key = True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable = False)
    zipcode = db.Column(db.Integer)
    address = db.Column(db.String(100))
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)
    user_image = db.Column(db.LargeBinary)
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.dog_id'), autoincrement = True)


    dog = db.relationship("Dog", backref="users", uselist=True)


    def __repr__(self):
        """Provide helpful information about user when printed."""

        return f'<User user_id={self.user_id} user_name={self.user_name} email={self.email} password= {self.password}>'

class Dog(db.Model):
    """Dog"""

    __tablename__ = "dogs"


    dog_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    breed = db.Column(db.String(50), nullable = False)
    dog_name = db.Column(db.String(50), nullable = False)
    gender = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    dog_image = db.Column(db.LargeBinary)

    
    

    def __repr__(self):
        """Provide helpful information about dogs when printed."""

        return f"<Class dog_id={self.dog_id} dog_name={self.dog_name}>"

def add_fake_data():
    engine = create_engine(DB_URI)
    INDEX_TO_ADDRESS_HOUSE_NUMBER = {
        0: 3708,
        1: 3714,
        2: 3720,
        3: 3711,
        4: 3717,
        5: 3809,
        6: 3815,
        7: 3820,
        8: 3825,
        9: 3836,
        10: 3844

    }
    with Session(engine) as session:
        for ii in range(10):
            an_user = User(
                email=f'user{ii}@gmail.com',
                password=f'pwd{ii}',
                user_name=f'user{ii}',
                zipcode='94403',
        address=f'{INDEX_TO_ADDRESS_HOUSE_NUMBER[ii]} Colegrove Street, San Mateo'

            )
            add_geocoding_data(an_user)
            session.add(an_user)
        session.commit()
    pass

def add_geocoding_data(user):
    """Adds in latitude and longitude to a user object."""

    gmaps_key = googlemaps.Client(key="AIzaSyAFB31etl8X7y0-VaeN4sA0xKUMnuS4ixg")
    if user.address is None:
        lat = -1
        lng = -1
    
    else:
        g = gmaps_key.geocode(user.address)
        lat = g[0]["geometry"]["location"]["lat"]
        lng = g[0]["geometry"]["location"]["lng"]
    user.latitude = lat
    user.longitude = lng
    return user


def connect_to_db(flask_app, db_uri=DB_URI, echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")
    return db

if __name__ == "__main__":

    connect_to_db(get_app())
