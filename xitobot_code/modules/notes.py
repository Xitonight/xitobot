from telegram import (
    Update,
    InlineQueryResultArticle,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedGif,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InputTextMessageContent
    )
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, InlineQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode
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
        await update.effective_message.reply_text("Please insert a nome for the note.")
        return ConversationHandler.END
    
    if not update.effective_message.reply_to_message and text == "":
        await update.effective_message.reply_text("Please provide some content for the note.")
        return ConversationHandler.END
    
    note_exists = notes_db.check_existing_note(note_name, chat_id)

    if note_exists:
        from xitobot_code.modules.conversations import OVERWRITE_NOTE
        context.user_data["note"] = note
        return OVERWRITE_NOTE
    else:
        notes_db.add_note_to_db(chat_id, chat_surname, note_name, text, description, data_type, file_id)
        await update.effective_message.reply_text(f"Saved {note_name}.")

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if len(context.args)>1 and not "-d" in context.args:
        await update.effective_message.reply_text("Please only provide the note's name.")
        return
    elif len(context.args)>1 and "-d" in context.args:
        note_name = next(arg for arg in context.args if arg!="-d")
        await update.effective_message.reply_text(note_name)
    else:
        note_name = context.args[0]

    note_exists = notes_db.check_existing_note(note_name, chat_id)

    if not note_exists:
        await update.effective_message.reply_text("There's no note with that name.")
        return

    note_values = notes_db.get_note(note_name, chat_id)
    text, description, data_type, file_id = note_values

    if "-d" in context.args:
        text+= f"\n\n*Description:*\n{description}"

    if data_type == Types.TEXT:
        await context.bot.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN_V2)
    elif data_type == Types.STICKER:
        await context.bot.send_sticker(chat_id, file_id, parse_mode=ParseMode.MARKDOWN_V2)
    elif data_type == Types.PHOTO:
        await context.bot.send_photo(chat_id, file_id, text, parse_mode=ParseMode.MARKDOWN_V2)
    elif data_type == Types.DOCUMENT:
        await context.bot.send_document(chat_id, file_id, text, parse_mode=ParseMode.MARKDOWN_V2)
    elif data_type == Types.GIF:
        await context.bot.send_animation(chat_id, file_id, caption=text, parse_mode=ParseMode.MARKDOWN_V2)
    elif data_type == Types.AUDIO:
        await context.bot.send_audio(chat_id, file_id, caption=text, parse_mode=ParseMode.MARKDOWN_V2)
    elif data_type == Types.VOICE:
        await context.bot.send_voice(chat_id, file_id, caption=text, parse_mode=ParseMode.MARKDOWN_V2)
    elif data_type == Types.VIDEO:
        await context.bot.send_video(chat_id, file_id, caption=text, parse_mode=ParseMode.MARKDOWN_V2)
    
async def get_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    
    notes_in_chat = notes_db.check_any_note(chat_id)
    
    if not notes_in_chat:
        await update.effective_message.reply_text(f"There are no notes to show in {chat_name}\.", parse_mode=ParseMode.MARKDOWN_V2)
        return
    
    notes_list = notes_db.list_all(chat_id)
    filtered_list = "\n".join([str("\- "+document["name"]) for document in notes_list])
    final_list = f"List of all notes in {chat_name}:\n"+filtered_list
    
    await context.bot.send_message(chat_id, final_list, parse_mode=ParseMode.MARKDOWN_V2)

async def del_all_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name

    notes_in_chat = notes_db.check_any_note(chat_id)

    if not notes_in_chat:
        await update.effective_message.reply_text(f"There aren't any notes to delete in {chat_name}\.", parse_mode=ParseMode.MARKDOWN_V2)
        return
    
    deleted = notes_db.clear_all_notes(chat_id)
    await update.effective_message.reply_text(f"Deleted {deleted} notes from {chat_name}\.", parse_mode=ParseMode.MARKDOWN_V2)

#---HANDLERS CREATION

get_all_notes_handler = CommandHandler("notes", get_all_notes)
del_all_notes_handler = CommandHandler("clearNotes", del_all_notes)
get_handler = CommandHandler("get", get)

application.add_handler(get_all_notes_handler)
application.add_handler(del_all_notes_handler)
application.add_handler(get_handler)
