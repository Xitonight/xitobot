from telegram import (
                        Update,
                        InlineQueryResultArticle,
                        InputTextMessageContent,
)
from telegram.ext import (
                            ContextTypes,
                            InlineQueryHandler,
                            CommandHandler,
)
from telegram.constants import (
                                    ParseMode,
)
from uuid import uuid4
from xitobot_code import application

async def to_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def to_bold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_bold = f"*{' '.join(context.args)}*"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_bold, parse_mode=ParseMode.MARKDOWN_V2)


async def to_italic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_italic = f"_{' '.join(context.args)}_"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_italic, parse_mode=ParseMode.MARKDOWN_V2)


async def to_underlined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_underlined = f"__{' '.join(context.args)}__"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_underlined, parse_mode=ParseMode.MARKDOWN_V2)

""""""""""""""""""""""""
"""INLINE TEXT FORMAT"""
""""""""""""""""""""""""

async def inline_text_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='caps it',
            input_message_content=InputTextMessageContent(query.upper()),
        ),

        InlineQueryResultArticle(
            id=str(uuid4()),
            title='bold it',
            input_message_content=InputTextMessageContent(
                f"*{query}*", parse_mode=ParseMode.MARKDOWN_V2
            )
        ),

        InlineQueryResultArticle(
            id=str(uuid4()),
            title='italic it',
            input_message_content=InputTextMessageContent(
                f"_{query}_", parse_mode=ParseMode.MARKDOWN_V2
            )
        ),

        InlineQueryResultArticle(
            id=str(uuid4()),
            title='underline it',
            input_message_content=InputTextMessageContent(
                f"__{query}__", parse_mode=ParseMode.MARKDOWN_V2
            )
        ),
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results)

to_caps_handler = CommandHandler('caps', to_caps)
to_bold_handler = CommandHandler('bold', to_bold)
to_italic_handler = CommandHandler('italic', to_italic)
to_underlined_handler = CommandHandler('underline', to_underlined)

inline_text_format_handler = InlineQueryHandler(inline_text_format)

application.add_handler(to_caps_handler)
application.add_handler(to_bold_handler)
application.add_handler(to_italic_handler)
application.add_handler(to_underlined_handler)
application.add_handler(inline_text_format_handler)