from config import *

@bot.message_handler(func=lambda msg: next_step_handler(msg.chat.id) == 'currency')
def currency_handler(m):
    cid = m.chat.id
    db.users.update_one({"_id": str(cid)}, {"$set": {"currency": m.text}})
    userStep[cid] = 'menu'


@bot.message_handler(commands=["reselect_currency"])
def currency_handler(m):
    cid = m.chat.id
    
    db.users.update_one({"_id": str(cid)}, {"$set": {"currency": m.text}})
    userStep[cid] = 'menu'