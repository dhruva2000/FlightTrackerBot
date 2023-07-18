from config import *

# This function takes in all callback queries and handles them accordingly
@bot.callback_query_handler(func=None)
async def callback_query(call):
    cid = call.message.chat.id
    if call.data == '1':
        await bot.answer_callback_query(call.id)
        await bot.send_message(call.message.chat.id, responses['ticket_type'], reply_markup=inline_generator(ticket_options))
        userStep[cid] = 'ticket_type'
    if call.data == '2':
        #TODO: Add tracking functionality
        await bot.answer_callback_query(call.id, responses["no_flights"])
    if call.data == '3':
        #TODO: Add settings functionality
        await bot.answer_callback_query(call.id, responses["not_user"])
    if call.data == '4':
        await bot.answer_callback_query(call.id)
        # await bot.send_message(call.message.chat.id, responses['ticket_type'], reply_markup=inline_generator(ticket_options))
