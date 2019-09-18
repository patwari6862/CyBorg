# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import asyncio
import importlib.util
import logging
from pathlib import Path

from telethon import TelegramClient
import os
import telethon.utils
import telethon.events

from . import hacks
from pymongo import MongoClient


class Cyborg(TelegramClient):
    def __init__(
            self, session, *, n_plugin_path="plugins", db_plugin_path="plugins",
            bot_token=None, api_config=None, **kwargs):
        self._name = "LoggedIn"
        self._logger = logging.getLogger("UniBorg")
        self._plugins = {}
        self.n_plugin_path = n_plugin_path
        self.db_plugin_path = db_plugin_path
        self.config = api_config
        self.mongo = MongoClient(os.environ.get("MONGO_URI",None))

        kwargs = {
            "api_id": 6,
            "api_hash": "eb06d4abfb49dc3eeb1aeb98ae0f581e",
            "device_model": "GNU/Linux nonUI",
            "app_version": "@CyBorg 2.0",
            "lang_code": "ml",
            **kwargs
        }

        self.tgbot = None
        if api_config.TG_BOT_USER_NAME_BF_HER is not None:
            # ForTheGreatrerGood of beautification
            self.tgbot = TelegramClient(
                "TG_BOT_TOKEN",
                api_id=api_config.APP_ID,
                api_hash=api_config.API_HASH
            ).start(bot_token=api_config.TG_BOT_TOKEN_BF_HER)

        super().__init__(session, **kwargs)

        # This is a hack, please avert your eyes
        # We want this in order for the most recently added handler to take
        # precedence
        self._event_builders = hacks.ReverseList()

        self.loop.run_until_complete(self._async_init(bot_token=bot_token))
        
        core_plugin = Path(__file__).parent / "_core.py"
        self.load_plugin_from_file(core_plugin)

        inline_bot_plugin = Path(__file__).parent / "_inline_bot.py"
        self.load_plugin_from_file(inline_bot_plugin)

        import compat.uniborg
        import compat.paperplane
        import sys
        sys.modules['uniborg'] = compat.uniborg
        sys.modules['userbot'] = compat.paperplane
        

        if str(self.config.PPE_MODE) == "True":
            for a_plugin_path in Path().glob(f"compat/paperplane/*.py"):
                self.load_plugin_from_file(a_plugin_path)

        for a_plugin_path in Path().glob(f"{self.n_plugin_path}/*.py"):
            self.load_plugin_from_file(a_plugin_path)

        if api_config.DB_URI is not None:
            for a_plugin_path in Path().glob(f"{self.db_plugin_path}/*.py"):
                self.load_plugin_from_file(a_plugin_path)

        LOAD = self.config.LOAD
        NO_LOAD = self.config.NO_LOAD
        if LOAD or NO_LOAD:
            to_load = LOAD
            if to_load:
                self._logger.info("Modules to LOAD: ")
                self._logger.info(to_load)
            if NO_LOAD:
                for plugin_name in NO_LOAD:
                    if plugin_name in self._plugins:
                        self.remove_plugin(plugin_name)


    async def _async_init(self, **kwargs):
        await self.start(**kwargs)

        self.me = await self.get_me()
        self.uid = telethon.utils.get_peer_id(self.me)

        self._logger.info(f"Logged in as {self.uid}")


    def load_plugin(self, shortname):
        self.load_plugin_from_file(f"{self.n_plugin_path}/{shortname}.py")

    def db_load_plugin(self, shortname):
        self.load_plugin_from_file(f"{self.db_plugin_path}/{shortname}.py")

    def load_plugin_from_file(self, path):
        path = Path(path)
        shortname = path.stem
        name = f"_UniborgPlugins.{self._name}.{shortname}"

        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)

        mod.borg = self
        mod.bot = self
        mod.logger = logging.getLogger(shortname)
        mod.mongo_client = self.mongo
        # declare Config and tgbot to be accessible by all modules
        mod.Config = self.config
        if self.config.TG_BOT_USER_NAME_BF_HER is not None:
            mod.tgbot = self.tgbot


        spec.loader.exec_module(mod)
        self._plugins[shortname] = mod
        self._logger.info(f"Successfully loaded plugin {shortname}")

    def remove_plugin(self, shortname):
        name = self._plugins[shortname].__name__

        for i in reversed(range(len(self._event_builders))):
            ev, cb = self._event_builders[i]
            if cb.__module__ == name:
                del self._event_builders[i]

        del self._plugins[shortname]
        self._logger.info(f"Removed plugin {shortname}")

    def db_remove_plugin(self, shortname):
        name = self.db_plugin_path + f"/{shortname}.py"

        for i in reversed(range(len(self._event_builders))):
            ev, cb = self._event_builders[i]
            if cb.__module__ == name:
                del self._event_builders[i]

        self._logger.info(f"Removed plugin {shortname}")

    def command(**args):
        """ Register a new event. """
        pattern = args.get("pattern", None)
        allow_sudo = args.get("allow_sudo", False)

        # get the pattern from the decorator
        if pattern is not None:
            if pattern.startswith("\#"):
                # special fix for snip.py
                args["pattern"] = re.compile(pattern)
            else:
                args["pattern"] = re.compile(self.config.COMMAND_HAND_LER + pattern)

        args["outgoing"] = True
        # should this command be available for other users?
        if allow_sudo:
            args["from_users"] = list(self.config.SUDO_USERS)
            # Mutually exclusive with outgoing (can only set one of either).
            args["incoming"] = True
            del args["allow_sudo"]

        # error handling condition check
        elif "incoming" in args and not args["incoming"]:
            args["outgoing"] = True

        # add blacklist chats, UB should not respond in these chats
        args["blacklist_chats"] = True
        black_list_chats = list(self.config.UB_BLACK_LIST_CHAT)
        if len(black_list_chats) > 0:
            args["chats"] = black_list_chats

        # check if the plugin should allow edited updates
        allow_edited_updates = False
        if "allow_edited_updates" in args and args["allow_edited_updates"]:
            allow_edited_updates = args['allow_edited_updates']
            del args['allow_edited_updates']

        is_message_enabled = True

        def decorator(func):
            if not disable_edited:
                self.add_event_handler(func, events.MessageEdited(**args))
            self.add_event_handler(func, events.NewMessage(**args))

            return func

        return decorator

    def await_event(self, event_matcher, filter=None):
        fut = asyncio.Future()

        @self.on(event_matcher)
        async def cb(event):
            try:
                if filter is None or await filter(event):
                    fut.set_result(event)
            except telethon.events.StopPropagation:
                fut.set_result(event)
                raise

        fut.add_done_callback(
            lambda _: self.remove_event_handler(cb, event_matcher))

        return fut
