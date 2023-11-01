from . import NOTES, INLINE_CHATS
from xitobot_code.tools.get_info import Types

#---NOTE SAVING / GETTING FUNCTIONS

def add_note_to_db(chat_id, chat_surname, note_name, note_text, description, note_type, file_id):
    NOTES.insert_one(
        {
        "chat_id":chat_id,
        "chat_surname":chat_surname,
        "name":note_name,
        "text":note_text,
        "description":description,
        "type":note_type.value,
        "file_id":file_id
        }
    )

def update_note(chat_id, note_name, note_text, description, note_type, file_id):
    NOTES.update_one(
        {"chat_id":chat_id,"name":note_name},
        {
            "$set": {
                "text":note_text,
                "description":description,
                "type":note_type,
                "file_id":file_id
                }
        }
    )

def get_note(note_name, chat_id=None, chat_surname=None):
    if chat_id:
        note = NOTES.find_one({"chat_id":chat_id, "name":note_name}, {"_id":0, "chat_id":0, "chat_surname":0, "name":0})
    if chat_surname:    
        note = NOTES.find_one({"chat_surname":chat_surname, "name":note_name}, {"_id":0, "chat_id":0, "chat_surname":0, "name":0})
    
    note_values = list(note.values())
    
    return note_values

def list_all(chat_id):
    notes_list = list(NOTES.find({"chat_id":chat_id}, {"_id":0, "name":1}))

    return notes_list

def check_existing_note(note_name, chat_id=None, chat_surname=None):
    return list(NOTES.find({"chat_id":chat_id, "name":note_name})) or list(NOTES.find({"chat_surname":chat_surname, "name":note_name}))

def check_any_note(chat_id):
    return list(NOTES.find({"chat_id":chat_id}))

#---NOTE DELETION FUNCTIONS

def clear_note(chat_id, note_name):
    NOTES.delete_one({"chat_id":chat_id, "name":note_name})

def clear_all_notes(chat_id):
    deleted = NOTES.delete_many({"chat_id":chat_id})
    
    return deleted.deleted_count

#---INLINE FUNCTIONS

def add_inline_chat(chat_id, chat_surname):
    INLINE_CHATS.insert_one({"chat_id":chat_id, "chat_surname":chat_surname})
    NOTES.update_many({"chat_id":chat_id}, {"$set": {"chat_surname":chat_surname}})

def update_inline_chat(chat_id, chat_surname):
    INLINE_CHATS.update_one({"chat_id":chat_id}, {"$set": {"chat_surname":chat_surname}})
    NOTES.update_many({"chat_id":chat_id}, {"$set": {"chat_surname":chat_surname}})

def get_inline_surname(chat_id):
    inline_chat = INLINE_CHATS.find_one({"chat_id":chat_id}, {"_id":0, "chat_id":0})
    surname = list(inline_chat.values())

    return surname[0]

def check_existing_inline_chat(chat_id):
    return INLINE_CHATS.find_one({"chat_id":chat_id})

