import discord
from discord.ext import commands
from dotenv import load_dotenv
from mpd import MPDClient
import os


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MPD_HOST = os.getenv('MPD_HOST')
MPD_PORT = os.getenv('MPD_PORT')
MPD_STREAM_PORT = os.getenv('MPD_STREAM_PORT')
MPD_PASSWORD = os.getenv('MPD_PASSWORD', '')


class MPD_Streamer(commands.Cog):
    """
    Some commands to send to a MPD server, as well as the ability to attach a MPD stream
    to a Discord voice channel.
    """
    def __init__(self, bot):
        self.bot = bot
        self.client = MPDClient()
        self.stream_url = "http://{0}:{1}/mpd.ogg".format(MPD_HOST, MPD_STREAM_PORT)

    def _mpd_command(self, kwargs):
        """
        Sends commands to the mpd server
        :param kwargs: a list of strings (function names)
        :return: a list of the results
        """
        self.client.connect(MPD_HOST, MPD_PORT)
        if MPD_PASSWORD:
            self.client.password(MPD_PASSWORD)
        return_values = []
        for arg in kwargs:
            return_values.append(getattr(self.client, arg)())
        self.client.disconnect()
        return return_values

    def _get_current_song(self) -> str:
        current, status = self._mpd_command(['currentsong', 'status'])
        title, artist, album = current.get("title"), current.get("artist"), current.get("album")
        elapsed, duration = status.get("elapsed"), status.get("duration")
        try:
            percent = int((float(elapsed) / float(duration)) * 100)
        except TypeError:
            return "Couldn't get values:\n{0}\n{1}".format(current, status)
        if not title or not artist or not album:
            return "Couldn't get values:\n{0}\npercent: {1}%".format(current, percent)
        else:
            return "**{0}**\n{1}, *{2}*\npercent: {3}%".format(title, artist, album, percent)

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel

        Currently requires the Voice Channel ID to connect
        """
        await ctx.send("Connecting to the channel; type $help for help")
        # Connects to voice
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.stream_url))
            ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
            return await ctx.send("Now playing:\n" + self._get_current_song())
        await channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.stream_url))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send("Now playing:\n" + self._get_current_song())

    @commands.command()
    async def stop(self, ctx):
        """Disconnects from the voice channel"""
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(name='currentsong', aliases=['current'])
    async def currentsong(self, ctx):
        """Gets the current song name

        Requires no arguments
        """
        await ctx.send(self._get_current_song())

    @commands.command()
    async def next(self, ctx):
        """Skips to the next song

        Requires no arguments
        """
        _, msg = self._mpd_command(['next']), self._get_current_song()
        await ctx.send("Now playing:\n{0}".format(msg))

    @commands.command(name='previous', aliases=['prev'])
    async def previous(self, ctx):
        """Goes back to the previous song

        Requires no arguments
        """
        _, msg = self._mpd_command(['previous']), self._get_current_song()
        await ctx.send("Now playing:\n{0}".format(msg))


# Main script
bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), description="MPD_Streamer for discord")


@bot.event
async def on_ready():
    print("Logged in as user {0}".format(bot.user))

bot.add_cog(MPD_Streamer(bot))
bot.run(DISCORD_TOKEN)
