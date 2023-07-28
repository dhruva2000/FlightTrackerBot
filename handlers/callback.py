from config import *
import datetime

# This function takes in all callback queries and handles them accordingly
@bot.callback_query_handler(func=lambda call: call.data != None)
async def menu_callback_query(call):
    cid = call.message.chat.id
    await bot.answer_callback_query(call.id)
    await bot.send_chat_action(cid, "typing")
    print(f"reached menu_callback_query and current call is {call.data}")
    if call.data == 0:
        userStep[cid] = "menu"
        # await bot.edit_message_text(
        #     text=(
        #         f"Hello {currUser['fname']}, I'm a bot programmed"
        #         " to find you the best tickets home. To get started click on the following 👇"
        #     ),
        #     chat_id=cid,
        #     reply_markup=inline_generator(menu_options),
        # )
    if call.data == 1 :
        await bot.edit_message_text(
            text=responses["ticket_type"],
            chat_id=cid,
            reply_markup=inline_generator(ticket_options),
        )
        userStep[cid] = "ticket_type"
    if call.data == 2:
        # TODO: Add tracking functionality
        await bot.answer_callback_query(call.id, responses["no_flights"])
    if call.data == 3:
        # TODO: Add settings functionality
        await bot.answer_callback_query(call.id, responses["not_user"])


# ------------------------ Handle Economy vs Business ------------------------ #
# @bot.callback_query_handler(
#     func=lambda msg: next_step_handler(msg.chat.id) == "ticket_type"
# )
# async def ticket_type_handler(call):
#     cid = call.message.chat.id
#     await bot.answer_callback_query(call.id)
#     await bot.send_chat_action(cid, "typing")
#     if call.data == "4":
#         db.search_params.update_one(
#             {"_id": str(cid)}, {"$set": {"ticket_type": "economy"}}
#         )
#     if call.data == "5":
#         db.search_params.update_one(
#             {"_id": str(cid)}, {"$set": {"ticket_type": "business"}}
#         )
#     await bot.edit_message_text(
#         text=responses["flight_type"],
#         chat_id=cid,
#         reply_markup=inline_generator(flight_type_options),
#     )
#     userStep[cid] = "flight_type"


# ----------------------- Handle One Way vs Round Trip ----------------------- #
# @bot.callback_query_handler(
#     func=lambda msg: next_step_handler(msg.chat.id) == "flight_type"
# )
# async def flight_type_handler(call):
#     cid = call.message.chat.id
#     await bot.answer_callback_query(call.id)
#     await bot.send_chat_action(cid, "typing")
#     if call.data == "6":
#         userStep[cid] = "depart_from_no_return"
#     if call.data == "7":
#         userStep[cid] = "depart_from_with_return"
#     await bot.edit_message_text(
#         text=responses["depart_from"],
#         chat_id=cid,
#     )

# @bot.message_handler(func = lambda msg: next_step_handler(msg.chat.id) == "depart_from_no_return" or "depart_from_with_return")
# async def start_date_handler(m):
#     cid = m.chat.id
#     await bot.send_chat_action(cid, "typing")
#     #TODO: receive the reply from the user and update our search_params with it
#     try:
#         lastOffset
#     except NameError:
#         lastOffset = 1
#     incomingMsgs = await bot.get_updates(offset = lastOffset, allowed_updates=["message"])
#     cnt = len(incomingMsgs)
#     if cnt!=0:
#         lastOffset = incomingMsgs[-1].update_id + 1
#         currReply = incomingMsgs[-1].message.text
#         # giving the date format
#         date_format = '%d-%m-%Y'
#         # using try-except blocks for handling the exceptions
#         try:
#             # formatting the date using strptime() function
#             dateObject = datetime.datetime.strptime(currReply, date_format)
#             if dateObject < datetime.datetime.now():
#                 await bot.send_message(
#                     cid,
#                     responses["invalid_date"],
#                 )
#             else:
#                 db.search_params.update_one(
#                     {"_id": str(cid)}, {"$set": {"date_from": dateObject.strftime("%d-%m-%Y")}}
#                 )
#         # If the date validation goes wrong
#         except ValueError:
#             # printing the appropriate text if ValueError occurs
#             await bot.send_message(
#                 cid,
#                 responses["invalid_date"],
#             )
#     if userStep[cid] == "depart_from_no_return":
#         await bot.send_message(
#             cid,
#             responses["starting_date"],
#         )

# ------------------------ Handle Starting Destination ----------------------- #
# @bot.callback_query_handler(
#     func=lambda msg: next_step_handler(msg.chat.id) == "depart_from_no_return" or  "depart_from_with_return"
# )
# async def starting_dest_handler(call):
#     cid = call.message.chat.id
#     await bot.send_chat_action(cid, "typing")
#     await bot.send_message(
#         call.message.chat.id,
#         responses["starting_city"],
#     )




