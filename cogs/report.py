import nextcord
from nextcord.ext import commands
from config import REPORT_CHANNEL

class USERREPORT(nextcord.ui.Modal):
    def __init__(self, user):
        super().__init__(
            "Nutzer Melden",
            timeout=5 * 60,
        )
        self.user = user

        self.grund = nextcord.ui.TextInput(
            label="Grund",
            min_length=2,
            max_length=1000,
            style=nextcord.TextInputStyle.paragraph
        )
        self.bewe = nextcord.ui.TextInput(
            label="Beweise",
            min_length=2,
            max_length=1000,
            style=nextcord.TextInputStyle.paragraph,
            required=False
        )
        self.add_item(self.grund)
        self.add_item(self.bewe)
        
        


    async def callback(self, interaction: nextcord.Interaction) -> None:
        report_channel = interaction.client.get_channel(REPORT_CHANNEL)
        if self.bewe is None:
            bw = "```/```"
        
        else:
            bw = f"```{self.bewe.value}```"
            
        em = nextcord.Embed(
            title="Nutzer gemeldet",
            description=f"User: {self.user.name} ({self.user.id})\nAuthor: {interaction.user.name} ({interaction.user.id})"
        )
        em.add_field(name="Grund", value=f"```{self.grund.value}```")
        em.add_field(name="Beweise", value=bw)
        
        await report_channel.send(embed=em)
        
        await interaction.response.send_message(f"{self.user.mention} erfolgreich gemeldet", ephemeral=True)

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @nextcord.message_command(name="Nachricht Melden")
    async def report(self, interaction: nextcord.Interaction, message: nextcord.Message):
        report_channel = self.bot.get_channel(REPORT_CHANNEL)
        
        em = nextcord.Embed(
            title="Nachricht gemeldet",
            description=f"```{message.content}```"
        )
        em.add_field(name="Author", value=f"`{message.author.name}`")
        em.add_field(name="Nutzer", value=f"`{interaction.user.name}`")
        
        await report_channel.send(embed=em)
        await interaction.response.send_message(f"Nachricht von {message.author.mention} erfolgreich gemeldet", ephemeral=True)
        
    @nextcord.user_command(name="Nutzer Melden")
    async def user_report(self, interaction: nextcord.Interaction, member: nextcord.Member):
        await interaction.response.send_modal(USERREPORT(member))
        
def setup(bot):
    bot.add_cog(Report(bot))