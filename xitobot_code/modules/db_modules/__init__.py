import pymongo as mongo
from ... import DB_URL, LOGGER

CLIENT = mongo.MongoClient(DB_URL)
DB = CLIENT["xitobot"]
db_list = CLIENT.list_database_names()

