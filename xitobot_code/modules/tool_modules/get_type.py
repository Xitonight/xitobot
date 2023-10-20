from enum import IntEnum
from telegram import Message

class Types(IntEnum):
    TEXT = 0
    STICKER = 1
    DOCUMENT = 2
    PHOTO = 3
    AUDIO = 4
    VOICE = 5
    VIDEO = 6

def get_message_type(msg: Message):
    data_type = None
    content = None
    text = ""
    raw_text = msg.caption or msg.text
    args = raw_text.split(maxsplit=2)
    note_name = args[1]

    if len(args) >= 3:
        data_type = Types.TEXT
        text = args[2]
    else:        
        if msg.reply_to_message.text:
            data_type = Types.TEXT
            text = msg.reply_to_message.text
        elif msg.reply_to_message.sticker:
            data_type = Types.STICKER
            content = msg.reply_to_message.sticker.file_id
        elif msg.reply_to_message.document:
            data_type = Types.DOCUMENT
            content = msg.reply_to_message.document.file_id
            text = msg.reply_to_message.caption
        elif msg.reply_to_message.photo:
            data_type = Types.PHOTO
            content = msg.reply_to_message.photo[-1].file_id
            text = msg.reply_to_message.caption
        elif msg.reply_to_message.audio:
            data_type = Types.AUDIO
            content = msg.reply_to_message.audio.file_id
            text = msg.reply_to_message.caption
        elif msg.reply_to_message.video:
            data_type = Types.VIDEO
            content = msg.reply_to_message.video.file_id
            text = msg.reply_to_message.caption

    return note_name, text, data_type, content 