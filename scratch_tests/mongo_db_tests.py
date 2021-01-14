from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
from urllib.parse import quote
from pymongo import MongoClient
import urllib.parse

username = urllib.parse.quote_plus('dbUser')
password = urllib.parse.quote_plus("PwBhv72bEOq4NGlI")

url = "mongodb+srv://{}:{}@cluster0.edygp.mongodb.net/test?retryWrites=true&w=majority".format(username, password)


client = MongoClient(url)
db = client["traffic"]
mycol = db["traffic_data"]

mydict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)