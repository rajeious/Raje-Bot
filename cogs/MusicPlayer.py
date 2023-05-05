import discord
import asyncio
import wavelink
from discord.ext import commands
from discord import app_commands


class MusicPlayer(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def setup_hook(self):
        print("Setting up Wavelink node...")
        # Wavelink 2.0 has made connecting Nodes easier... Simply create each Node
        # and pass it to NodePool.connect with the client/bot.
        node: wavelink.Node = wavelink.Node(uri='lavalink.alexanderof.xyz:2333', password='lavalink', secure=False)
        try:
            await wavelink.NodePool.connect(client=self.client, nodes=[node])
        except Exception as e:
            print(f"Failed to connect to Wavelink node: {e}")
        else:
            print("Connected to Wavelink node successfully!")
        

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")
        await self.setup_hook()

    @app_commands.command(name="join", description="the bot will join the voice channel")
    async def join(self, interaction: discord.Interaction):
        try:
            voice_channel = interaction.user.voice.channel
            if interaction.guild.voice_client is not None:
                await interaction.response.send_message("Bot already joined the voice channel.")
            else:
                vc: wavelink.Player = await voice_channel.connect(cls=wavelink.Player)
                await interaction.response.send_message("Joined.")
        except AttributeError:
            await interaction.response.send_message("You must be in a voice channel to use this command.")
        except Exception as e:
            print(f"An error occurred in join command: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")

    @app_commands.command(name="play", description="the bot will play music from youtube")
    async def play(self, interaction: discord.Interaction, *, search: str):
        try:
            
            if not interaction.user.voice or not interaction.user.voice.channel:
                await interaction.response.send_message("You must join a voice channel to play music.")
                return
            
            await interaction.response.defer()

            if not interaction.guild.voice_client:
                vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = interaction.guild.voice_client

            track = await wavelink.YouTubeTrack.search(search, return_first=True)
            
            
            # Send a response message once the music starts playing
            message = await interaction.followup.send(f"Searching for **{search}**...")

            await vc.play(track)

            # Edit the response message to inform the user that the bot is now playing the track
            await asyncio.sleep(1)
            await message.edit(content=f"Now Playing **{track}**")

        except Exception as e:
            print(f"An error occurred in play: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")

    @app_commands.command(name="pause", description="the bot will pause the currently playing music")
    async def pause(self, interaction: discord.Interaction):
        try:
            
            if not interaction.user.voice or not interaction.user.voice.channel:
                await interaction.response.send_message("You must be in a voice channel to use this command.")
                return
            
            vc = interaction.guild.voice_client
            if vc.is_playing:
                await vc.pause()
                embed_pause = discord.Embed(title=f"Paused", color=discord.Color.from_rgb(255, 255 ,255))
                await interaction.response.send_message(embed=embed_pause)
            else:
                await interaction.response.send_message("No music is currently playing.")
        except Exception as e:
            print(f"An error occurred in pause: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")

    @app_commands.command(name="resume", description="the bot will resume the currently paused music")
    async def resume(self, interaction: discord.Interaction):
        try:
            
            if not interaction.user.voice or not interaction.user.voice.channel:
                await interaction.response.send_message("You must be in a voice channel to use this command.")
                return
            
            vc = interaction.guild.voice_client
            if vc.is_paused():
                await vc.resume()
                embed_resume = discord.Embed(title=f"Resumed", color=discord.Color.from_rgb(255, 255 ,255))
                await interaction.response.send_message(embed=embed_resume)
            else:
                await interaction.response.send_message("The music is not currently paused.")
        except Exception as e:
            print(f"An error occurred in resume: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")

    @app_commands.command(name="stop", description="the bot will stop playing music")
    async def stop(self, interaction: discord.Interaction):
        try:
            
            if not interaction.user.voice or not interaction.user.voice.channel:
                await interaction.response.send_message("You must be in a voice channel to use this command.")
                return
            
            vc = interaction.guild.voice_client
            if vc.is_playing:
                await vc.stop()
                embed_stop = discord.Embed(title=f"Stopped", color=discord.Color.from_rgb(255, 255 ,255))
                await interaction.response.send_message(embed=embed_stop)
            else:
                await interaction.response.send_message("No music is currently playing.")
        except Exception as e:
            print(f"An error occurred in stop: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.")

    @app_commands.command(name="disconnect", description="the bot will leave the voice channel")
    async def disconnect(self, interaction: discord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client
        await vc.disconnect()

        await interaction.response.send_message("Disconnected")
    
async def setup(client):
    await client.add_cog(MusicPlayer(client))
