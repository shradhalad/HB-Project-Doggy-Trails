from pprint import pprint
import os
import cloudinary.uploader
import ipdb
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask import make_response
from flask_sqlalchemy_session import current_session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Dog
from base64 import b64encode
import base64
from io import BytesIO #Converts data from Database into bytes
from app_settings import get_app
from model import add_geocoding_data

app = get_app()
app.secret_key = "thisisnotthesecretkey"

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "hbproject"


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/signup', methods = ['GET'])
def signup_form():
    """Show signup form to user to sign up to access more features."""

    return render_template("signup.html")

@app.route('/signup', methods = ['POST'])
def complete_signup():
    """Process user's signup to app"""
    #Get form variables and add user to database.

    email = request.form["email"]
    password = request.form["password"]

    new_user = User(email=email, password=password)

    user = User.query.filter_by(email=email).first()
    
    
    if not user:
        add_geocoding_data(new_user)
        db.session.add(new_user)
        db.session.commit()
        user = new_user
    
    flash(f"Welcome {email}")
    resp = make_response(render_template("user_profile.html", user=user))
    resp.set_cookie('user_id', str(user.user_id).encode())
    resp.set_cookie('user_email', str(user.email).encode())

    return resp


@app.route('/login', methods = ['GET'])
def login_form():
    """Show login form to user."""
    
    return render_template("login_form.html")


def check_user(email, password):

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Please sign up to be able to login.")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash("Logged in")
    resp = redirect("/user-profile")
    resp.set_cookie('user_id', user.user_id)

    return resp



@app.route('/login', methods = ['POST'])
def complete_login():
    """Log user in."""
    
    #Get variables from form and log user in to app.
    email = request.form["email"]
    password = request.form["password"]
    
    return check_user(email, password)

    


def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

@app.route('/POST_user_profile', methods = ['POST'])
def POST_user_profile():
    
    user_image = request.files["user_image"]
    user_name = request.form["user_name"]
    zipcode = request.form["zipcode"]
    address = request.form["address"]

    dog_image = request.files["dog_image"]
    dog_name = request.form["dog_name"]
    breed = request.form["breed"]
    gender = request.form["gender"]
    age = request.form["age"]

    # print(request.form.keys())
    # print(request.files.keys())

    update_user_id = request.cookies.get('user_id')
    print(repr(update_user_id))
    user = User.query.filter_by(user_id=int(update_user_id)).first()
    if user is None:
        redirect ('/signup')
    user.user_image = user_image.read()
    user_image.stream.seek(0)
    user.user_name = user_name
    user.zipcode = zipcode
    user.address = address

    result = cloudinary.uploader.upload(user_image, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    img_url = result['secure_url']

    add_geocoding_data(user)
    db.session.commit() 


    newFile_dog = Dog(dog_image=dog_image.read(), dog_name=dog_name, breed=breed, gender=gender, age=age)
    db.session.add(newFile_dog)
    db.session.commit() 

    return redirect ('/search')
    


@app.route('/search', methods = ['GET'])
def search():

    return render_template('search.html')


@app.route("/search_api",methods = ['GET'])
def search_api():
    args = request.args
    zipcode = args.get("zipcode")
    result = {}
    filtered_user = User.query.filter_by(zipcode=zipcode)
    result['users'] = []
    for user in filtered_user:
        result['users'].append({
            'name': user.user_name,
            'zipcode': user.zipcode,
            'email': user.email,
            'address': user.address,
            'lat': user.latitude,
            'lng': user.longitude,
        })

        
    return result

@app.route('/message_board', methods = ['GET'])
def message_board():
    """Show message board to user."""
    
    return render_template("message_board.html")


@app.route('/logout')
def logout():
    """Log out."""
    
    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")






if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)