import os
import telebot
import requests
from telebot import types
import pymongo 
from collections import OrderedDict
import json
import time
import sys

# ----------------------------- Global variables ----------------------------- #
BOT_TOKEN = os.environ['BOT_TOKEN']
API_KEY = os.environ['API_KEY']
client = pymongo.MongoClient(os.environ['MONGODB_URI'])
bot = telebot.TeleBot(BOT_TOKEN)
userStep = {}
with open("response.json", encoding='utf-8') as r:
    responses = json.load(r, object_pairs_hook=OrderedDict)
db = client.flight_tracker
# --------------------------------- Functions -------------------------------- #
def is_user(cid):
    return db.users.find_one(str(cid)) is not None and db.users.find_one(str(cid))['active'] == True

def next_step_handler(uid):
    if uid not in userStep:
        userStep[uid] = 0
    return userStep[uid]

@bot.message_handler(commands=["start"])
def start(m):
    cid = m.chat.id
    if not is_user(cid):
        currUser = {
            "_id": str(cid),
            "active": True,
            "fname": m.chat.first_name,
            "lname": m.chat.last_name,
            "notifications": False,
            "tracking":{},
        }
        db.users.insert_one(currUser)
    currUser = db.users.find_one(str(cid))
    bot.send_message(
        cid,
        (f"Hello! {currUser['fname']} {currUser['lname']}, I'm a bot programmed" 
       " to find you the best tickets home. To get started click on the following 👇")
    )
