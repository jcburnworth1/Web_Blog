## Import libraries
from flask import session
from src.common.database import Database
import uuid
from src.models.blog import Blog
import datetime

## User Class
class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        """Search the database for a user by their email"""
        data = Database.find_one(collection='users',
                                 query={'email': email})

        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        """Search the database for a user by their _id"""
        data = Database.find_one(collection='users',
                                 query={'_id': _id})

        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        """Check if password is correct or not"""
        user = User.get_by_email(email)

        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        """Register a new user into mongo"""
        user = cls.get_by_email(email)

        if user is None:
            ## User doesn't exists
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
        else:
            ## User already exists
            return True

    @staticmethod
    def login(user_email):
        """Authenticate a new user into the application"""
        ## Login valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        """Logout the user and clear the session email"""
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        """Create a new blog and save to mongo"""
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        """Create a new post and save to mongo"""
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        """JSON model for our application to mongo"""
        return {
            'email': self.email,
            '_id': self._id,
            'password': self.password
        }

    def save_to_mongo(self):
        """Save new user to mongo users collection"""
        Database.insert(collection='users',
                        data=self.json())
