import discord
from discord.ext import commands
import json

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

       

    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcom.py is ready!")

    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        print("Member joined:", member)
        
        # Create and send embed
        embed = discord.Embed(title="Welcome!", description=f"Welcome nyet, {member.mention}!", color=0x00ff00)
        await member.guild.text_channels[0].send(embed=embed)
    



async def setup(client):
    await client.add_cog(Welcome(client))