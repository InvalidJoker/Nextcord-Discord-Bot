import nextcord
from nextcord.ext import commands
from config import TOKEN, PREFIX, ERROR_CHANNEL, OWNER
import os

bot = commands.Bot(command_prefix=PREFIX, intents=nextcord.Intents.all(), case_insensitive=True, owner_ids=[OWNER])

for i in os.listdir("./cogs"):
    if i.endswith(".py"):
        bot.load_extension(f"cogs.{i[:-3]}")

@bot.event
async def on_ready():
    print(f"📡 | Bot ID: {bot.user.id} | Bot Name: {bot.user.name}\n❤️ | Trete meinem Discord bei: https://discord.gg/x8b26bTCd4")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
    except commands.ExtensionAlreadyLoaded:
        return await ctx.send("Cog is already loaded")
    except commands.ExtensionNotFound:
        return await ctx.send("Cog is not found")
    await ctx.send("Cog loaded")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f"cogs.{extension}")
    except commands.ExtensionNotFound:
        return await ctx.send("Cog is not found")
    await ctx.send("Cog reloaded")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
    except commands.ExtensionNotFound:
        return await ctx.send("Cog is not found")
    await ctx.send("Cog unloaded")

@bot.command()
@commands.is_owner()
async def check(ctx, cog_name):
    try:
        bot.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog is loaded")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    else:
        await ctx.send("Cog is unloaded")
        bot.unload_extension(f"cogs.{cog_name}")

@bot.event
async def on_application_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = nextcord.Embed(
                title="⌚ × Cooldown",
                description=f"» Du musst noch {round(error.retry_after)} Sekunden warten!",
            )
            await ctx.send(embed=em, delete_after=20)
            return
        else:
            userem = nextcord.Embed(
                title="❌ × Ein Fehler ist aufgetreten",
                description=f"Beim Ausführen dieses Befehls ist ein Fehler aufgetreten. Bitte versuchen sie es später erneut!",
            )
            em = nextcord.Embed(title="❌ Fehler", description=f"```{error}```")
            errorkanal = bot.get_channel(ERROR_CHANNEL)
            await errorkanal.send(embed=em)
            await ctx.send(embed=userem, delete_after=30)
            return

@bot.event
async def on_command_error(ctx, error):
        if isinstance(error, commands.NotOwner):
            em = nextcord.Embed(
                title="👑 × Du darfst diesen Befehl nicht ausführen",
                description=f"Nur <@{OWNER}> darf diesen Command benutzen!",
            )
            await ctx.send(embed=em, delete_after=20)
            return
        else:
            userem = nextcord.Embed(
                title="❌ × Ein Fehler ist aufgetreten",
                description=f"Beim Ausführen dieses Befehls ist ein Fehler aufgetreten. Bitte versuchen sie es später erneut!",
            )
            em = nextcord.Embed(title="❌ Fehler", description=f"```{error}```")
            errorkanal = bot.get_channel(ERROR_CHANNEL)
            await errorkanal.send(embed=em)
            await ctx.send(embed=userem, delete_after=30)
            return

bot.run(TOKEN)