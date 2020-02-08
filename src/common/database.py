## Import libraries
import pymongo

## Database Class
## Will create connection to Mongo for interactions
class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        """Connection to mongo and database: fullstack"""
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        """Insert record into fullstack"""
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        """Retrieve all results data from fullstack based on supplied query"""
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        """Retrieve first document in the query result"""
        return Database.DATABASE[collection].find_one(query)
