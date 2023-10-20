class Config(object):
    LOGGER = True

    TOKEN = "your token" #get this from https://t.me/BotFather

    BASE_FILE_URL = "API base file url (http://localhost:8081/file/bot if you're hosting the API on the same machine as the bot)"
    BASE_URL = "API base url"

    DATABASE_URL = "your database url"
    DATABASE_NAME = "name of your choice"
    NOTES_COLLECTION_NAME = "collection name of your choice"

    OWNER_ID = "your id"
    OWNER_USERNAME = "your username"

    LOAD = []
    NO_LOAD = ["echo"]