from telethon import events
from sample_config import Config
from cyborg.util import admin_cmd as ac
from cyborg.util import is_read as ir
from cyborg.util import progress as pg
from cyborg.util import humanbytes as hb
from cyborg.util import time_formatter as tf

def admin_cmd(pattern=None, allow_sudo=True, outgoing=True, incoming=False, allow_edited_updates=False):
    return ac(pattern, allow_sudo, outgoing, incoming, allow_edited_updates)

async def is_read(borg, entity, message, is_out=None):
    ir(borg, entity, message, is_out)

def progress(current, total, event, start, type_of_ps):
    return pg(current, total, event, start, type_of_ps)

def humanbytes(size):
    return hb(size)

def time_formatter(milliseconds: int) -> str:
    return tf(milliseconds)
