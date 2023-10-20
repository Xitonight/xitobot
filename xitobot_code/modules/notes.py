from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ParseMode
from xitobot_code import application
from xitobot_code.modules.tool_modules.get_type import get_message_type
from xitobot_code.modules.db_modules.notes_db import add_note_to_db

async def save(update: Update, context: ContextTypes):
    chat_id = update.effective_chat.id
    msg = update.effective_message

    note_name, text, data_type, content = get_message_type(msg)
    await add_note_to_db(chat_id, note_name, text, data_type, content)

async def get_all_notes(update: Update, context: ContextTypes):
    pass

save_handler = CommandHandler("save", save)
application.add_handler(save_handler)
