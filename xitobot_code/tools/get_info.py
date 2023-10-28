from enum import IntEnum
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from xitobot_code import application

class Types(IntEnum):
    TEXT = 0
    STICKER = 1
    DOCUMENT = 2
    PHOTO = 3
    AUDIO = 4
    VOICE = 5
    VIDEO = 6
    GIF = 7

def get_note_type(note_msg):
    note_name = ""
    note_text = ""
    description = "No description\."
    note_type = None
    file_id = None

    raw_text = note_msg.text
    args = raw_text.split(maxsplit=3)
    reply = note_msg.reply_to_message
    
    if (len(args) == 1):
        return note_name, note_text, description, note_type, file_id

    note_name = args[1]
        
    if not reply and len(args) == 2:
        return note_name, note_text, description, note_type, file_id
    
    if not reply and len(args) == 3:
        note_type = Types.TEXT
        note_text = args[2]
        return note_name, note_text, description, note_type, file_id

    if reply and len(args)==3:
        description = args[2]
    if reply.text:
        note_type = Types.TEXT
        note_text = reply.text
    elif reply.sticker:
        note_type = Types.STICKER
        file_id = reply.sticker.file_id
    elif reply.animation:
        note_type = Types.GIF
        file_id = reply.document.file_id
        note_text = reply.caption or ""
    elif reply.document:
        note_type = Types.DOCUMENT
        file_id = reply.document.file_id
        note_text = reply.caption or ""
    elif reply.photo:
        note_type = Types.PHOTO
        file_id = reply.photo[-1].file_id
        note_text = reply.caption or ""
    elif reply.audio:
        note_type = Types.AUDIO
        file_id = reply.audio.file_id
        note_text = reply.caption or ""
    elif reply.video:
        note_type = Types.VIDEO
        file_id = reply.video.file_id
        note_text = reply.caption or ""

    return note_name, note_text, description, note_type, file_id 

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        reply = update.message.reply_to_message
        if reply.text:
            replied_message_id = reply.message_id
        elif reply.photo:
            replied_message_id = reply.photo[-1].file_id
        await update.message.reply_text(f"ID: {replied_message_id}")
    else:
        await update.message.reply_text(f"You must reply to a message to use this command.")

def get_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

get_id_handler = CommandHandler('getid', get_id)
application.add_handler(get_id_handler)
