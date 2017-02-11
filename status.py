import argparse
import json

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

    @property
    def tuling_token(self):
        return self._tuling_token

    @property
    def telebot_token(self):
        return self._telebot_token

    @property
    def admin(self):
        return self._admin

bot_status = Status()
