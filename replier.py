class Replier(object):
    def __init__(self, sender):
        self.sender = sender

    async def send(self, reply, msg):
        if not reply: return
        await self.sender.sendChatAction("typing")
        if msg["chat"]["type"] == "group" or msg["chat"]["type"] == "supergroup":
            await self.sender.sendMessage(reply, reply_to_message_id=msg["message_id"])
        else:
            await self.sender.sendMessage(reply)
