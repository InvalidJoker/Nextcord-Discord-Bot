import nextcord
from nextcord.ext import commands

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        if "@everyone" in ctx.message.content:
            await ctx.reply("Nö find ich ned cool")
            return
        
        elif "@here" in ctx.message.content:
            await ctx.reply("Nö find ich ned cool")
            return
        
        await ctx.send("Pong!")

    @nextcord.slash_command()
    async def slash_ping(self, ctx: nextcord.Interaction):
        await ctx.response.send_message("Pong!", ephemeral=True)

    @commands.command()
    async def say(self, ctx: commands.Context, *, message: str):
        await ctx.send(f"{ctx.author.mention}: ```{message}```")

def setup(bot):
    bot.add_cog(Base(bot))