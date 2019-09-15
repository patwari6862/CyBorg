from telethon import events
from sample_config import Config
from cyborg.util import is_read as ir
from cyborg.util import progress as pg
from cyborg.util import humanbytes as hb
from cyborg.util import time_formatter as tf

def admin_cmd(pattern=None, outgoing=True):
    pattern = Config.COMMAND_HAND_LER + pattern
    return events.NewMessage(r"{}".format(pattern), outgoing)

async def is_read(borg, entity, message, is_out=None):
    ir(borg, entity, message, is_out)

def progress(current, total, event, start, type_of_ps):
    return pg(current, total, event, start, type_of_ps)

def humanbytes(size):
    return hb(size)

def time_formatter(milliseconds: int) -> str:
    return tf(milliseconds)
