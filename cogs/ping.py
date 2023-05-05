import discord
from discord.ext import commands
from discord import app_commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")


    @app_commands.command(name="ping", description="the bot will reply")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

async def setup(client):
    await client.add_cog(ping(client))