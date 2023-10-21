from . import NOTES
import json
from xitobot_code.modules.tool_modules.get_info import Types

def add_note_to_db(chat_id, note_name, note_text, description, note_type, file_id):
    NOTES.insert_one(
        {
        "chat_id":chat_id,
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

def check_existing_notes(chat_id, note_name):
    if list(NOTES.find({"chat_id":chat_id, "name":note_name})):
        return True
    
    return False

def clear_note(chat_id, note_name):
    if not list(NOTES.find({"chat_id":chat_id, "name":note_name})):
        return -1
    
    NOTES.delete_one({"chat_id":chat_id, "name":note_name})
    
    return 0

def list_all(chat_id):
    notes_list = list(NOTES.find({"chat_id":chat_id}, {"_id":0, "name":1}))
    
    return notes_list

def get_note(chat_id, note_name):
    note = NOTES.find_one({"chat_id":chat_id,"name":note_name}, {"_id":0, "chat_id":0, "name":0})
    note_values = list(note.values())
    
    return note_values

def clear_all_notes(chat_id):
    if not list(NOTES.find({"chat_id":chat_id})):
        return -1
    
    deleted = NOTES.delete_many({"chat_id":chat_id})
    
    return deleted.deleted_count