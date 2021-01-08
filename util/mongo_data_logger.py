# mongo relatedMongoLogger
from pymongo import MongoClient
import urllib.parse
import uuid

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
        self.server_uuid = self.get_server_uuid()

    def log_data(self, data_dict: dict):

        data_dict["computer_id"] = self.server_uuid
        data_dict["arg_file"] = env_file
        mycol.insert_one(data_dict)

    def get_server_uuid(self):
        computer_id = uuid.UUID(int=uuid.getnode())
        return computer_id



def init_mongo_logger(envfile):
    global env_file
    env_file = envfile

