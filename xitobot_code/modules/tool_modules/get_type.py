from enum import IntEnum
from telegram import Update, Message

class Types(IntEnum):
    TEXT = 0
    STICKER = 1
    DOCUMENT = 2
    PHOTO = 3
    AUDIO = 4
    VOICE = 5
    VIDEO = 6

def get_note_type(note_msg):
    data_type = None
    content = None
    text = ""
    raw_text = note_msg.text
    args = raw_text.split(maxsplit=2)
    reply = note_msg.reply_to_message
    
    if len(args) == 1:
        note_name = None
    else:
        note_name = args[1]
        if reply and len(args) >= 3:
            if reply.text:
                data_type = Types.TEXT
                text = str(reply.text).join(args[2])
            elif reply.sticker:
                data_type = Types.STICKER
                content = reply.sticker.file_id
            elif reply.document:
                data_type = Types.DOCUMENT
                content = reply.document.file_id
                text = str(reply.caption).join(args[2])
            elif reply.photo:
                data_type = Types.PHOTO
                content = reply.photo[-1].file_id
                text = str(reply.caption).join(args[2])
            elif reply.audio:
                data_type = Types.AUDIO
                content = reply.audio.file_id
                text = str(reply.caption).join(args[2])
            elif reply.video:
                data_type = Types.VIDEO
                content = reply.video.file_id
                text = str(reply.caption).join(args[2])
        elif not reply and len(args)>=3:
            data_type = Types.TEXT
            text = args[2]
        elif reply and len(args)==2:
            if reply.text:
                data_type = Types.TEXT
                text = reply.text
            elif reply.sticker:
                data_type = Types.STICKER
                content = reply.sticker.file_id
            elif reply.document:
                data_type = Types.DOCUMENT
                content = reply.document.file_id
                text = reply.caption
            elif reply.photo:
                data_type = Types.PHOTO
                content = reply.photo[-1].file_id
                text = reply.caption
            elif reply.audio:
                data_type = Types.AUDIO
                content = reply.audio.file_id
                text = reply.caption
            elif reply.video:
                data_type = Types.VIDEO
                content = reply.video.file_id
                text = reply.caption
        else:
            text = ""

    return note_name, text, data_type, content 