import os
import telebot
import requests
from telebot import types
from pymongo import MongoClient
import json
import time
import sys

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_KEY = os.environ.get("API_KEY")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hello! I'm a bot programmed to find you the best tickets home. To get started, send",
    )
