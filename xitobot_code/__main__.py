import importlib
from xitobot_code import LOGGER
from xitobot_code.modules import ALL_MODULES
from xitobot_code.modules.stupid_modules import STUPID_MODULES
from . import application
import os
from telegram import Update
from telegram.ext import (  ContextTypes, 
                            filters, 
                            MessageHandler, 
                            CommandHandler,
)

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("xitobot_code.modules." + module_name)

for module_name in STUPID_MODULES:
    imported_stupid_module = importlib.import_module("xitobot_code.modules.stupid_modules." + module_name)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pid = os.getpid()
    await update.message.reply_text(f"{update.message.text} The base url is: {context.bot.base_url}"
                                    f"\nwith {pid}")

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="eiiiii")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown command :(")

def main():
    start_handler = CommandHandler('start', start)
    check_handler = CommandHandler('check', check)
    unknown_commands_handler = MessageHandler(filters.COMMAND & filters.Text("@xitosbot"), unknown)

    application.add_handler(start_handler)
    application.add_handler(check_handler)
    application.add_handler(unknown_commands_handler)

    application.run_polling()

if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()