# mongo relatedMongoLogger
from pymongo import MongoClient
import urllib.parse

# init mongo connection
username = urllib.parse.quote_plus('dbUser')
password = urllib.parse.quote_plus("PwBhv72bEOq4NGlI")
url = "mongodb+srv://{}:{}@cluster0.edygp.mongodb.net/test?retryWrites=true&w=majority".format(username, password)
client = MongoClient(url)
db = client["traffic"]
mycol = db["traffic_data"]
env_file = None

class MongoLogger:
    def __init__(self):
        pass

    def log_data(self, data_dict: dict):
        data_dict["arg_file"] = env_file
        mycol.insert_one(data_dict)


def init_mongo_logger(envfile):
    global env_file
    env_file = envfile

