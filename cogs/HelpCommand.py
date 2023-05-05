import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="help", description="Show all commands for the bot")
    async def help(self, interaction: discord.Interaction):
        try:
            help_embed = discord.Embed(title="Help Desk for Raje Bot", description="All commands for the bot", color=discord.Color.random())
            help_embed.set_author(name="Raje Bot", icon_url=self.client.user.avatar)
            help_embed.add_field(name="Level", value="check your XP and level", inline=False)
            help_embed.add_field(name="Userinfo", value="All information about the user", inline=False)
            help_embed.add_field(name="play", value="the bot will play music from youtube", inline=False)
            help_embed.add_field(name="Need Help?", value="[Join and Support The Server!](https://discord.gg/922KbjBCj8)", inline=False)
            help_embed.set_footer(text=f"Requested by <@{interaction.user}>.", icon_url=interaction.user.avatar)

            await interaction.response.send_message(embed=help_embed)
        except Exception as e:
            print(f"An error occurred in help: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")

async def setup(client):
    await client.add_cog(HelpCommand(client))