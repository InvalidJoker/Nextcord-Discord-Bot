import nextcord
from nextcord.ext import commands


class Verify(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Verifizieren", style=nextcord.ButtonStyle.green, custom_id="view7803r783"
    )
    async def callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = interaction.guild.get_role(1043280333879136306)
        logs = interaction.guild.get_channel(1043280357262372986)
        
        if role in interaction.user.roles:
            await interaction.response.send_message("Du bist bereits verifiziert", ephemeral=True)
            return
        
        await interaction.user.add_roles(role)
        await interaction.response.send_message("Du wurdest erfolgreich verifiziert", ephemeral=True)
        
        await logs.send(f"{interaction.user.mention} wurde erfolgreich verifiziert")


class VerifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Verify())
        
    @nextcord.slash_command(description="Verify Setup", default_member_permissions=8)
    async def verify(self, interaction: nextcord.Interaction):
        await interaction.channel.send(view=Verify())
        await interaction.response.send_message("Erfolgreich", ephemeral=True)
    
def setup(bot):
    bot.add_cog(VerifyCog(bot))