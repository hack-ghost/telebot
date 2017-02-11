import requests
import json

from telepot.helper import Router

class Handler(object):
    def __init__(self, tuling_token, admin):
        self._tuling_token = tuling_token
        self.admin = admin
        self.router = Router(self._by_command(),
        {
        "chat": self.on_chat,
        "count": self.on_count,
        None: self._pass,
        })

    async def _pass(self, *aa, **kk): return ""

    def _by_command(self, prefix=('/', '-'), separator=' ', pass_args=True):
        def extractor(msg):
            if msg["text"].startswith('-'):
                return "-chat" + " " + msg["text"].lstrip("- ")
            else:
                return msg["text"]

        if not isinstance(prefix, (tuple, list)):
            prefix = (prefix,)

        def f(msg):
            text = extractor(msg)
            for px in prefix:
                if text.startswith(px):
                    chunks = text[len(px):].split(separator)
                    return chunks[0], (chunks[1:],) if pass_args else ()
            return (None,),  # to distinguish with `None`
        return f

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
