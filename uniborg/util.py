from cyborg.util import admin_cmd as ac
from cyborg.util import is_read as ir
from cyborg.util import progress as pg
from cyborg.util import humanbytes as hb
from cyborg.util import time_formatter as tf

def admin_cmd(pattern=None, allow_sudo=True, outgoing=True, incoming=False, blacklist_chats=True, allow_edited_updates=False):
    ac(pattern, )

async def is_read(borg, entity, message, is_out=None):
    ir(borg, entity, message, is_out)

async def progress(current, total, event, start, type_of_ps):
    pg(current, total, event, start, type_of_ps)

def humanbytes(size):
    hb(size)

def time_formatter(milliseconds: int) -> str:
    tf(milliseconds)
