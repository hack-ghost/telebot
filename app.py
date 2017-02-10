#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Import
import argparse
import requests
import json
import sys
import asyncio

import telepot
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open

from handler import Handler
from replier import Replier

# Parse arguments
argparser = argparse.ArgumentParser(description = "A telegram bot just for fun.")
argparser.add_argument("--config", action = "store", default = "config.json", type = str, help = "The config file of the bot.")

args = argparser.parse_args()

config_file = args.config
try:
    with open(config_file) as config:
        bot_config = json.loads(config.read(), encoding="utf-8")
        telebot_token = bot_config["token"]
        admin = bot_config["admin"]
        tuling_token = bot_config["tuling"]
except:
    print("read error")
    sys.exit()

# Make a telebot
class TeleBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TeleBot, self).__init__(*args, **kwargs)
        self.handler = Handler(tuling_token, admin)
        self.replier = Replier(self.sender)

    async def on_chat_message(self, msg):
        await self.sender.sendChatAction("typing")
        reply = await self.handler.handle(msg)
        await self.replier.send(reply, msg)

# Start the Bot
bot = telepot.aio.DelegatorBot(telebot_token, [
    pave_event_space()(
        per_chat_id(), create_open, TeleBot, timeout=30),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
