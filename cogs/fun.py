import nextcord
from nextcord.ext import commands
from nextcord import SlashOption

import random
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Stelle dem Bot eine Frage und er wird sie dir beantworten.")
    async def ask(self, ctx: nextcord.Interaction, *, question: str = SlashOption(description="Deine Frage", required=True)):
        answers = [
            "Ja",
            "Nein",
            "Vielleicht",
            "Wahrscheinlich",
            "Sieht so aus",
            "Sehr wahrscheinlich",
            "Sehr unwahrscheinlich",
        ]

        answer = random.choice(answers)

        em = nextcord.Embed(
            title="8ball",
            description=f"» Frage: {question}\n» Antwort: {answer}",
            color=nextcord.Color.random()
        )
        await ctx.response.send_message(embed=em, ephemeral=True)

    @nextcord.slash_command(description="Würfelt eine Zahl zwischen 1 und 6.")
    async def dice(self, ctx: nextcord.Interaction):
        dice = random.randint(1, 6)
        await ctx.response.send_message(f"Du hast eine {dice} gewürfelt!", ephemeral=True)

    @nextcord.slash_command(description="Lasse den Bot eine Münze werfen.")
    async def coin(self, ctx: nextcord.Interaction, pick: str = SlashOption(description="Wähle Kopf oder Zahl", required=True, choices=["Kopf", "Zahl"])):
        coin = random.choice(["Kopf", "Zahl"])
        if pick.lower() == coin.lower():
            await ctx.response.send_message(f"Du hast {pick} gewählt und {coin} wurde geworfen! 🤔", ephemeral=True)
        else:
            await ctx.response.send_message(f"Du hast {pick} gewählt und {coin} wurde geworfen! 🤔", ephemeral=True)


def setup(bot):
    bot.add_cog(Fun(bot))