from . import DB
from ..tool_modules.get_type import Types

class Notes():
    chat_id = ""
    name = ""
    value = ""
    file = ""
    is_reply = False
    msgtype = 0

    def __init__(self, chat_id, name, value, file=None):
        self.chat_id = str(chat_id)
        self.name = name
        self.value = value
        self.file = file

async def add_note_to_db(chat_id, note_name, note_data, msgtype, file=None):
    DB["notes"].insert_one({"chat_id":chat_id, "name":note_name, "note_data":note_data or "", "msgtype":msgtype.value, "file":file})
    