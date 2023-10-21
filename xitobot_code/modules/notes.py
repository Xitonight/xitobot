from telegram import Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode
from xitobot_code import application, LOGGER
from xitobot_code.modules.tool_modules.get_info import get_note_type, Types
import xitobot_code.modules.db_modules.notes_db as notes_db

ASKING = 0

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    note_name, text, description, data_type, content = get_note_type(update.effective_message)
    note = [note_name, text, description, data_type, content]
    
    if note_name == "" and text == "":
        await update.effective_message.reply_text("Please insert a nome for the note.")
        return ConversationHandler.END
    
    if not update.effective_message.reply_to_message and data_type == None:
        await update.effective_message.reply_text("Please provide some content for the note.")
        return ConversationHandler.END
    
    if notes_db.check_existing_notes(chat_id, note_name):
        context.user_data["note"] = note
        await context.bot.send_message(chat_id, f"{note_name} is already saved.\nOverwrite it? (yes / no)")
        return ASKING
    else:
        notes_db.add_note_to_db(chat_id, note_name, text, description, data_type, content)
        await update.effective_message.reply_text(f"Saved {note_name}.")

async def overwrite_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.effective_message.text
    chat_id = update.effective_chat.id
    note_name, text, description, data_type, content = context.user_data["note"]
    
    if user_response == "yes":
        notes_db.update_note(chat_id, note_name, text, description, data_type, content)
        await context.bot.send_message(chat_id, f"Updated {note_name}.")

    elif user_response == "no":
        await context.bot.send_message(chat_id, "Canceling overwrite.")
    
    else:
        await context.bot.send_message(chat_id, "Please type 'yes' or 'no'.")
    
    return ConversationHandler.END

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if len(context.args)>1:
        await update.effective_message.reply_text("Please only provide the note's name.")
        return
    note_name = context.args[0]
    text, description, data_type, content = notes_db.get_note(chat_id, note_name)
    
    if data_type == Types.TEXT:
        await context.bot.send_message(chat_id, text)
    elif data_type == Types.STICKER:
        await context.bot.send_sticker(chat_id, content)
    elif data_type == Types.DOCUMENT:
        await context.bot.send_document(chat_id, content, text)
    elif data_type == Types.PHOTO:
        await context.bot.send_photo(chat_id, content, text)
    elif data_type == Types.AUDIO:
        await context.bot.send_audio(chat_id, content, caption=text)
    elif data_type == Types.VOICE:
        await context.bot.send_voice(chat_id, content, caption=text)
    elif data_type == Types.VIDEO:
        await context.bot.send_video(chat_id, content, caption=text)
    
async def get_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    notes_list = notes_db.list_all(chat_id)
    if notes_list:
        filtered_list = "\n".join([str("\- "+document["name"]) for document in notes_list])
        final_list = f"List of all notes in {chat_name}:\n"+filtered_list
    else:
        final_list = f"I didn't find any note to show in {chat_name}\."
    await context.bot.send_message(chat_id, final_list, parse_mode=ParseMode.MARKDOWN_V2)

async def del_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    deleted = notes_db.clear_all_notes(chat_id)
    if deleted == -1:
        await update.effective_message.reply_text(f"There aren't any notes to delete in {chat_name}\.", parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await update.effective_message.reply_text(f"Deleted {deleted} notes from {chat_name}\.", parse_mode=ParseMode.MARKDOWN_V2)

get_all_notes_handler = CommandHandler("notes", get_all_notes)
del_all_notes_handler = CommandHandler("clearnotes", del_all_notes)
get_handler = CommandHandler("get", get)

note_update_conversation_handler = ConversationHandler(
    entry_points = [CommandHandler("save", save)],
    states = {ASKING: [MessageHandler(filters.TEXT, overwrite_note)]},
    fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
)

application.add_handler(get_all_notes_handler)
application.add_handler(del_all_notes_handler)
application.add_handler(get_handler)
application.add_handler(note_update_conversation_handler)