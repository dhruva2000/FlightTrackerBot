from config import *
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter

# ----------------------------- Helper Functions ----------------------------- #

def currency_generator(options):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        keyboard.add(
            types.KeyboardButton(option)
        )
    return keyboard

def keyboard_generator(options):
    keyboard = types.InlineKeyboardMarkup()
    for option in options:
        keyboard.add(
            types.InlineKeyboardButton(text=option['name'], callback_data=option['id'])
        )
    return keyboard

class MenuCallbackFilter(AdvancedCustomFilter):
    key = 'config'
    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


# ----------------------------- Handler Functions ---------------------------- #
#If the user isn't in our database we run this function
@bot.message_handler(commands=["start"], func=lambda msg: not is_user(msg.chat.id) and next_step_handler(msg.chat.id) == 0)
def start_not_user(m):
    cid = m.chat.id
    if not is_user(cid):
        currUser = {
            "_id": str(cid),
            "active": True,
            "fname": m.chat.first_name,
            "lname": m.chat.last_name,
            "notifications": False,
            "currency": "USD",
            "tracking":{},
        }
        db.users.insert_one(currUser)
        userStep[cid] = 'currency'
        bot.send_message(cid,
            (f"Hello! {currUser['fname']} {currUser['lname']}, before proceeding please let me" 
           " know what your preferred currency is. Respond by typing a capital 3 letter currency code"
           " such as USD, CAD, EUR, etc. The supported currencies are in your keyboard below 👇"),
            reply_markup=currency_generator(currencies),
            force_reply=True
        )
# We run this function if the user is already in our database
@bot.message_handler(commands=["start"], func=lambda msg: is_user(msg.chat.id))
def start_is_user(m):
    cid = m.chat.id
    currUser = db.users.find_one(str(cid))
    bot.send_message(
        cid,
        (f"Hello! {currUser['fname']} {currUser['lname']}, I'm a bot programmed" 
       " to find you the best tickets home. To get started click on the following 👇"),
        reply_markup=keyboard_generator(menu_options)
    )

# This function takes in all callback queries and handles them accordingly
@bot.callback_query_handler(func=None)
def callback_query(call):
    cid = call.message.chat.id
    if call.data == '1':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, responses['ticket_type'], reply_markup=keyboard_generator(ticket_options))
        userStep[cid] = 'ticket_type'
    if call.data == '2':
        #TODO: Add tracking functionality
        bot.answer_callback_query(call.id, responses["no_flights"])
    if call.data == '3':
        #TODO: Add settings functionality
        bot.answer_callback_query(call.id, responses["not_user"])
    if call.data == '4':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, responses['ticket_type'], reply_markup=keyboard_generator(ticket_options))

bot.add_custom_filter(MenuCallbackFilter())