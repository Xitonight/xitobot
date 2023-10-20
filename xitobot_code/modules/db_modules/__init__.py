import pymongo as mongo
from ... import DB_URL, DB_NAME, NOTES_COLL_NAME, LOGGER 

CLIENT = mongo.MongoClient(DB_URL)
DB = CLIENT[DB_NAME]
NOTES = DB[NOTES_COLL_NAME]
DB_LIST = CLIENT.list_database_names()

