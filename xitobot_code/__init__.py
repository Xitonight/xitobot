import logging
from telegram.ext import ApplicationBuilder, Defaults
from telegram.constants import ParseMode
from .config import Config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

TOKEN = Config.TOKEN

BASE_URL = Config.BASE_URL
BASE_FILE_URL = Config.BASE_FILE_URL

DB_URL = Config.DATABASE_URL
DB_NAME = Config.DATABASE_NAME
NOTES_COLL_NAME = Config.NOTES_COLLECTION_NAME
INLINE_CHATS_COLL_NAME = Config.INLINE_CHATS_COLLECTION_NAME

LOAD = Config.LOAD
NO_LOAD = Config.NO_LOAD

DEFAULTS = Config.BOT_DEFAULTS


application = ApplicationBuilder().defaults(DEFAULTS).base_url(BASE_URL).base_file_url(BASE_FILE_URL).token(TOKEN).build()