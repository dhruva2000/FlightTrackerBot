from config import *

@bot.message_handler(commands=['cancel'])
async def cancel_command(m):
    cid = m.chat.id
    if is_user(cid):
        if next_step_handler(cid) != 0:
            userStep[cid] = 0
            await bot.send_chat_action(cid, 'typing')
            await bot.send_message(
                cid, responses['cancel'])
        else:
            await bot.send_chat_action(cid, 'typing')
            await bot.send_message(
                cid, "You haven't done anything yet")
    else:
        await bot.send_chat_action(cid, 'typing')
        await bot.send_message(cid, responses['not_user'])