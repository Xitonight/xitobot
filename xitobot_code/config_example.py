from telegram.constants import ParseMode
from telegram.ext import Defaults

class Config(object):
    LOGGER = True

    TOKEN = "your token" #get this from https://t.me/BotFather

    BASE_FILE_URL = "API base file url"     #if you don't know what any of this means just leave it blank
    BASE_URL = "API base url"           #and remember not to include them in the __init__ when you build the application

    DATABASE_URL = "your database url"
    DATABASE_NAME = "name of your choice"
    NOTES_COLLECTION_NAME = "collection name of your choice"

    OWNER_ID = "your id"
    OWNER_USERNAME = "your username"

    BOT_DEFAULTS = Defaults(parse_mode=ParseMode.MARKDOWN_V2)   #you can set defaults so you won't have to type them all over

    LOAD = []
    NO_LOAD = [""]