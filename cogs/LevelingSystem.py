# Import required modules
import discord
import json
import math
import random
from discord.ext import commands
from discord import app_commands
from typing import Optional

# Define constants
XP_PER_LEVEL = 50
LEVEL_UP_MESSAGE = "Congratulations, you leveled up to level {level}!"

# Define the LevelingSystem cog
class LevelingSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("cogs/json/xp_data.json", "r") as f:
            self.xp_data = json.load(f)

    async def save_xp_data(self):
        with open(self.xp_data_file, "w") as f:
            json.dump(self.xp_data, f)

    async def load_xp_data(self):
        with open(self.xp_data_file, "r") as f:
            self.xp_data = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_xp_data()
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @commands.Cog.listener()
    async def on_member_remove(self, user):
        with open("cogs/json/xp_data.json", "r") as f:
            self.xp_data = json.load(f)
    
            guild_id = str(user.guild.id)
            if guild_id in self.xp_data and str(user.id) in self.xp_data[guild_id]:
                del self.xp_data[guild_id][str(user.id)]

                with open("cogs/json/xp_data.json", "w") as f:
                    json.dump(self.xp_data, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        global XP_PER_LEVEL
        
        # Ignore messages from bots
        if message.author.bot:
            return

        # Check if user is in XP data
        user_id = str(message.author.id)
        guild_id = str(message.guild.id)

        if guild_id not in self.xp_data:
            self.xp_data[guild_id] = {}

        if user_id not in self.xp_data[guild_id]:
            self.xp_data[guild_id][user_id] = {"xp": 0, "level": 1}

        # Set initial XP for level 1 users
        if self.xp_data[guild_id][user_id]["level"] == 1:
            XP_PER_LEVEL = 50

        # Add XP for message
        random_xp = random.randint(5, 20)
        self.xp_data[guild_id][user_id]["xp"] += random_xp

        # Check if user leveled up
        current_xp = self.xp_data[guild_id][user_id]["xp"]
        current_level = self.xp_data[guild_id][user_id]["level"]
        xp_required = math.ceil((6 * (current_level * 6)) / 2.5)

        if current_xp >= xp_required:
            self.xp_data[guild_id][user_id]["level"] += 1
            current_level += 1
            self.xp_data[guild_id][user_id]["xp"] = 0  # Reset XP
            xp_required = math.ceil((6 * (current_level * 6)) / 2.5)

            level_up_embed = discord.Embed(
                title="you leveled up!", color=discord.Color.green())
            level_up_embed.add_field(
                name="Congratulations", value=f"{message.author.mention} you leveled up to level {self.xp_data[guild_id][user_id]['level']}!")

            await message.channel.send(embed=level_up_embed)

        # Save XP data to file
        with open("cogs/json/xp_data.json", "w") as f:
            json.dump(self.xp_data, f, indent=4)

        await self.bot.process_commands(message)

    @app_commands.command(name="level", description="check your XP and level")
    async def level(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        try:
        
            if member is None:
                user_id = str(interaction.user.id)
                guild_id = str(interaction.guild.id)
            else:
                user_id = str(member.id)
                guild_id = str(member.guild.id)

            #Check if user is in XP data
            if guild_id not in self.xp_data or user_id not in self.xp_data[guild_id]:
                if member is None:
                    await interaction.response.send_message("You do not have any XP yet.")
                else:
                    await interaction.response.send_message(f"{member.display_name} does not have any XP yet.")
                return

            current_level = self.xp_data[guild_id][user_id]["level"]
            xp_required = math.ceil((6 * (current_level * 6)) / 2.5)
    
            # Get user's XP
            xp = self.xp_data[guild_id][user_id]["xp"]
            level = self.xp_data[guild_id][user_id]["level"]

            user_name = member.display_name if member else interaction.user.name
            embed = discord.Embed(title=f"{user_name}'s XP and Level", color=discord.Color.green())
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
            embed.add_field(name="XP", value=f"{xp}", inline=False)
            embed.add_field(name="Level", value=f"{level}", inline=False)
            embed.add_field(name="TOTAL XP required for next level", value=f"{xp_required}", inline=False)
    
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(f"An error occurred in level: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")

async def setup(client):
    await client.add_cog(LevelingSystem(client))