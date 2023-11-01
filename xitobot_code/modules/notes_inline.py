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
from telegram.ext import InlineQueryHandler, ContextTypes
from xitobot_code import application, LOGGER
from xitobot_code.tools.get_info import Types
import xitobot_code.database.notes_db as notes_db
from uuid import uuid4

async def set_inline_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    inline_chat_exists = notes_db.check_existing_inline_chat(chat_id)
    args = context.args
    
    if len(args)>1:
        await update.effective_message.reply_text("The surname for the chat must only contain 1 word\.")
        return
    elif not args:
        await update.effective_message.reply_text("Please insert a valid surname for the chat\.")
        return
    
    surname = args[0]

    if inline_chat_exists:
        from xitobot_code.modules.conversations import OVERWRITE_CHAT_SURNAME
        context.user_data["chat_new_surname"] = surname
        await update.effective_message.reply_text(
            f"{update.effective_chat.effective_name} is already registered as {notes_db.get_inline_surname(chat_id)}\.\nWould you like to update the surname? \(yes / no\)"
            )
        return OVERWRITE_CHAT_SURNAME

    notes_db.add_inline_chat(chat_id, surname)
    await update.effective_message.reply_text(
        f"{update.effective_chat.effective_name} notes will be accessible with inline commands under the name of {surname}\."
        )
    
async def inline_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    
    if not query:
        return
    
    splitted_query = query.split()
    
    if "-d" in query:
        args = [arg for arg in splitted_query if arg!="-d"]
    else:
        args = query.split(maxsplit=2)

    chat_surname, note_name = args

    note_exists = notes_db.check_existing_note(note_name, chat_surname=chat_surname)
    
    if not note_exists:
        return
    
    note_values = notes_db.get_note(note_name, chat_surname=chat_surname)
    text, description, data_type, file_id = note_values

    if "-d" in query:
        text+= f"\n\n*Description:*\n{description}"

    results = []

    if data_type == Types.TEXT:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=note_name,
                input_message_content=InputTextMessageContent(text)
            )
        )
    elif data_type == Types.STICKER:
        results.append(
            InlineQueryResultCachedSticker(
                id=str(uuid4()),
                sticker_file_id=file_id,
            )
        )
    elif data_type == Types.DOCUMENT:
        results.append(
            InlineQueryResultCachedDocument(
                id=str(uuid4()),
                document_file_id=file_id,
                title=note_name,
                caption=text
            )
        )    
    elif data_type == Types.PHOTO:
        results.append(
            InlineQueryResultCachedPhoto(
                id=str(uuid4()),
                photo_file_id=file_id,
                title=note_name,
                caption=text
            )
        )
    elif data_type == Types.AUDIO:
        results.append(
            InlineQueryResultCachedAudio(
                id=str(uuid4()),
                audio_file_id=file_id,
                caption=text
            )
        )
    elif data_type == Types.VOICE:
        results.append(
            InlineQueryResultCachedVoice(
                id=str(uuid4()),
                voice_file_id=file_id,
                title=note_name,
                caption=text
            )
        )
    elif data_type == Types.VIDEO:
        results.append(
            InlineQueryResultCachedVideo(
                id=str(uuid4()),
                video_file_id=file_id,
                title=note_name,
                caption=text
            )
        )
    elif data_type == Types.GIF:
        results.append(
            InlineQueryResultCachedGif(
                id=str(uuid4()),
                gif_file_id=file_id,
                title=note_name,
                caption=text
            )
    )
        
    await context.bot.answer_inline_query(update.inline_query.id, results)

inline_notes_hander = InlineQueryHandler(inline_notes)

application.add_handler(inline_notes_hander)
