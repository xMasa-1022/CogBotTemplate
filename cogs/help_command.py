from discord.ext import commands
import discord, json
import config as cf

prefix = cf.prefix

class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    @commands.command()
    async def help(self, ctx):
        page_count = 0

# ----- Help Command ----- #
# >> StartPage
        startpage = discord.Embed(title = f"{ctx.guild.name}", description = f"> {self.bot.name}のヘルプです！", color = 0xfbbedf)
    # └> StartPage Footer
        startpage.set_footer(text = f"{ctx.author}", icon_url = f"{ctx.author.avatar.url}")

        page_contents = [
            startpage,
        ]

        sent_message: discord.Message = await ctx.channel.send(embed=page_contents[0])

        reactions = [
            "🗑",
        ]

        for reaction in reactions:
            await sent_message.add_reaction(reaction)

        def help_react_check(reaction: discord.Reaction, user: discord.User):
            emoji = str(reaction.emoji)
            return emoji in reactions and user == ctx.message.author and reaction.message.id == sent_message.id

        while not self.bot.is_closed():

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=help_react_check, timeout=60.0)

            except:
                await sent_message.clear_reactions()
                return

            else:
                emoji = str(reaction.emoji)
                if emoji == "🗑":
                    await sent_message.delete()
                    return

                await sent_message.remove_reaction(str(reaction.emoji), user)
                await sent_message.edit(embed=page_contents[page_count])

    @help.error
    async def help_error(self, ctx, error):
        e = discord.Embed(title="エラーが発生しました",description=f">>> ```\n{error}\n```",color=0xff0000)
        await ctx.send(embed = e)

def setup(bot) -> None:
    bot.add_cog(HelpCommand(bot))
