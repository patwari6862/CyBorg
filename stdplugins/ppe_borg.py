try:
    from userbot import bot
    from userbot.events import register
except:
    pass
from uniborg.util import admin_cmd

if borg:
    @borg.on(admin_cmd(pattern="ppe"))
    def test(event):
        try:
            import userbot.__main___
        except Exception as e:
            print(str(e))
elif bot:
    @register(outgoing=True, pattern="^.borg")
    async def switch_borg(event):
        try:
            import stdborg
            await event.delete
        except Exception as e:
            await event.edit(str(e))
