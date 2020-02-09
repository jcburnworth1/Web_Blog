##### https://github.com/schoolofcode-me/web_blog/blob/master/src/templates/base.html #####
## Import libraries
from flask import Flask, render_template, request, session, make_response
from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
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

    ## Validate user
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

@app.route('/blogs/new', methods=['POST', 'GET'])

def create_new_blog():
    """Allow user to create a new blog"""
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(author=user.email, title=title, description=description, author_id=user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    """Load posts from the selected blog"""
    blog = Blog.from_mongo(blog_id)

    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)

@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])

def create_new_post(blog_id):
    """Allow user to create a new post"""
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id=blog_id, title=title, content=content, author=user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

## If we are in main, execute the program
if __name__ == '__main__':
    app.run()