import logging
from telegram.ext import ApplicationBuilder
from .config import Config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

TOKEN = Config.API_KEY
BASE_URL = Config.BASE_URL
BASE_FILE_URL = Config.BASE_FILE_URL
LOAD = Config.LOAD
NO_LOAD = Config.NO_LOAD

application = ApplicationBuilder().base_url(Config.BASE_URL).base_file_url(Config.BASE_FILE_URL).token(Config.API_KEY).build()