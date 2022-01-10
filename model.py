from flask_sqlalchemy import SQLAlchemy
from app_settings import get_app



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
    location = db.Column(db.String(50))
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
