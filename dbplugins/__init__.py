#credits from @penn5 https://github.com/friendly-telegram/friendly-telegram/
import sys
import logging

from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec

from cyborg import cyborg, util


# When a name is matched, the import is overriden, and our custom object is returned
settings = {"uniborg": cyborg, "uniborg.util": util}


class BotCompat(MetaPathFinder, Loader):
    def __init__(self, clients):
        self.clients = clients
        self.created = []

    def find_spec(self, fullname, path, target=None):
        if fullname in settings:
            return ModuleSpec(fullname, self)

    def create_module(self, spec):
        ret = settings[spec.name](self.clients)
        self.created += [ret]
        return ret

    def exec_module(self, module):
        module.__path__ = []

    async def client_ready(self, client):
        self.clients += [client]
        for mod in self.created:
            try:
                await mod.client_ready(client)
            except BaseException:
                logging.exception("Failed to send client_ready to compat layer " + repr(mod))


def activate(clients):
    compatlayer = BotCompat(clients)
    sys.meta_path.insert(0, compatlayer)
    return compatlayer
