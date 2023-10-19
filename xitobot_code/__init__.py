import logging
from telegram.ext import ApplicationBuilder
from .config import Config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

TOKEN = Config.TOKEN
BASE_URL = Config.BASE_URL
BASE_FILE_URL = Config.BASE_FILE_URL
LOAD = Config.LOAD
NO_LOAD = Config.NO_LOAD

application = ApplicationBuilder().base_url(BASE_URL).base_file_url(BASE_FILE_URL).token(TOKEN).build()