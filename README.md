
# ℹ️ What is xitobot?
xitobot is a multi-funcional modular telegram bot with group management features and all sorts of useful tools.
### DISCLAIMER
I'm not a professional dev, this is my first big project ever and my first time working with PTB and PyMongo or basically any other Python lib. To create this bot i took inspiration from [@PaulSonOfLars](https://github.com/PaulSonOfLars)' [tgbot](https://github.com/PaulSonOfLars/tgbot), once called [Marie](https://t.me/BanhammerMarie_bot), now deprecated and replaced by [Rose](https://t.me/MissRose_bot)

# 📁 Sources:
## 🐍 PTB
It's built with Python [3.10.12](https://www.python.org/downloads/release/python-31012/) using [PTB](https://python-telegram-bot.org/) (Python-Telegram-Bot), a really easy-to-use wrapper for the Telgram Bot API.

If you want to learn more about it check the [official site's documentation](https://docs.python-telegram-bot.org/en/v20.6/) and the [Github page](https://github.com/python-telegram-bot/python-telegram-bot/wiki) which contains kind of a really basic tutorial on how to build your first Telgram Bot using the wrapper.

## 🍃 MongoDB
For database related modules i'm using [MongoDB](https://www.mongodb.com/) paired with PyMongo to work with the db from Python, but you can use whatever you like the most. All modules that make use of the DB are located in [db_modules](xitobot/modules/db_modules)

### Installation
Here are the links to the documentation to install Mongo:
- [Windows](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
- [Linux Ubuntu](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) (If you're using any other distro check [this](https://www.mongodb.com/docs/manual/installation/))
- [MacOS](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
- [Docker](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/#std-label-docker-mongodb-community-install)

# ❗ Dependencies:
You can install all Python dependencies using

`pip3 install -r requirements.txt` 

inside of the root folder of the bot (xitobot)

# ⚙️ Setting up the bot and running it:
## Configuration
The bot is based on a config.py file which only contains a class with all the globally needed variables:
- API token
- Base_url
- Base_url_file (required if you're hosting the Telegram Bot API on your machine)
- Database_url
- Load order
...

As the project is still work in progress i can't provide a full list of all the variables that'll be needed, but i'll try to keep this updated. I'll provide a config example of how the config.py should look

## Running the bot
Once you've set up everything you need, the database, the config and the dependencies, you can run the bot from the root folder using the following command:

`python3 -m xitobot_code`

# 🤝 Need help?
In case you have trouble setting up the bot you can find a bunch of contacts to find me in my profile :)

Good luck!!
