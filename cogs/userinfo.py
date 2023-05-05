import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="userinfo", description="All information about the user")
    async def userinfo(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        try:
            
            if member is None:
                member = interaction.user
            elif member is not None:
                member = member

            member_color = member.color if member else interaction.user.color
            member_avatar = member.avatar if member else interaction.user.avatar
            member_name = member.name if member else interaction.user.name
            member_id = member.id if member else interaction.user.id
            member_dis = member.discriminator if member else interaction.user.discriminator
            member_nick = member.nick if member else interaction.user.nick
            member_join = member.joined_at.strftime("%m/%d/%Y, %H:%M:%S") if member else interaction.user.joined_at.strftime("%m/%d/%Y, %H:%M:%S")
            member_created = member.created_at.strftime("%m/%d/%Y, %H:%M:%S") if member else interaction.user.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            member_status = str(member.status).title() if member else str(interaction.user.status).title()
            member_top_role = member.top_role.name if member else interaction.user.top_role.name
            member_bot = member.bot if member else interaction.user.bot

            info_embed = discord.Embed(title=f"{member_name}'s User Information", description="All information about the user.", color=member_color)
            info_embed.set_thumbnail(url=member_avatar)
            info_embed.add_field(name="Name:", value=member_name,inline=False)
            info_embed.add_field(name="ID:", value=member_id,inline=False)
            info_embed.add_field(name="Discriminator:", value=member_dis,inline=False)
            info_embed.add_field(name="Nickname:", value=member_nick,inline=False)
            info_embed.add_field(name="Joined At:", value=member_join,inline=False)
            info_embed.add_field(name="Created At:", value=member_created,inline=False)
            info_embed.add_field(name="Status:", value=member_status,inline=False)
            info_embed.add_field(name="Top Role:", value=member_top_role,inline=False)
            info_embed.add_field(name="Bot User?", value=member_bot,inline=False)


            await interaction.response.send_message(embed=info_embed)
        except Exception as e:
            print(f"An error occurred in userinfo: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")     

async def setup(client):
    await client.add_cog(userinfo(client))