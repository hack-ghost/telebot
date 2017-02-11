import requests
import json

import telepot.aio
from telepot.aio.helper import Router
from telepot import glance

import status

bot_status = status.bot_status

class Handler(object):
    def __init__(self, tuling_token, admin):
        self._tuling_token = tuling_token
        self.admin = admin

        self.text_router = Router(self._by_command(),
        {
        "chat": self.on_chat,
        "count": self.on_count,
        "status": self.on_status,
        "switch": self.on_switch,
        None: self._pass,
        })

        self._unblocking_commands = ["status", "switch"]

    async def _pass(self, *aa, **kk): return ""

    def _assure_privilege(fn):
        async def wrapper(self, msg, *args, **kwargs):
            if msg["from"]["username"] != self.admin:
                return "Sorry, you're not privileged."
            else:
                return await fn(self, msg, *args, **kwargs)
        return wrapper

    def _by_command(self, prefix=("/",), separator=" ", pass_args=True):
        if not isinstance(prefix, (tuple, list)):
            prefix = (prefix,)

        def key_function(msg):
            chat_id = msg["chat"]["id"]
            command_text = msg["text"].split()[0]
            text = msg["text"]

            if command_text.startswith("/"):
                command_text = command_text.lstrip("/")
                if "@" in command_text:
                    if command_text.count("@") == 1:
                        if command_text.endswith(bot_status.name):                        
                            command = command_text.split("@")[0]
                        else:
                            return
                    else:
                        return
                else:
                    command = command_text.lstrip("/")

            if text.startswith("-"):
                command = "chat"

            # If the bot has been switched off, make some commands avaliable
            if not bot_status.switch[chat_id]:
                if command not in self._unblocking_commands:
                    return

            if text.startswith("-"):
                chucks = text.lstrip("-" + separator).split(separator)
                return command, chucks if pass_args else ()

            for px in prefix:
                if text.startswith(px):
                    chunks = text[len(px):].split(separator)
                    return command, (chunks[1:],) if pass_args else ()
            return (None,),  # to distinguish with `None`

        return key_function

    async def _get_tuling(self, msg, text="你好"):
        api_url = "http://www.tuling123.com/openapi/api"
        json_data = {"key": self._tuling_token, "info": text, "userid": msg["from"]["id"]}
        request = requests.post(api_url, data = json_data)
        result = json.loads(request.text)
        return result["text"]

    async def on_chat(self, msg, *args):
        user_text = " ".join(args[0])
        return await self._get_tuling(msg, text = user_text)

    async def on_count(self, msg, *args, **kwargs):
        return "233"

    async def on_status(self, msg, *args, **kwargs):
        chat_id = msg["chat"]["id"]

        if bot_status.switch[chat_id]:
            return "The bot is on."
        else:
            return "The bot is off."

    @_assure_privilege
    async def on_switch(self, msg, *args, **kwargs):
        chat_id = msg["chat"]["id"]
        bot_status.switch[chat_id] = not bot_status.switch[chat_id]
        return "Switched " + ("on. " if bot_status.switch[chat_id] else "off.")

    async def handle(self, msg):
        content_type, chat_type, chat_id = glance(msg)

        if content_type == "text":
            return await self.text_router.route(msg)
