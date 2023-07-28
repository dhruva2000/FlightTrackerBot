from config import *

# -------------------- Handle start and end date querying -------------------- #
#TODO: create a function to validate dates
# @bot.message_handler(
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