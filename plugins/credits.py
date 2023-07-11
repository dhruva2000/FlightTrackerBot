from config import *


@bot.message_handler(func=lambda m: m.content_type == "text" and m.text == "CREDITS")
@bot.message_handler(commands=["credits"])
def command_credits(m):
    bot.send_chat_action(m.chat.id, "typing")
