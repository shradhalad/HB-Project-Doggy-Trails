from pprint import pprint
import os
from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Dog

app = Flask("__name__")

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

    db.session.add(new_user)
    db.session.commit()
    
    flash(f"Welcome {email}")
    return redirect("/login")








if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)