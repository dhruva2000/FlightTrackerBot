from config import *

@bot.message_handler(commands=['cancel'])
def cancel_command(m):
    cid = m.chat.id
    if is_user(cid):
        if next_step_handler(cid) != 0:
            userStep[cid] = 0
            bot.send_chat_action(cid, 'typing')
            bot.send_message(
                cid, responses['cancel'])
        else:
            bot.send_chat_action(cid, 'typing')
            bot.send_message(
                cid, "You haven't done anything yet")
    else:
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, responses['not_user'])