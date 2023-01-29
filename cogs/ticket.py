import nextcord
from nextcord.ext import commands

class View(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Erstellen", style=nextcord.ButtonStyle.blurple, custom_id="view_1234"
    )
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        c = interaction.guild.get_channel(1043280341365952572)
        t = await c.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites= {
                interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
                interaction.user: nextcord.PermissionOverwrite(view_channel=True)
            }
        )
        em = nextcord.Embed(
            title="Ticket",
            description="..."
        )
        await t.send(content=f"{interaction.user.mention}", embed=em, view=Edit())
        
        await interaction.response.send_message(f"Ticket in {t.mention} erstellt", ephemeral=True)

class Edit(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Schließen", style=nextcord.ButtonStyle.danger, custom_id="view_12345"
    )
    async def create(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        
        await interaction.response.send_message(f"Ticket wird geschlossen ...", ephemeral=True)
        await interaction.channel.delete()
        await interaction.user.send("Dein Ticket wurde geschlossen")


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View())
        self.bot.add_view(Edit())
        
    @nextcord.slash_command(description="Ticket Setup", default_member_permissions=8)
    async def ticket(self, interaction: nextcord.Interaction):
        await interaction.channel.send(view=View())
        await interaction.response.send_message("Erfolgreich", ephemeral=True)
    
def setup(bot):
    bot.add_cog(Ticket(bot))