from config import *
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

# ----------------------------- Helper Functions ----------------------------- #

# class MenuCallbackFilter(AdvancedCustomFilter):
#     key = 'config'
#     def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
#         return config.check(query=call)


# ----------------------------- Handler Functions ---------------------------- #
#If the user isn't in our database or they choose to reselect their currency we run this function
@bot.message_handler(commands=["start"], func=lambda msg: not is_user(msg.chat.id) and next_step_handler(msg.chat.id) == 0)
@bot.message_handler(commands=["select_currency"], func=lambda msg: is_user(msg.chat.id))
async def start_currency_handler(m):
    cid = m.chat.id
    if not is_user(cid):
        currUser = {
            "_id": str(cid),
            "active": True,
            "fname": m.chat.first_name,
            "lname": m.chat.last_name,
            "notifications": False,
            "currency": "USD",
            "search_params": {"fly_from": None, "fly_to": None, "date_from": None, "date_to": None, "return_from": None, "return_to": None, "price_to": None, "max_stopovers": None, "sort": None},
            "tracking":{},
        }
        db.users.insert_one(currUser)
        userStep[cid] = 'currency'
    currUser = db.users.find_one(str(cid))
    await bot.send_message(cid,
        (f"Hello! {currUser['fname']} {currUser['lname']}, before proceeding please let me" 
        " know what your preferred currency is. Respond by selecting one of the supported"
        " currencies in your keyboard below"),
        reply_markup=reply_generator(currencies)
    )
# We run this function if the user is already in our database
@bot.message_handler(commands=["start"], func=lambda msg: is_user(msg.chat.id))
@bot.message_handler(func=lambda msg: next_step_handler(msg.chat.id) == 'menu' or next_step_handler(msg.chat.id) == 'currency')
async def start_is_user(m):
    # print(f"reached start_is_user and next_step is {next_step_handler(m.chat.id)}")
    cid = m.chat.id
    if next_step_handler(cid) == 'currency':
        await remove_reply_keyboard(cid, "removing keyboard... ")
        db.users.update_one({"_id": str(cid)}, {"$set": {"currency": m.text}})
        userStep[cid] = 'menu'
        print(f"reached line 49 and next_step is {next_step_handler(m.chat.id)}")
    if next_step_handler(cid) == 'menu' or next_step_handler(cid) == 0:
        currUser = db.users.find_one(str(cid))
        await bot.send_chat_action(cid, "typing")
        await bot.send_message(
            cid,
            (f"Hello {currUser['fname']}, I'm a bot programmed" 
        " to find you the best tickets home. To get started click on the following 👇"),
            reply_markup=inline_generator(menu_options)
        )


# bot.add_custom_filter(MenuCallbackFilter())