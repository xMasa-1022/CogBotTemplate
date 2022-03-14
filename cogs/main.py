#coding=utf-8
from discord.ext import commands
import discord, json, os, random, datetime, string, traceback

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Ping Command

    @commands.command()
    @commands.cooldown(2, 15, type=discord.ext.commands.BucketType.channel)
    async def ping(self, ctx):
        ping_s = self.bot.latency
        ping = (ping_s / 1000)
        ping = str(ping)[(0):-15]
        e = discord.Embed(title=":ping_pong: Ping!",description=f"> 現在のPingは{ping}msです！",color=0x3bd37b)
        await ctx.channel.send(embed=e)

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        e = discord.Embed(title="エラーが発生しました",description=f">>> ```\n{error}\n```",color=0xff0000)
        await ctx.reply(embed = e)

def setup(bot):
    bot.add_cog(GeneralCog(bot))