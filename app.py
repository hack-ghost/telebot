#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Import
import requests
import json
import sys
import asyncio

from functools import wraps

# Import required modules
import telepot
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open

# Import app modules
from handler import Handler
from replier import Replier

import status

bot_status = status.bot_status

# Make a telebot
class TeleBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TeleBot, self).__init__(*args, **kwargs) # Init super class first to get sender mixin
        self.status = status.bot_status
        self.handler = Handler(self.status.tuling_token, self.status.admin)
        self.replier = Replier(self.sender)

    async def on_chat_message(self, msg):
        reply = await self.handler.handle(msg)
        await self.replier.send(reply, msg)

# Start the Bot
bot = telepot.aio.DelegatorBot(status.bot_status.telebot_token, [
    pave_event_space()(
        per_chat_id(), create_open, TeleBot, timeout=30),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
