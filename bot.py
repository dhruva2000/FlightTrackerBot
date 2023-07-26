from config import *
import importdir
import sys
import asyncio

if sys.version_info.major < 3:
    raise Exception("Must be using Python 3")

#Custom function to import all handlers from the handlers folder and put them in our global namespace
importdir.do('handlers', globals())

asyncio.run(bot.polling())