from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ParseMode
from xitobot_code import application
from xitobot_code.modules.tool_modules.get_type import get_note_type
from xitobot_code.modules.db_modules.notes_db import add_note_to_db, list_all, clear_all_notes

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    note_name, text, data_type, content = get_note_type(update.effective_message)

    if note_name == None:
        await update.effective_message.reply_text("Please insert a nome for the note.")
    elif not update.effective_message.reply_to_message and data_type == None:
        await update.effective_message.reply_text("Please provide some content for the note.")
    else:
        await update.effective_message.reply_text(f"Saved {note_name}.")
        await add_note_to_db(chat_id, note_name, text, data_type, content)


async def get_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    notes_list = list_all(chat_id)
    if notes_list:
        filtered_list = "\n".join([str("- "+document["name"]) for document in notes_list])
        final_list = f"List of all notes in {chat_name}:\n\- "+filtered_list
    else:
        final_list = f"I didn't find any note to show in {chat_name}\."
    await context.bot.send_message(chat_id, final_list, parse_mode=ParseMode.MARKDOWN_V2)

async def del_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    deleted = clear_all_notes(chat_id)
    if deleted == -1:
        await update.effective_message.reply_text(f"There aren't any notes to delete in {chat_name}\.", parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await update.effective_message.reply_text(f"Deleted {deleted} notes from {chat_name}\.", parse_mode=ParseMode.MARKDOWN_V2)


save_handler = CommandHandler("save", save)
get_all_notes_handler = CommandHandler("notes", get_all_notes)
del_all_notes_handler = CommandHandler("clearnotes", del_all_notes)

application.add_handler(save_handler)
application.add_handler(get_all_notes_handler)
application.add_handler(del_all_notes_handler)