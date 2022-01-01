from pprint import pprint
import os
import ipdb
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Dog

app = Flask("__name__")

app.secret_key = "thisisnotthesecretkey"


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
    #ipdb.set_trace()
    #Get form variables and add user to database.
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(email=email, password=password)


    user = User.query.filter_by(email=email).first()
    
    if not user:
        db.session.add(new_user)
        db.session.commit()
    
    flash(f"Welcome {email}")
    return render_template("user_profile.html")


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
    return redirect("/user-profile")


@app.route('/login', methods = ['POST'])
def complete_login():
    """Log user in."""
    
    #Get variables from form and log user in to app.
    email = request.form["email"]
    password = request.form["password"]

    check_user(email, password)

@app.route('/POST_user_profile', methods = ['POST'])
def POST_user_profile():
    ipdb.set_trace()
    pass

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'









if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)