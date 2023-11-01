from telegram import Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, ContextTypes, filters
from xitobot_code import application
from xitobot_code.modules.notes import save
from xitobot_code.modules.notes_inline import set_inline_notes
import xitobot_code.database.notes_db as notes_db

OVERWRITE_NOTE, OVERWRITE_CHAT_SURNAME = range(2)

async def update_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_response = update.effective_message.text
    chat_id = update.effective_chat.id
    note_name, text, description, data_type, file_id = context.user_data["note"]

    if user_response.lower() == "yes":
        notes_db.update_note(chat_id, note_name, text, description, data_type, file_id)
        await context.bot.send_message(chat_id, f"Updated {note_name}\.")
    elif user_response.lower() == "no":
        await context.bot.send_message(chat_id, "Canceling overwrite\.")
    else:
        await context.bot.send_message(chat_id, "Please type 'yes' or 'no'\.")
    return ConversationHandler.END

async def update_inline_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_response = update.effective_message.text
    surname = context.user_data["chat_new_surname"]
    
    if user_response.lower() == "yes":
        notes_db.update_inline_chat(chat_id, surname)
        await context.bot.send_message(chat_id, f"Updated surname for {update.effective_chat.effective_name}\.")
    elif user_response.lower() == "no":
        await context.bot.send_message(chat_id, "Canceling overwrite\.")
    else:
        await context.bot.send_message(chat_id, "Please type 'yes' or 'no'\.")
        return OVERWRITE_CHAT_SURNAME
    return ConversationHandler.END


note_update_handler = ConversationHandler(
    entry_points = [CommandHandler("save", save)],
    states = {OVERWRITE_NOTE: [MessageHandler(filters.TEXT, update_note)]},
    fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
)

inline_name_update_handler = ConversationHandler(
    entry_points = [CommandHandler("setInlineMode", set_inline_notes)],
    states = {OVERWRITE_CHAT_SURNAME: [MessageHandler(filters.ALL, update_inline_name)]},
    fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
)

application.add_handler(note_update_handler)
application.add_handler(inline_name_update_handler)