try:
    from userbot import bot
    from userbot.events import register
except:
    pass
from uniborg.util import admin_cmd

if borg:
    @borg.on(admin_cmd(pattern="ppe"))
    async def switch_ppe(event):
        try:
            borg.ppe_start("__main__")
            await event.delete
        except NameError:
            await event.edit("Borg is not loaded")
elif bot:
    @register(outgoing=True, pattern="^.borg")
    async def switch_borg(event):
        try:
            import stdborg
            await event.delete
        except NameError:
            await event.edit("Bot is not loaded")
