from config import *

# @bot.message_handler(func=lambda m: m.content_type == "text" and m.text == "CREDITS")
@bot.message_handler(commands=["credits"])
async def credits_command(m):
    if not is_user(m.chat.id):
        await bot.send_chat_action(m.chat.id, "typing")
        await bot.send_message(m.chat.id, responses["not_user"])
    else:
        await bot.send_chat_action(m.chat.id, "typing")
        await bot.send_message(m.chat.id, responses["credits"])
