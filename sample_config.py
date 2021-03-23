from os import environ

# To use manual values, change these
default_bot_token = "Your_Bot_Token_Here"
default_sudo_chat_id =  -1234567777
default_owner_id = 12345567

# Don't change these value
bot_token = environ.get("BOT_TOKEN", default_bot_token)
sudo_chat_id = int(environ.get("SUDO_CHAT_ID", default_sudo_chat_id))
owner_id = int(environ.get("OWNER_ID", default_owner_id))
