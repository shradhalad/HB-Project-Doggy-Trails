from pprint import pprint
import os


from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Dog


app = Flask(__name__)

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/signup')
def signup():
    """View signup."""

    return render_template('signup.html')








if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)