## Import libraries
import uuid
import datetime
from src.common.database import Database
from src.models.post import Post

## Blog Class
class Blog(object):

    def __init__(self, author, title, description, _id=None):
        """Intialize the objet with an author, title, description, and id"""
        self.author = author
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        """Allows user to create a new post with title and content"""
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)

        post.save_to_mongo()

    def get_posts(self):
        """Retrieve posts associated with the given blog"""
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        """Save blog details to mongo blogs collection"""
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        """JSON model for our application to mongo"""
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        """Retrieve our data from mongo based on supplied post id"""
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})

        return cls(**blog_data) # Simplified the elements to match between post and database
