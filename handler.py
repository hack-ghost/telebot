import requests
import json

from telepot.routing import by_command
from telepot.helper import Router

class Handler(object):
    def __init__(self, tuling_token, admin):
        self._tuling_token = tuling_token
        self.admin = admin
        self.router = Router(by_command(
        lambda msg: "/chat" + " " + msg["text"].lstrip("- ") if msg["text"][0] == "-" else msg["text"],
        pass_args = True),
        {
        "chat": self.on_chat,
        "count": self.on_count,
        None: self._pass,
        })

    async def _pass(self, *aa, **kk): return ""

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

    async def handle(self, msg):
        return await self.router.route(msg)
