import os
import requests
from telebot import types
import pymongo 
from collections import OrderedDict
import json
from telebot.async_telebot import AsyncTeleBot
import asyncio
# ----------------------------- Global variables ----------------------------- #
BOT_TOKEN = os.environ['BOT_TOKEN']
API_KEY = os.environ['API_KEY']
client = pymongo.MongoClient(os.environ['MONGODB_URI'])
# bot = telebot.TeleBot(BOT_TOKEN)
bot = AsyncTeleBot(BOT_TOKEN)
userStep = {} # track the current step of the user
currUser = ""

with open("response.json", encoding='utf-8') as r:
    responses = json.load(r, object_pairs_hook=OrderedDict) # load responses

db = client.flight_tracker # initalize database


# --------------------------------- Keyboards -------------------------------- #

menu_options = [
    {'id': 1, 'name': 'New Flight'},
    {'id': 2, 'name': 'Track Flights'},
    {'id': 3, 'name': 'Settings'},
]

ticket_options = [
    {'id': 4, 'name': 'Economy'},
    {'id': 5, 'name': 'Business'},
    {'id': 0, 'name': 'Menu ☰'}
]

flight_type_options = [
    {'id': 6, 'name': 'One-way'},
    {'id': 7, 'name': 'Round-trip'},
    {'id': 0, 'name': 'Menu ☰'}
]

currencies = [
    'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 
    'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 
    'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 
    'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EEK', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 
    'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 
    'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 
    'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 
    'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 
    'MNT', 'MOP', 'MRO', 'MTL', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 
    'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 
    'QAR', 'QUN', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 
    'SHP', 'SLL', 'SOS', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 
    'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 
    'VUV', 'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMK', 'ZMW', 'ZWL']

# --------------------------------- Functions -------------------------------- #
def is_user(cid):
    return db.users.find_one(str(cid)) is not None and db.users.find_one(str(cid))['active'] == True

def next_step_handler(cid):
    if cid not in userStep:
        userStep[cid] = 0
    return userStep[cid]

def reply_generator(options):
    curr = 0
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=True, is_persistent=False)
    while curr < len(options)-4:
        keyboard.add(options[curr], options[curr+1], options[curr+2], options[curr+3])
        curr += 4
    return keyboard

def inline_generator(options):
    temp = []
    curr = 0
    keyboard = []
    while curr < len(options):
        while len(temp) < 2 and curr<len(options):
            temp.append(types.InlineKeyboardButton(text=options[curr]['name'], callback_data=options[curr]['id']))
            curr += 1
        keyboard.append(temp)
        temp = []
    return types.InlineKeyboardMarkup(keyboard=keyboard)

async def remove_reply_keyboard(cid, text):
    msg = await bot.send_message(cid, text, reply_markup=types.ReplyKeyboardRemove())
    await bot.delete_message(cid, msg.message_id)
    