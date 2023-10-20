class Config(object):
    LOGGER = True

    TOKEN = "your token"
    BASE_FILE_URL = "your base file url (http://localhost:8081/file/bot if you're hosting the API on the same machine as the bot)"
    BASE_URL = "your base url"

    DATABASE_URL = "your database url"

    OWNER_ID = "your id"
    OWNER_USERNAME = "your username"

    LOAD = []
    NO_LOAD = ["echo"]