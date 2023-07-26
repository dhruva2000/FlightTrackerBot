from config import *


# This function takes in all callback queries and handles them accordingly
@bot.callback_query_handler(func=None)
async def menu_callback_query(call):
    cid = call.message.chat.id
    await bot.answer_callback_query(call.id)
    await bot.send_chat_action(cid, "typing")
    if call.data == "0":
        userStep[cid] = "menu"
        # await bot.edit_message_text(
        #     text=(
        #         f"Hello {currUser['fname']}, I'm a bot programmed"
        #         " to find you the best tickets home. To get started click on the following 👇"
        #     ),
        #     chat_id=cid,
        #     reply_markup=inline_generator(menu_options),
        # )
    if call.data == "1":
        await bot.edit_message_text(
            text=responses["ticket_type"],
            chat_id=cid,
            reply_markup=inline_generator(ticket_options),
        )
        userStep[cid] = "ticket_type"
    if call.data == "2":
        # TODO: Add tracking functionality
        await bot.answer_callback_query(call.id, responses["no_flights"])
    if call.data == "3":
        # TODO: Add settings functionality
        await bot.answer_callback_query(call.id, responses["not_user"])


# ------------------------ Handle Economy vs Business ------------------------ #
@bot.callback_query_handler(
    func=lambda msg: next_step_handler(msg.chat.id) == "ticket_type"
)
async def ticket_type_handler(call):
    cid = call.message.chat.id
    await bot.answer_callback_query(call.id)
    await bot.send_chat_action(cid, "typing")
    if call.data == "4":
        db.search_params.update_one(
            {"_id": str(cid)}, {"$set": {"ticket_type": "economy"}}
        )
    if call.data == "5":
        db.search_params.update_one(
            {"_id": str(cid)}, {"$set": {"ticket_type": "business"}}
        )
    await bot.edit_message_text(
        text=responses["flight_type"],
        chat_id=cid,
        reply_markup=inline_generator(flight_type_options),
    )
    userStep[cid] = "flight_type"


# ----------------------- Handle One Way vs Round Trip ----------------------- #
#TODO: figure out how to show just depart_from question and exclude the return_from question
@bot.callback_query_handler(
    func=lambda msg: next_step_handler(msg.chat.id) == "flight_type"
)
async def flight_type_handler(call):
    cid = call.message.chat.id
    await bot.answer_callback_query(call.id)
    await bot.send_chat_action(cid, "typing")
    if call.data == "6":
        userStep[cid] = "depart_from_no_return"
    if call.data == "7":
        userStep[cid] = "depart_from_with_return"
    await bot.edit_message_text(
        text=responses["depart_from"],
        chat_id=cid,
    )
# ------------------------ Handle Starting Destination ----------------------- #
@bot.callback_query_handler(
    func=lambda msg: next_step_handler(msg.chat.id) == "depart_from_no_return" or  "depart_from_with_return"
)
async def ticket_type_handler(call):
    cid = call.message.chat.id
    if call.data == "6":
        db.search_params.update_one(
            {"_id": str(cid)}, {"$set": {"ticket_type": "economy"}}
        )
        await bot.answer_callback_query(call.id)
        await bot.send_chat_action(cid, "typing")
        await bot.send_message(
            call.message.chat.id,
            responses["flight_type"],
            reply_markup=inline_generator(flight_type_options),
        )
    if call.data == "7":
        db.search_params.update_one(
            {"_id": str(cid)}, {"$set": {"ticket_type": "business"}}
        )
        await bot.answer_callback_query(call.id)
        await bot.send_chat_action(cid, "typing")
        await bot.send_message(
            call.message.chat.id,
            responses["flight_type"],
            reply_markup=inline_generator(flight_type_options),
        )
