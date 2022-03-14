import os, traceback, discord, datetime
from discord.ext import commands
import config as cf

# CONFIG
token = cf.token
prefix = cf.prefix
cogs = cf.cogs
#
class MyBot(commands.Bot):

    def __init__(self, command_prefix, **kwargs):
        super().__init__(command_prefix, **kwargs)

        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        os.system('clear')
        print(f">>> {self.user}にログインしました！")
        await self.change_presence(activity=discord.Game(name=f"{prefix}help"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance ( error , commands.CommandNotFound ):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            return

if __name__ == '__main__':
    bot = MyBot(command_prefix=prefix, intents = discord.Intents.all())
    bot.run(token)