## Import libraries
from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.user import User

## Create the flask application
app = Flask(__name__) #'__main__'
app.secret_key = 'jose'

## Base endpoint to
@app.route('/') # www.mysite.com/api/ - Empty endpoint that will run the below

def hello_method():
    """Load the intial login page"""
    return render_template('login.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

## Setup Login endpoint
@app.route('/login', methods=['POST'])

def login_user():
    """Capture the input email and password from the login page"""
    ## Capture the user inputs
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template('profile.html', email=session['email'])

## If we are in main, execute the program
if __name__ == '__main__':
    app.run()