from model import db, User, Dog, connect_to_db


def create_user(email, user_id, user_name, password, zipcode):
    """Create and return a new user."""

    user = User(email=email, user_id=user_id, user_name=user_name, password=password, zipcode=zipcode)

    db.session.add(user)
    db.session.commit()

    return user

if __name__ == "__main__":
    from server import app

    connect_to_db(app)