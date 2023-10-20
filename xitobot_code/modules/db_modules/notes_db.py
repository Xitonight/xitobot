from . import DB
from ..tool_modules.get_type import Types

async def add_note_to_db(chat_id, note_name, note_data, msgtype, file=None):
    await DB["notes"].insert_one({"chat_id":chat_id, "name":note_name, "note_data":note_data or "", "msgtype":msgtype.value, "file":file})

def list_all(chat_id):
    notes_list = list(DB["notes"].find({"chat_id":chat_id}, {"_id":0, "name":1}))
    return notes_list

def get_note(chat_id, note_name):
    

def clear_all_notes(chat_id):
    if not list(DB["notes"].find({"chat_id":chat_id})):
        return -1
    else:
        delete = DB["notes"].delete_many({"chat_id":chat_id})
        return delete.deleted_count