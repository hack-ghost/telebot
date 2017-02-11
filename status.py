import argparse
import json

from collections import defaultdict

# Import a non-async telepot library to use non-async getMe() function
import telepot

# Parse arguments
argparser = argparse.ArgumentParser(description = "A telegram bot just for fun.")
argparser.add_argument("--config", action = "store", default = "config.json", type = str, help = "Location of the config file of the bot.")

args = argparser.parse_args()

class Status(object):
    """
    Use a status class to store the program stauts, and provide other modules
    a interface.
    """
    def __init__(self):
        global args
        self.config_file = args.config

        with open(self.config_file) as config:
            self._bot_config = json.loads(config.read(), encoding="utf-8")
            self._telebot_token = self._bot_config["token"]
            self._admin = self._bot_config["admin"]
            self._tuling_token = self._bot_config["tuling"]
        self._bot = telepot.Bot(self._telebot_token)
        self._me = self._bot.getMe()
        del self._bot # Won't use it in the future

        self.switch = defaultdict(lambda: True)

    @property
    def tuling_token(self):
        return self._tuling_token

    @property
    def telebot_token(self):
        return self._telebot_token

    @property
    def admin(self):
        return self._admin

    @property
    def name(self):
        return self._me["username"]

    @property
    def me(self):
        return self._me

# Initialize a status object to provide interface to other modules
bot_status = Status()
