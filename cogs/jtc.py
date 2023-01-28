import nextcord
from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord import ChannelType, SlashOption

import asyncio

channels = []

class JTC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # method
    async def get_channel(self, guild: int):
        async with self.bot.db.cursor() as c:
            await c.execute("SELECT channel FROM jtcs WHERE guild = ?", (guild,))
            data = await c.fetchone()
            return int(data[0]) if data is not None else None
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        
        await asyncio.sleep(2)
        
        async with self.bot.db.cursor() as c:
            await c.execute("CREATE TABLE IF NOT EXISTS jtcs(channel INTEGER, guild INTEGER)")
        await self.bot.db.commit()
        
        print("JTC: WORKING")
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        if after.channel and await self.get_channel(after.channel.guild.id) == after.channel.id:
            c = await after.channel.clone(name=f"⌚ | {member.name}")
            await member.move_to(c)
            channels.append(c.id)
        
        if before.channel and before.channel.id in channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                channels.remove(before.channel.id)
                
    @nextcord.slash_command(description="Stelle das JTC System ein")
    async def setup_jtc(self, ctx: nextcord.Interaction, channel: GuildChannel = SlashOption(description="Der Kanal", required=True, channel_types=[ChannelType.voice])):
        if await self.get_channel(ctx.guild.id) is not None:
            async with self.bot.db.cursor() as c:
                await c.execute("UPDATE jtcs SET channel = ? WHERE guild = ?", (channel.id, ctx.guild.id,))

            await self.bot.db.commit()
            
        else:
            async with self.bot.db.cursor() as c:
                await c.execute("INSERT INTO jtcs (channel, guild) VALUES (?, ?)", (channel.id, ctx.guild.id,))

            await self.bot.db.commit()

            
        
        
def setup(bot):
    bot.add_cog(JTC(bot))