##### https://github.com/schoolofcode-me/web_blog/blob/master/src/templates/base.html #####
## Import libraries
from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.user import User

## Create the flask application
app = Flask(__name__) #'__main__'
app.secret_key = 'jose'

## Home Endpoint
@app.route('/')
def home_template():
    return render_template('home.html')

## Base Endpoint
@app.route('/login') ## http://127.0.0.1:5000/login

def login_template():
    """Load the login page"""
    return render_template('login.html')

## Base Endpoint
@app.route('/register') ## http://127.0.0.1:5000/register

def register_template():
    """Load the regsiter login page"""
    return render_template('register.html')

## Database Connection
@app.before_first_request
def initialize_database():
    Database.initialize()

## Login Endpoint
@app.route('/auth/login', methods=['POST'])

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

## Registration Endpoint
@app.route('/auth/register', methods=['POST'])

def register_user():
    """Capture the input email and password from the registration page"""
    ## Capture the user inputs
    email = request.form['email']
    password = request.form['password']

    User.register(email=email, password=password)

    return render_template('profile.html', email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')

def user_blogs(user_id=None):
    """Show user's blogs on navigation to the blogs page"""
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()


    return render_template('user_blogs.html', blogs=blogs, email=user.email)

## If we are in main, execute the program
if __name__ == '__main__':
    app.run()