from telegram import Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, ContextTypes, filters
from xitobot_code import application, LOGGER
from xitobot_code.tools.get_info import get_note_type, Types
import xitobot_code.database.notes_db as notes_db

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chat_id = update.effective_chat.id
    chat_has_inline = notes_db.check_existing_inline_chat(chat_id)
    chat_surname = None
    
    if chat_has_inline:
        chat_surname = notes_db.get_inline_surname(chat_id)
    
    note_name, text, description, data_type, file_id = get_note_type(update.effective_message)
    note = [note_name, text, description, data_type, file_id]

    if note_name == "" and text == "":
        await update.effective_message.reply_text("Please insert a nome for the note\.")
        return ConversationHandler.END
    
    if not update.effective_message.reply_to_message and text == "":
        await update.effective_message.reply_text("Please provide some content for the note\.")
        return ConversationHandler.END
    
    note_exists = notes_db.check_existing_note(note_name, chat_id)

    if note_exists:
        from xitobot_code.modules.conversations import OVERWRITE_NOTE
        context.user_data["note"] = note
        await context.bot.send_message(chat_id, f"{note_name} is already saved\.\nOverwrite it? \(yes / no\)")
        return OVERWRITE_NOTE
    else:
        notes_db.add_note_to_db(chat_id, chat_surname, note_name, text, description, data_type, file_id)
        await update.effective_message.reply_text(f"Saved {note_name}\.")

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE, hash_note: str = None):
    chat_id = update.effective_chat.id
    
    if hash_note is None:
        args = context.args
    else:
        args = hash_note.split(maxsplit=2)

    if len(args)>1 and not "-d" in args:
        await update.effective_message.reply_text("Please only provide the note's name\.")
        return
    elif len(args)>1 and "-d" in args:
        note_name = next(arg for arg in args if arg!="-d")
    else:
        note_name = args[0]

    note_exists = notes_db.check_existing_note(note_name, chat_id)

    if not note_exists:
        await update.effective_message.reply_text("There's no note with that name\.")
        return

    note_values = notes_db.get_note(note_name, chat_id)
    text, description, data_type, file_id = note_values

    if "-d" in args:
        text = text.join(f"\n\n*Description:*\n{description}")
    
    if data_type == Types.TEXT:
        await context.bot.send_message(chat_id, text)
    elif data_type == Types.STICKER:
        await context.bot.send_sticker(chat_id, file_id)
    elif data_type == Types.PHOTO:
        await context.bot.send_photo(chat_id, file_id, text)
    elif data_type == Types.DOCUMENT:
        await context.bot.send_document(chat_id, file_id, text)
    elif data_type == Types.GIF:
        await context.bot.send_animation(chat_id, file_id, caption=text)
    elif data_type == Types.AUDIO:
        await context.bot.send_audio(chat_id, file_id, caption=text)
    elif data_type == Types.VOICE:
        await context.bot.send_voice(chat_id, file_id, caption=text)
    elif data_type == Types.VIDEO:
        await context.bot.send_video(chat_id, file_id, caption=text)

async def hash_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    no_hash = update.effective_message.text[1:]
    await get(update, context, no_hash)

async def get_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    
    notes_in_chat = notes_db.check_any_note(chat_id)
    
    if not notes_in_chat:
        await update.effective_message.reply_text(f"There are no notes to show in {chat_name}.")
        return
    
    notes_list = notes_db.list_all(chat_id)
    filtered_list = "\n".join([str("\- "+document["name"]) for document in notes_list])
    final_list = f"List of all notes in {chat_name}:\n"+filtered_list
    
    await context.bot.send_message(chat_id, final_list)

async def delete_one_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if len(context.args)>1:
        await update.effective_message.reply_text("Please, only provide the note's name.")
        return
    
    note_name = context.args[0]
    note_exists = notes_db.check_existing_note(note_name, chat_id)
    
    if not note_exists:
        await update.effective_message.reply_text("There's no note with that name.")
        return
    
    notes_db.clear_note(chat_id, note_name)
    await update.effective_message.reply_text(f"Deleted {note_name}.")


async def delete_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name

    notes_in_chat = notes_db.check_any_note(chat_id)

    if not notes_in_chat:
        await update.effective_message.reply_text(f"There aren't any notes to delete in {chat_name}.")
        return
    
    deleted = notes_db.clear_all_notes(chat_id)
    await update.effective_message.reply_text(f"Deleted {deleted} notes from {chat_name}.")

#---HANDLERS CREATION

get_handler = CommandHandler("get", get)
hash_get_handler = MessageHandler(filters.Regex(r"^#[^\s]+"), hash_get)
get_all_notes_handler = CommandHandler("notes", get_all_notes)
delete_one_note_handler = CommandHandler("clear", delete_one_note)
delete_all_notes_handler = CommandHandler("clearNotes", delete_all_notes)

# the save handler is in conversations.py

application.add_handler(get_handler)
application.add_handler(hash_get_handler)
application.add_handler(get_all_notes_handler)
application.add_handler(delete_one_note_handler)
application.add_handler(delete_all_notes_handler)
