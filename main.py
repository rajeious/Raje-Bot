import discord
import os
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
from discord import Activity, ActivityType

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    activity = Activity(type=ActivityType.watching, name=f"{len(client.guilds)} servers.", status=discord.Status.dnd)
    await client.change_presence(activity=activity)
    print("Bot is Online!")
    client.loop.create_task(update_activity_status())

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def update_activity_status():
    while True:
        activity = Activity(type=ActivityType.watching, name=f"{len(client.guilds)} servers.")
        await client.change_presence(activity=activity, status=discord.Status.dnd)
        await asyncio.sleep(900)  # update every 15 minutes

@client.event
async def on_guild_update(before, after):
    if not before.features and "COMMUNITY" in after.features:
        # The guild has just enabled the "COMMUNITY" feature
        channel = after.system_channel or after.text_channels[0]
        await channel.send("You have enabled the community!")

@client.event
async def on_guild_join(guild):
    if "COMMUNITY" not in guild.features:
        system_channel = guild.system_channel
        if system_channel is not None:
            await system_channel.send("This guild does not have the community feature enabled. " +
                                       "Some features may not work.")
        else:
            await guild.text_channels[0].send("This guild does not have the community feature enabled.\n" +
                                        "some features will not work" )         
    await asyncio.sleep(900)  # update every 15 minutes
    activity = Activity(type=ActivityType.watching, name=f"{len(client.guilds)} servers.")
    await client.change_presence(activity=activity, status=discord.Status.dnd)

@client.event
async def on_guild_remove(guild):

    await asyncio.sleep(900)  # update every 15 minutes
    activity = Activity(type=ActivityType.watching, name=f"{len(client.guilds)} servers.")
    await client.change_presence(activity=activity, status=discord.Status.dnd)
    
async def main():
    
    await load()
    await client.start(os.getenv("TOKEN"))

keep_alive()
asyncio.run(main())
