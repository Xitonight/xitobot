import pymongo as db

CLIENT = db.MongoClient("mongodb://localhost:27017/")
DB = CLIENT["xitobot"]
db_list = CLIENT.list_database_names()
if "xitobot" in db_list:
    print("Found 1 or more results for xitobot")
