from discord.ext import commands
import discord, traceback, json, datetime, os, sys
from aioconsole import aexec
import config as cf

cogs = cf.cogs
owners = cf.owners

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval")
    @commands.is_owner()
    async def _eval(self, ctx: commands.Context, *, code: str):
        if code.startswith("```python"):
            code = code[9:-3]
        if code.startswith("```"):
            code = code[3:-3]
        if code.startswith("```py"):
            code = code[5:-3]
        local_variables = {
        "discord": discord,
        "self": self,
        "bot": self.bot,
        "client": self.bot,
        "ctx": ctx,
        "message": ctx.message,
        "author": ctx.message.author,
        "guild": ctx.message.guild,
        "channel": ctx.message.channel
        }
        try:
            await aexec(code, local_variables)
        except:
            ee = discord.Embed(title="例外が発生しました！",description=f"**エラー内容:**\n```\n{traceback.format_exc()}\n```",color=0xE74C3C)
            await ctx.channel.send(embed=ee)

    @_eval.error
    async def _eval_error(self, ctx, error):
        e = discord.Embed(title="エラーが発生しました",description=f">>> ```\n{error}\n```",color=0xff0000)
        await ctx.send(embed = e)

    @commands.command(aliases=['r', 'rl'])
    @commands.is_owner()
    async def reload(self, ctx: commands.Context) -> None:
        fails = []
        empty_list = []
        for extension in cogs:
            try:
                self.bot.reload_extension(f"{extension}")
            except:
                if extension in fails:
                    pass
                else:
                    fails.append(extension)
        if fails == empty_list:
            await ctx.message.add_reaction("✅")
        else:
            e = discord.Embed(title = "リロード中にエラーが発生しました", description = f">>> ```\n{fails}\n```", color = 0xff0000)
            await ctx.send(embed = e)

    @reload.error
    async def reload_error(self, ctx, error):
        e = discord.Embed(title="エラーが発生しました",description=f">>> ```\n{error}\n```",color=0xff0000)
        await ctx.send(embed = e)

    @commands.command(aliases=['shutdown'])
    @commands.is_owner()
    async def stop(self, ctx: commands.Context) -> None:
        e = discord.Embed(title="ボット停止", description=f">>> 実行者： {ctx.author.mention} ({ctx.author})\n実行したチャンネル： {ctx.channel.mention}\n実行した時間： {datetime.datetime.now()}", color=0xff0000)
        await ctx.send(embed=e)
        await self.bot.close()

    @commands.command(aliases = ["relogin", "res"])
    @commands.is_owner()
    async def restart(self, ctx: commands.Context) -> None:
        e = discord.Embed(title = "再起動", description = f">>> 実行者： {ctx.author.mention} ({ctx.author})\n実行したチャンネル： {ctx.channel.mention}\n実行した時間： {datetime.datetime.now()}", color = 0xff0000)
        await ctx.send(embed = e)
        os.execv(sys.executable, ['python'] + sys.argv)

def setup(bot):
    bot.add_cog(AdminCog(bot))
