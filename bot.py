from config import *
import importdir
import sys
import asyncio


if sys.version_info.major < 3:
    raise Exception("Must be using Python 3")

importdir.do('handlers', globals())


asyncio.run(bot.polling())